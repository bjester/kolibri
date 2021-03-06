<template>

  <!-- eslint-disable max-len -->
  <KModal
    :title="$tr('csvDetails')"
    :submitText="$tr('close')"
    size="large"
    @cancel="closeModal"
    @submit="closeModal"
  >
    <p>{{ $tr('sectionDescription') }}</p>

    <table>
      <thead>
        <tr>
          <th>{{ $tr('columnNameHeader') }}</th>
          <th>{{ $tr('columnIDHeader') }}</th>
          <th>{{ $tr('columnInfoHeader') }}</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>
            {{ $tr('uuid') }}<br>
            <span class="label" :style="label">{{ $tr('optional') }}</span>
          </td>
          <td><code>UUID</code></td>
          <td>{{ $tr('uuidInfo') }}</td>
        </tr>
        <tr>
          <td>
            {{ $tr('username') }}<br>
            <span class="label" :style="label">{{ $tr('required') }}</span>
          </td>
          <td><code>USERNAME</code></td>
          <td>{{ $tr('usernameInfo') }}</td>
        </tr>
        <tr>
          <td>
            {{ $tr('password') }}<br>
            <span class="label" :style="label">{{ $tr('required') }}</span>
          </td>
          <td><code>PASSWORD</code></td>
          <td>{{ $tr('passwordInfo') }} <code>*</code></td>
        </tr>
        <tr>
          <td>
            {{ $tr('fullName') }}<br>
            <span class="label" :style="label">{{ $tr('required') }}</span>
          </td>
          <td><code>FULL_NAME</code></td>
          <td>{{ $tr('fullNameInfo') }}</td>
        </tr>
        <tr>
          <td>
            {{ $tr('userType') }}<br>
            <span class="label" :style="label">{{ $tr('required') }}</span>
          </td>
          <td><code>USER_TYPE</code></td>
          <td>
            <div>{{ $tr('possibleValues') }}</div>
            <ul>
              <li><code>ADMIN</code></li>
              <li><code>FACILITY_COACH</code></li>
              <li><code>CLASS_COACH</code></li>
              <li><code>LEARNER</code></li>
            </ul>
          </td>
        </tr>
        <tr>
          <td>
            {{ $tr('identifier') }}<br>
            <span class="label" :style="label">{{ $tr('optional') }}</span>
          </td>
          <td><code>IDENTIFIER</code></td>
          <td>{{ $tr('identifierInfo') }}</td>
        </tr>
        <tr>
          <td>
            {{ $tr('birthYear') }}<br>
            <span class="label" :style="label">{{ $tr('optional') }}</span>
          </td>
          <td><code>BIRTH_YEAR</code></td>
          <td>{{ $tr('yearInfo') }}</td>
        </tr>
        <tr>
          <td>
            {{ $tr('gender') }}<br>
            <span class="label" :style="label">{{ $tr('optional') }}</span>
          </td>
          <td><code>GENDER</code></td>
          <td>
            <div>{{ $tr('possibleValues') }}</div>
            <ul>
              <li><code>MALE</code></li>
              <li><code>FEMALE</code></li>
              <li><code>NOT_SPECIFIED</code></li>
            </ul>
          </td>
        </tr>
        <tr>
          <td>
            {{ $tr('enrolled') }}<br>
            <span class="label" :style="label">{{ $tr('optional') }}</span>
          </td>
          <td><code>ENROLLED_IN</code></td>
          <td>
            <div>{{ $tr('listClassesEnrolled') }}</div>
            <ul>
              <li>{{ $tr('listClassesEnrolledL1') }}</li>
              <li>{{ $tr('listClassesEnrolledL2') }}</li>
              <li>{{ $tr('listClassesEnrolledL3') }}</li>
            </ul>
          </td>
        </tr>
        <tr>
          <td>
            {{ $tr('assigned') }}<br>
            <span class="label" :style="label">{{ $tr('optional') }}</span>
          </td>
          <td><code>ASSIGNED_TO</code></td>
          <td>
            <div>{{ $tr('listClassesAssigned') }}</div>
            <ul>
              <li>{{ $tr('listClassesAssignedL1') }}</li>
              <li>{{ $tr('listClassesAssignedL2') }}</li>
              <li>{{ $tr('listClassesAssignedL3') }}</li>
            </ul>
          </td>
        </tr>

      </tbody>
    </table>
  </KModal>
  <!-- eslint-enable max-len -->

