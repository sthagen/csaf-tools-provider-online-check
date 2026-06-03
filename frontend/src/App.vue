<template>
  <div id="app">
    <div class="container pt-4">
      <div class="row justify-content-center">
        <div class="col-md-12">
          <div class="card shadow">
            <div class="card-body">
              <h2 class="card-title mb-4">CSAF Provider Check <span class="badge bg-warning text-dark ms-2">Beta</span></h2>

              <p>Check a CSAF Provider's metadata and all its documents for validity.<br />
                Learn more about CSAF (Common Security Advisory Framework) at <a href="https://csaf.io" target="_blank">csaf.io</a>.</p>

              <form @submit.prevent="startScan">
                <div class="mb-3">
                  <label for="domainInput" class="form-label">Enter a domain name or <a href="https://docs.oasis-open.org/csaf/csaf/v2.1/csaf-v2.1.html#717-requirement-7-provider-metadatajson-" title="Provider Metadata File" target="_blank">PMD</a> JSON URL to start the check:</label>
                  <input
                    type="text"
                    class="form-control"
                    id="domainInput"
                    v-model="domain"
                    placeholder="example.com"
                    required
                  >
                </div>

                <button
                  type="submit"
                  class="btn btn-primary"
                  :disabled="loading"
                >
                  <span v-if="loading" class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
                  <span v-else>{{ 'Start Check' }}</span>
                </button>
              </form>

              <!-- display of requirements messages -->
              <div v-if="messagesList" class="mt-4">
                <div v-if="result?.status === 'DONE_CHECKER'">
                  <h3 class="alert-heading">Check completed</h3>
                </div>
                <div v-else-if="result?.status === 'CACHED_CHECKER'">
                  <h3 class="alert-heading">Check result found in cache</h3>
                </div>

                <div v-show="scanTime">
                  Start time of the check: {{ scanTime }}
                </div>

                <h4 :class="trustedProviderStatus" class="small-margin-top medium-font-size">
                  <span v-if="trustedProviderStatus === 'text-green'">PASSED:</span>
                  <span v-else>FAILED:</span>
                  {{ role }}
                </h4>
                <MessageLine v-for="item of trustedProviderMessages" :key="item.text" :text="item.text" :type="item.type"></MessageLine>

                <p class="small-margin-top">
                    <a class="btn btn-primary" data-bs-toggle="collapse" href="#collapseAllMessages" role="button" aria-expanded="false" aria-controls="collapseAllMessages"
                      :key="displayAllMessagesTitle"
                    >
                      {{  displayAllMessagesTitle }}
                    </a>
                </p>
                <div class="collapse" id="collapseAllMessages" ref="allMessagesRef">
                  <div class="card card-body">
                    <h5 class="card-title">All messages:</h5>
                    <div class="card-text log-card-size overflow-scroll">
                      <MessageLine v-for="item of messagesList" :key="item.text" :text="item.text" :type="item.type"></MessageLine>
                    </div>
                  </div>
                </div>
                <p class="small-margin-top">
                    <a class="btn btn-primary" data-bs-toggle="collapse" href="#collapseResultOutput" role="button" aria-expanded="false" aria-controls="collapseResultOutput"
                      :key="displayResultOutputTitle"
                    >
                      {{ displayResultOutputTitle }}
                    </a>
                </p>
                <div class="collapse" id="collapseResultOutput" ref="resultOutputRef">
                  <div class="card card-body">
                    <div class="card-title d-flex gap-2 mb-2">
                      <h5 class="me-auto log-header">Result of the checker:</h5>
                      <button class="btn btn-sm btn-outline-secondary" @click="copyResultToClipboard">Copy to clipboard</button>
                      <button class="btn btn-sm btn-outline-secondary" @click="downloadJson">Download</button>
                    </div>
                    <div class="card-text log-card-size overflow-scroll">
                      <pre>{{ result?.results_checker }}</pre>
                    </div>
                  </div>
                </div>
                <p class="small-margin-top">
                    <a class="btn btn-primary" data-bs-toggle="collapse" href="#collapseLogOutput" role="button" aria-expanded="false" aria-controls="collapseLogOutput"
                      :key="displayLogOutputTitle">
                      {{ displayLogOutputTitle }}
                    </a>
                </p>
                <div class="collapse" id="collapseLogOutput" ref="logOutputRef">
                  <div class="card card-body">
                    <div class="cart-title d-flex gap-2 mb-2">
                      <h5 class="me-auto log-header">Log output:</h5>
                      <button class="btn btn-sm btn-outline-secondary" @click="copyLogToClipboard">Copy to clipboard</button>
                      <button class="btn btn-sm btn-outline-secondary" @click="downloadLog">Download</button>
                    </div>
                    <div class="card-text log-card-size overflow-scroll">
                      <pre>{{ result?.runtime_output?.join('\n') }}</pre>
                    </div>
                  </div>
                </div>
              </div>
              <div
                v-if="result && ['ERROR', 'UNDEFINED', 'INITIALIZED', 'RUNNING_CHECKER', 'PAUSED'].includes(result?.status)"
                class="mt-4"
              >
                <div :class="['alert', resultClass]" role="alert">
                  <div v-if="result.status === 'ERROR' || result.status === 'UNDEFINED'">
                    <h5 class="alert-heading">Error</h5>
                    <p class="mb-0">{{ result.error }}</p>
                  </div>
                  <div v-if="result.status === 'INITIALIZED'">
                    <h5 class="alert-heading">Check started...</h5>
                    <pre>{{ result.results_checker }}</pre>
                  </div>
                  <div v-if="result.status === 'RUNNING_CHECKER'">
                    <h5 class="alert-heading">Check running...</h5>
                    <h6 class="alert-heading">Files checked: {{ result.files_checked }}</h6>
                    <h6 class="alert-heading">Latest file checked: {{ result.latest_file_checked }}</h6>
                    <pre>{{ result.results_checker }}</pre>
                  </div>
                  <div v-if="result.status === 'PAUSED'">
                    <h5 class="alert-heading">Check paused</h5>
                    <pre>{{ result.results_checker }}</pre>
                  </div>
                </div>
                <div v-if="result.runtime_output" class="mt-4">
                  <div :class="['alert', resultClass]" role="alert">
                    <h5 class="alert-heading">Details</h5>
                    <li v-for="(item, index) in result.runtime_output" :key="index">
                    <p class="mb-0">{{ item }}</p>
                    </li>
                  </div>
                </div>
              </div>

              <div v-if="error" class="mt-4">
                <div class="alert alert-danger" role="alert">
                  <h5 class="alert-heading">Error</h5>
                  <p class="mb-0">{{ error }}</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="row justify-content-center mt-4 pb-4">
        <div class="col-md-12">
          <div class="card">
            <div class="card-body">
              <h5 class="card-title">About</h5>
              <p class="card-text">
                This is an experimental tool that checks a CSAF provider's metadata and documents for validity.
                It uses <a href="https://github.com/gocsaf/csaf/blob/main/docs/csaf_checker.md"><code>csaf_checker</code></a> of the gocsaf toolsuite under the hood.
              </p>
              <p>
                <a href="https://github.com/csaf-tools/provider-online-check/" target="_blank">
                  Website and Source Code
                </a>
                &nbsp;
                <a :href="apiDocsUrl" target="_blank">
                  API Documentation
                </a>
              </p>
              <p v-if="footerText" v-html="footerText"></p>
              <VersionDisplay :checkerVersion="version?.csaf_checker_version"
                                  :provider-version="version?.csaf_provider_version"
                                  :validator-version="version?.csaf_validator_version"
                />
            </div>
          </div>
        </div>
    </div>
    </div>
  </div>
