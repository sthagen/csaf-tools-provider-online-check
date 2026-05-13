<template>
  <div id="app">
    <nav class="navbar navbar-dark bg-dark">
      <div class="container-fluid">
        <span class="navbar-brand mb-0 h1">CSAF Provider Scan <span class="badge bg-warning text-dark ms-2">Beta</span></span>
      </div>
    </nav>

    <div class="container mt-5">
      <div class="row justify-content-center">
        <div class="col-md-8">
          <div class="card shadow">
            <div class="card-body">
              <h2 class="card-title mb-4">Scan a Domain <span class="badge bg-warning ms-2" style="font-size: 0.4em; vertical-align: middle;">Experimental</span></h2>

              <form @submit.prevent="startScan">
                <div class="mb-3">
                  <label for="domainInput" class="form-label">Domain</label>
                  <input
                    type="text"
                    class="form-control"
                    id="domainInput"
                    v-model="domain"
                    placeholder="example.com"
                    required
                  >
                  <div class="form-text">Enter a domain to scan a CSAF provider</div>
                  <VersionDisplay :checkerVersion="version?.csaf_checker_version"
                                  :provider-version="version?.csaf_provider_version"
                                  :validator-version="version?.csaf_validator_version"
                  />
                </div>

                <button
                  type="submit"
                  class="btn btn-primary"
                  :disabled="loading"
                >
                  <span v-if="loading" class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
                  <span v-else>{{ 'Start Scan' }}</span>
                </button>
              </form>

              <!-- display of requirements messages -->
              <div v-if="messagesList" class="mt-4">
                <div v-if="result?.status === 'DONE_CHECKER'">
                  <h5 class="alert-heading">Scan Done</h5>
                </div>
                <div v-else-if="result?.status === 'CACHED_CHECKER'">
                  <h5 class="alert-heading">Scan found in cache</h5>
                </div>
                
                <h6 :class="publisherStatus" class="small-margin-top">CSAF publisher</h6>
                <Message v-for="item of publisherMessages" :text="item.text" :type="item.type"></Message> 
                
                <h6 :class="providerStatus" class="small-margin-top">CSAF provider</h6>
                <Message v-for="item of providerMessages" :text="item.text" :type="item.type"></Message> 
                
                <h6 :class="trustedProviderStatus" class="small-margin-top">CSAF trusted provider</h6>
                <Message v-for="item of trustedProviderMessages" :text="item.text" :type="item.type"></Message> 

                <h6 class="small-margin-top">All messages</h6>
                <Message v-for="item of messagesList" :text="item.text" :type="item.type"></Message>
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
                    <h5 class="alert-heading">Scan started...</h5>
                    <pre>{{ result.results_checker }}</pre>
                  </div>
                  <div v-if="result.status === 'RUNNING_CHECKER'">
                    <h5 class="alert-heading">Scan Running...</h5>
                    <pre>{{ result.results_checker }}</pre>
                  </div>
                  <div v-if="result.status === 'PAUSED'">
                    <h5 class="alert-heading">Scan paused</h5>
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

      <div class="row justify-content-center mt-4">
        <div class="col-md-8">
          <div class="card">
            <div class="card-body">
              <h5 class="card-title">About</h5>
              <p class="card-text">
                This is an experimental tool that scans domains for <a href="https://www.csaf.io" target="_blank">CSAF</a> (Common Security Advisory Framework)
                provider metadata and checks its validity. Results may vary.
              </p>
              <p>
                <a href="https://github.com/Intevation/csaf-provider-scan/" target="_blank">
                  Website and Source Code
                </a>
                &nbsp;
                <a :href="apiDocsUrl" target="_blank">
                  API Documentation
                </a>
              </p>
              <p v-if="footerText" v-html="footerText"></p>
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
import Message from './Message.vue'
import VersionDisplay from './VersionDisplay.vue';

interface AppData {
  session_id: string;
  domain: string;
  loading: boolean;
  result: any;
  error: any;
  messagesList: any;
  version: {
    csaf_checker_version: string;
    csaf_validator_version: string;
    csaf_provider_version: string;
  } | null
}