</template>


<script>

  export default {
    name: 'CsvInfoModal',
    computed: {
      label() {
        return { color: this.$themeTokens.annotation };
      },
    },
    methods: {
      closeModal() {
        this.$emit('cancel');
      },
    },
    $trs: {
      csvDetails: 'CSV details',
      sectionDescription:
        'A CSV spreadsheet should use the first row as a header, and contain the following columns:',
      close: 'Close',
      required: 'Required',
      optional: 'Optional',
      uuidInfo:
        'An ID used by Kolibri to uniquely identify a user. Leave it blank to create a new user',
      usernameInfo: 'Maximum 125 characters. Can contain letters, numbers and underscores',
      passwordInfo: 'Maximum 125 characters. To leave unchanged, use an asterisk:',
      fullNameInfo: 'Maximum 125 characters',
      possibleValues: 'Possible values:',
      identifierInfo:
        'Any identifying string, such as a student ID or email address. Maximum 64 characters',
      yearInfo: 'A four-digit year, greater than 1900',
      listClassesEnrolled: 'Classes to enroll the user in as a learner:',
      listClassesEnrolledL1: 'Can be any type of user',
      listClassesEnrolledL2: {
        message: 'Write the class names separated by commas',
        context:
          'Refers to values in a column of the CSV (comma separated values) file used to import users. When a user is assigned to coach multiple classes, the class names in this field must be separated by commas.',
      },
      listClassesEnrolledL3: {
        message:
          'If an existing class does not match by name, a new class with that name will be created',
        context:
          'Refers to values in a column of the CSV (comma separated values) file used to import users. When a CSV file contains a class name that is not present in the database, import command will create it.',
      },
      listClassesAssigned: {
        message: 'Classes to which the user will be assigned as a coach:',
        context:
          'Description of a column in the CSV (comma separated values) file used to import and export users. Values in this column indicate classes where a coach user will be assigned to.',
      },
      listClassesAssignedL1: {
        message: 'Do not use for learner users',
        context:
          'Refers to values in a column of the CSV (comma separated values) file used to import and export users.',
      },
      listClassesAssignedL2: 'List of class names, separated by commas',
      listClassesAssignedL3: {
        message: 'If an existing class does not match by name, it will be created',
        context:
          'Explanation that when a CSV file is used to import users and classes they are assigned to, and the CSV file contains a class name that is not already present in a facility, a new class with the name listed in the CSV file will be created.  ',
      },
      columnNameHeader: 'Column',
      columnIDHeader: 'Identifier',
      columnInfoHeader: 'Information',
      uuid: 'Database ID',
      username: 'Username',
      password: 'Password',
      fullName: 'Full name',
      userType: 'User type',
      identifier: 'Identifier',
      birthYear: 'Birth year',
      gender: 'Gender',
      enrolled: 'Learner enrollment',
      assigned: 'Coach assignment',
      /* eslint-disable kolibri/vue-no-unused-translations */
      // stub out some extra strings
      downloadSample: 'Download a sample CSV file',
      exampleUser: {
        message: 'Example User {number}',
        context:
          'When downloading a sample CSV file, this string is used to generate some class names. These might be strings like "Example Name 1234", "Example Name 5678"',
      },
      exampleUsername: {
        message: 'user-{number}',
        context:
          'When downloading a sample CSV file, this string is used to generate usernames. These must be valid Kolibri usernames (only letters, no spaces), for example "user-1234"',
      },
      exampleClass: {
        message: 'Example Class - {letter}',
        context:
          'When downloading a sample CSV file, this string is used to generate some class names. These might be strings like "Example Class - A",  "Example Class - B",  and "Example Class - C"',
      },
      /* eslint-enable */
    },
  };

</script>


<style lang="scss" scoped>

  td,
  th {
    padding: 12px 8px;
    line-height: 1.5em;
    text-align: left;
    vertical-align: top;
  }

  .label {
    font-size: smaller;
    font-weight: normal;
  }

  ul {
    margin: 0;
  }

</style>
