import re
from contextlib import contextmanager
from sqlite3 import OperationalError

from django.db import connection as default_connection
from django.db import transaction


class LockConnection(object):
    @property
    def vendor(self):
        return "unknown"

    @property
    def in_transaction(self):
        return False

    def execute(self, sql, params=None):
        """
        :param sql: A string of the SQL to execute
        :type sql: str
        :param params: A list/tuple of the SQL parameters
        :type params: list|tuple|None
        """
        pass


class DjangoLockConnection(LockConnection):
    def __init__(self, connection):
        self.connection = connection

    @property
    def vendor(self):
        return self.connection.vendor

    @property
    def in_transaction(self):
        return self.connection.in_atomic_block

    def execute(self, sql, params=None):
        with self.connection.cursor() as c:
            c.execute(sql, params or [])


class SQLAlchemyLockConnection(LockConnection):
    param_pattern = re.compile(r"([^%])(%s)")

    def __init__(self, session, engine):
        """
        :param session:
        :type session: sqlalchemy.orm.session.Session
        :type engine: sqlalchemy.engine.base.Engine
        """
        self.session = session
        self.engine = engine
        self.param_number = 0

    def convert_to_named_parameters(self, sql, params):
        i = 0
        params_dict = {}
        match = self.param_pattern.match(sql)
        while match:
            name = "key{i}".format(i=i)
            replace = "{group1}:{name}".format(group1=match.group(1), name=name)
            params_dict.update({name: params[i]})
            sql = re.sub(self.param_pattern, replace, sql, count=1)
            i += 1
            match = self.param_pattern.match(sql)
        return sql, params_dict

    @property
    def vendor(self):
        return self.engine.name

    @property
    def in_transaction(self):
        return bool(self.session.transaction)

    def execute(self, sql, params=None):
        sql, params_dict = self.convert_to_named_parameters(sql, params or [])
        self.session.execute(sql, params_dict)


class LockOperation(object):
    def __init__(self, connection):
        self.connection = connection

    def validate(self):
        raise NotImplementedError(
            "Lock not implemented for vendor {vendor}".format(
                vendor=self.connection.vendor
            )
        )

    def execute(self):
        pass

    def revert(self):
        pass


class SQLiteLockOperation(LockOperation):
    @property
    def model(self):
        from kolibri.core.device.models import SQLiteLock

        return SQLiteLock

    def validate(self):
        pass

    def execute(self):
        sql, params = self.model.get_acquire_sql()
        while True:
            try:
                self.connection.execute(sql, params)
            except OperationalError as e:
                if "database is locked" not in str(e):
                    raise e

    def revert(self):
        sql, params = self.model.get_release_sql()
        try:
            self.connection.execute(sql, params)
        except OperationalError as e:
            if "database is locked" not in str(e):
                raise e


class PostgresLockOperation(LockOperation):
    def validate(self):
        if not self.connection.in_transaction:
            raise NotImplementedError("Advisory lock requires transaction")

    def execute(self, key=1):
        sql = "SELECT pg_advisory_xact_lock(%s) AS lock;"
        self.connection.execute(sql, [key])


def get_lock_operation(lock_connection):
    if lock_connection.vendor == "sqlite":
        return SQLiteLockOperation(lock_connection)
    elif lock_connection.vendor == "postgresql":
        return PostgresLockOperation(lock_connection)
    else:
        return LockOperation(lock_connection)


@contextmanager
def db_lock(lock_connection=None):
    connection = lock_connection or DjangoLockConnection(default_connection)
    lock_op = get_lock_operation(connection)

    lock_op.validate()
    lock_op.execute()
    yield
    lock_op.revert()


@contextmanager
def db_lock_with_transaction():
    with transaction.atomic():
        with db_lock():
            yield