export default defineComponent({
  name: 'App',
  components: { Message, VersionDisplay },
  data() {
    return {
      session_id: '1',
      domain: '',
      loading: false,
      result: null,
      error: null,
      messagesList: null,
      version: null
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
    publisherMessages() {
      if (this.messagesList) {
        return this.messagesList.filter(msg => [1, 2, 3, 4].includes(msg.num))
      }
      return null
    },
    publisherStatus() {
      if (this.publisherMessages) {
        return this.publisherMessages.filter(msg => msg.type === 2).length === 0 ? 'text-green' : 'text-red'
      }
      return 'text-red'
    },
    providerMessages() {
      if (this.messagesList) {
        const providerMessages = []
        providerMessages.push(
          this.publisherStatus === 'text-green'
            ? {text: 'Is a valid CSAF publisher', type: 0 }
            : {text: 'Is not a valid CSAF publisher', type: 2 }
        )
        providerMessages.push(...(this.messagesList.filter(msg => [5, 6, 7].includes(msg.num))))
        const dirBaseMessages = this.messagesList.filter(msg => [11,12,13,14].includes(msg.num))
        const rolieBaseMessages = this.messagesList.filter(msg => [15,16,17].includes(msg.num))
        if (rolieBaseMessages.filter(msg => msg.type === 2).length <= dirBaseMessages.filter(msg => msg.type === 2).length) {
          providerMessages.push(...rolieBaseMessages)
        } else {
          providerMessages.push(...dirBaseMessages)
        }
        return providerMessages
      }
      return null
    },
    providerStatus() {
      if (this.providerMessages) {
        return this.providerMessages.filter(msg => msg.type === 2).length === 0 ? 'text-green' : 'text-red'
      }
      return 'text-red'
    },
    trustedProviderMessages() {
      if (this.messagesList) {
        const trustedProviderMessages = []
        trustedProviderMessages.push(
          this.providerStatus === 'text-green' ? {text: 'Is valid CSAF provider', type: 0 }
                                              : {text: 'Is not a valid CSAF provider', type: 2})
        const filtered = this.messagesList.filter(msg => [18,19,20].includes(msg.num))
        trustedProviderMessages.push(...filtered)
        return trustedProviderMessages
      }
      return null
    },
    trustedProviderStatus() {
      if (this.trustedProviderMessages) {
        return this.trustedProviderMessages.filter(msg => msg.type === 2).length === 0 ? 'text-green' : 'text-red'
      }
      return 'text-red'
    },
  },
  methods: {
    async startScan() {
      this.loading = true
      this.result = null
      this.error = null

      try {
        const response = await axios.post(`${this.backendUrl}/api/scan/start`, {
          domain: this.domain,
          session_id: this.session_id
        })
        this.result = response.data
        if (['DONE_CHECKER', 'CACHED_CHECKER'].includes(this.result?.status)) {
          this.extractMessagesFromResultsChecker(this.result.results_checker)
        } else {
          this.messagesList = null
        }
      } catch (err: any) {
        this.messagesList = null
        this.error = err.response?.data?.detail || err.message || 'An error occurred while starting the scan'
      } finally {
        if (['INITIALIZED', 'RUNNING_CHECKER'].includes(this.result?.status) ) {
          setTimeout(this.startScan, 3000)
        } else {
          this.loading = false
        }
      }
    },
    extractMessagesFromResultsChecker(results_checker: any) {
      if (typeof results_checker === 'string') {
        results_checker = JSON.parse(results_checker)
      }
      if (results_checker.domains?.[0]?.requirements) {
        this.extractMessages(results_checker.domains[0].requirements)
      } else {
        this.messagesList = null
      }
    },
    extractMessages(requirements: {messages: {text: string, type: number}[]}[]) {
      this.messagesList = []
      for (const req of requirements) {
        for (const msg2 of req.messages ?? []) {
          this.messagesList.push({type: msg2.type, text: msg2.text, num: req.num })
        }
      }
    }
  }
})
</script>

<style scoped>
#app {
  min-height: 100vh;
  background-color: #f8f9fa;
}
.text-green {
  color: green;
}
.text-red {
  color: red;
}
.small-margin-top {
  margin-top: 15px;
}
</style>
