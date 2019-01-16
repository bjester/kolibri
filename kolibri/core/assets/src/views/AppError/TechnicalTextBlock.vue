<template>

  <div>
    <!-- visible text area, hidden to screenreaders -->
    <textarea
      v-model="text"
      readonly
      class="error-log"
      wrap="soft"
      aria-hidden="true"
      :style="[dynamicHeightStyle, {
        backgroundColor: $coreBgError,
        border: $coreGrey300,
      }]"
    >
    </textarea>
    <!-- invisible text block for copying, visible to screenreaders -->
    <pre ref="textBox" class="visuallyhidden">{{ text }}</pre>
    <div>
      <KButton
        v-if="clipboardCapable"
        ref="copyButton"
        class="copy-to-clipboard-button"
        :primary="false"
        :text="$tr('copyToClipboardButtonPrompt')"
      />
    </div>
  </div>

</template>


<script>

  import { mapGetters, mapState, mapActions } from 'vuex';
  import KButton from 'kolibri.coreVue.components.KButton';
  import ClipboardJS from 'clipboard';

  export default {
    name: 'TechnicalTextBlock',
    $trs: {
      copyToClipboardButtonPrompt: 'Copy to clipboard',
      copiedToClipboardConfirmation: 'Copied to clipboard',
      downloadAsTextPrompt: 'Or download as a text file',
    },
    components: {
      KButton,
    },
    props: {
      text: {
        type: String,
        default: '',
      },
      maxHeight: {
        type: Number,
        required: false,
      },
      minHeight: {
        type: Number,
        default: 72,
      },
    },
    computed: {
      ...mapGetters(['$coreBgError', '$coreGrey300']),
      ...mapState({
        error: state => state.core.error,
      }),
      clipboardCapable() {
        return ClipboardJS.isSupported();
      },
      dynamicHeightStyle() {
        return {
          height: `${16 + this.text.split('\n').length * 18}px`,
          maxHeight: `${this.maxHeight}px`,
          minHeight: `${this.minHeight}px`,
        };
      },
    },
    mounted() {
      if (this.clipboardCapable) {
        this.clipboard = new ClipboardJS(this.$refs.copyButton.$el, {
          text: () => this.text,
          // needed because modal changes browser focus
          container: this.$refs.textBox,
        });

        this.clipboard.on('success', () => {
          this.createSnackbar({
            text: this.$tr('copiedToClipboardConfirmation'),
            autoDismiss: true,
          });
        });
      }
    },
    destroyed() {
      if (this.clipboard) {
        this.clipboard.destroy();
      }
    },
    methods: {
      ...mapActions(['createSnackbar']),
    },
  };

</script>


<style lang="scss" scoped>

  @import '~kolibri.styles.definitions';

  .error-log {
    width: 100%;
    padding: 8px;
    font-family: monospace;
    line-height: 18px;
    white-space: pre;
    resize: none;
    border-radius: $radius;
  }

  .copy-to-clipboard-button {
    margin-left: 0;
  }

</style>