</template>

<script lang="ts">
import axios from 'axios'
import { defineComponent } from 'vue'
import MessageLine from './MessageLine.vue'
import VersionDisplay from './VersionDisplay.vue';

interface ResultCheckerData {
  domains: {
    requirements: {num: number, messages: {text: string, type: number}[]}[],
    passed: boolean;
    role: string;
  }[];
  date: string;
}

interface AppData {
  session_id: string;
  domain: string;
  loading: boolean;
  initializedListeners: boolean;
  result: any;
  error: any;
  messagesList: null | MessageData[];
  scanTime: null | string;
  passed: boolean;
  role: string | null;
  isShowAllMessages: boolean;
  isShowResultOutput: boolean;
  isShowLogOutput: boolean;
  version: {
    csaf_checker_version: string;
    csaf_validator_version: string;
    csaf_provider_version: string;
  } | null
}

interface MessageData {
  text: string;
  type: number;
  num: number;
}

export default defineComponent({
  name: 'App',
  components: { MessageLine, VersionDisplay },
  data() {
    return {
      session_id: '1',
      domain: '',
      loading: false,
      initializedListeners: false,
      result: null,
      error: null,
      messagesList: null,
      scanTime: null,
      passed: false,
      role: null,
      version: null,
      isShowAllMessages: false,
      isShowResultOutput: false,
      isShowLogOutput: false
    } as AppData
  },
  async mounted() {
    axios
      .get(`${this.backendUrl}/api/information/`)
      .then(response => this.version = response.data)
  },
  computed: {
    resultClass() {
      switch(this.result?.status) {
        case 'ERROR':
          return 'alert-danger'
        case 'UNDEFINED':
          return 'alert-danger'
        case 'DONE_CHECKER':
          return 'alert-success'
        case 'CACHED_CHECKER':
          return 'alert-success'
        default:
          return 'alert-info'
      }
    },
    backendUrl() {
      // Use the same protocol and host as the client, but with backend port
      const protocol = window.location.protocol
      const hostname = window.location.hostname
      const backendPort = import.meta.env.VITE_BACKEND_PORT || 48090
      return `${protocol}//${hostname}:${backendPort}`
    },
    apiDocsUrl() {
      return `${this.backendUrl}/api/docs`
    },
    footerText() {
      return import.meta.env.VITE_FOOTER_TEXT || ''
    },
    trustedProviderMessages() {
      if (this.messagesList) {
        const trustedProviderMessages = []

        // requirements 1 (Valid CSAF document), 2 (Filename), 3 (TLS), 4 (TLP:WHITE)
        // Show all messages
        trustedProviderMessages.push(...this.filterMessageListByNums([1, 2, 3, 4]))

        // requirements 5 (TLP:AMBER and TLP:RED), 6 (Redirects) and 7 (provider-metadata.json)
        // Show all messages
        trustedProviderMessages.push(...this.filterMessageListByNums([5, 6, 7]))

        // requirements min one of 8 (security.txt), 9 (Well-known URL for provider-metadata.json), 10 (DNS path)
        // One must succeed, then show that message, else show all messages
        const req8Messages = this.filterMessageListByNums([8])
        const req9Messages = this.filterMessageListByNums([9])
        const req10Messages = this.filterMessageListByNums([10])
        if (req8Messages.length > 0  && req8Messages.filter((msg:MessageData) => msg.type === 2).length === 0) {
          trustedProviderMessages.push(...req8Messages)
        } else if (req9Messages.length > 0  && req9Messages.filter((msg:MessageData) => msg.type === 2).length === 0) {
          trustedProviderMessages.push(...req9Messages)
        } else if (req10Messages.length > 0  && req10Messages.filter((msg:MessageData) => msg.type === 2).length === 0) {
          trustedProviderMessages.push(...req10Messages)
        } else {
          trustedProviderMessages.push(...req8Messages, ...req9Messages, ...req10Messages)
        }

        // requirements dir based 11 (One folder per year), 12 (index.txt), 13 (changes.csv), 14 (Directory listings)
        //           or ROLIE based 15 (ROLIE feed), 16 (ROLIE service document), 17 (ROLIE category document)
        // Show the dir-based messages or show the ROLIE based messages
        const dirBaseMessages = this.filterMessageListByNums([11, 12, 13, 14])
        const rolieBaseMessages = this.filterMessageListByNums([15, 16, 17])
        if (rolieBaseMessages.filter((msg:MessageData) => msg.type === 2).length
            <= dirBaseMessages.filter((msg: MessageData) => msg.type === 2).length) {
          trustedProviderMessages.push(...rolieBaseMessages)
        } else {
          trustedProviderMessages.push(...dirBaseMessages)
        }

        // requirements 18 (Integrity), 19 (Signatures), 20 (Public OpenPGP Key)
        // Show all messages
        trustedProviderMessages.push(...this.filterMessageListByNums([18, 19, 20]))
        return trustedProviderMessages
      }
      return null
    },
    trustedProviderStatus() {
      return this.passed ? 'text-green': 'text-red'
    },
    displayAllMessagesTitle(): string {
      return this.isShowAllMessages ? 'Hide all messages' : 'Show all messages'
    },
    displayResultOutputTitle(): string {
      return this.isShowResultOutput ? 'Hide JSON output' : 'Show JSON output'
    },
    displayLogOutputTitle(): string {
      return this.isShowLogOutput ? 'Hide log output' : 'Show log output'
    }
  },
  methods: {
    async startScan() {
      this.loading = true
      this.result = null
      this.error = null
      this.clearFields()

      try {
        const response = await axios.post(`${this.backendUrl}/api/scan/start`, {
          domain: this.domain,
          session_id: this.session_id
        })
        this.result = response.data
        if (['DONE_CHECKER', 'CACHED_CHECKER'].includes(this.result?.status)) {
          const parsedResultsChecker = this.parseResultsChecker(this.result.results_checker)
          this.extractMessagesFromResultsChecker(parsedResultsChecker)
          this.setScanTime(parsedResultsChecker)
          this.setPassed(parsedResultsChecker)
          this.setRole(parsedResultsChecker)
          if (!this.initializedListeners) {
            setTimeout(() => {
              this.initializeListeners()
            })
          }
        } else {
          this.clearFields()
        }
      } catch (err: any) {
        this.clearFields()
        this.error = err.response?.data?.detail || err.message || 'An error occurred while starting the scan'
        if (err.response?.data?.detail[0]?.msg) {
          this.error = `${err.response?.data?.detail[0]?.input}: ${err.response?.data?.detail[0]?.msg}`
        }
      } finally {
        if (['INITIALIZED', 'RUNNING_CHECKER'].includes(this.result?.status) ) {
          setTimeout(this.startScan, 3000)
        } else {
          this.loading = false
        }
      }
    },
    clearFields() {
      this.messagesList = null
      this.scanTime = null
      this.passed = false
    },
    parseResultsChecker(results_checker: string): ResultCheckerData {
      return JSON.parse(results_checker)
    },
    setScanTime(parsedResultsChecker: ResultCheckerData) {
      if (parsedResultsChecker?.date) {
        this.scanTime = new Date(parsedResultsChecker?.date).toLocaleString(undefined, { timeZoneName: 'short' })
      }
    },
    setPassed(parsedResultsChecker: ResultCheckerData) {
      this.passed = parsedResultsChecker?.domains?.[0]?.passed ?? false;
    },
    setRole(parsedResultsChecker: ResultCheckerData) {
      this.role = parsedResultsChecker?.domains?.[0]?.role ?? "Unknown Role";
      this.role = this.role.replace('csaf', 'CSAF').replaceAll('_', ' ');
      this.role = this.role.replace(/\b\w/g, (c: string) => c.toUpperCase());
    },
    initializeListeners() {
      const allMessagesRef = this.$refs.allMessagesRef as HTMLElement
      allMessagesRef?.addEventListener('show.bs.collapse', () => { this.isShowAllMessages = true })
      allMessagesRef?.addEventListener('hide.bs.collapse', () => { this.isShowAllMessages = false })
      const resultOutputRef = this.$refs.resultOutputRef as HTMLElement
      resultOutputRef?.addEventListener('show.bs.collapse', () => { this.isShowResultOutput = true })
      resultOutputRef?.addEventListener('hide.bs.collapse', () => { this.isShowResultOutput = false })
      const logOutputRef = this.$refs.logOutputRef as HTMLElement
      logOutputRef?.addEventListener('show.bs.collapse', () => { this.isShowLogOutput = true })
      logOutputRef?.addEventListener('hide.bs.collapse', () => { this.isShowLogOutput = false })
      this.initializedListeners = true
    },
    extractMessagesFromResultsChecker(results_checker: ResultCheckerData) {
      if (results_checker.domains?.[0]?.requirements) {
        this.extractMessages(results_checker.domains[0].requirements)
      } else {
        this.messagesList = null
      }
    },
    extractMessages(requirements: {num: number, messages: {text: string, type: number}[]}[]) {
      this.messagesList = []
      for (const req of requirements) {
        for (const msg2 of req.messages ?? []) {
          this.messagesList.push({type: msg2.type, text: msg2.text, num: req.num })
        }
      }
    },
    filterMessageListByNums(nums: number[]): MessageData[] {
      return this.messagesList?.filter((msg: MessageData) => nums.includes(msg.num)) ?? []
    },
    copyToClipboard(text: string) {
      if (navigator.clipboard) {
        // This is the "normal" modern method, but does not work with HTTP (development setups)
        navigator.clipboard.writeText(text)
      } else {
        // Fallback to old method for development setups using HTTP
        const el = document.createElement('textarea')
        el.value = text
        document.body.appendChild(el)
        el.select()
        document.execCommand('copy')
        document.body.removeChild(el)
      }
    },
    copyResultToClipboard() {
      // results_checker is a string (not a JSON object), pass it directly
      this.copyToClipboard(this.result?.results_checker ?? '')
    },
    copyLogToClipboard() {
      // runtime_output is a list, join it by newlines
      this.copyToClipboard(this.result?.runtime_output?.join('\n') ?? '')
    },
    downloadJson() {
      const blob = new Blob([this.result?.results_checker ?? ''], { type: 'application/json' })
      const a = document.createElement('a')
      a.href = URL.createObjectURL(blob)
      a.download = `${this.domain}-result.json`
      a.click()
      URL.revokeObjectURL(a.href)
    },
    downloadLog() {
      const blob = new Blob([this.result?.runtime_output?.join('\n') ?? ''], { type: 'text/plain' })
      const a = document.createElement('a')
      a.href = URL.createObjectURL(blob)
      a.download = `${this.domain}-log.txt`
      a.click()
      URL.revokeObjectURL(a.href)
    },
    formatTime(ts: number) {
      return new Date(ts * 1000).toLocaleString()
    }
  }
})
</script>

<style scoped>
  #app {
    background-color: #f1f1f1;
    /* from csaf.io without the external "Darker Grotesque" */
    font-family: Arial, Helvetica, sans-serif;
    min-height: 100vh;
  }
.text-green {
  color: var(--bs-success);
}
.text-red {
  color: var(--bs-danger);
}
.small-margin-top {
  margin-top: 15px;
}
.log-header {
  margin-top: 7px;
}
.medium-font-size {
  font-size: 1.3rem;
}
.log-card-size {
  max-height: 510px;
}
</style>
