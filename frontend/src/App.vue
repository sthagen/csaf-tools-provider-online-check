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
                </div>

                <button
                  type="submit"
                  class="btn btn-primary"
                  :disabled="loading"
                >
                  <span v-if="loading" class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
                  {{ result ? 'Update' : 'Start Scan' }}
                </button>
              </form>

              <!--- display of requirements messages -->
              <div v-if="messagesList" class="mt-4">
                <div v-if="result?.status === 'DONE_CHECKER'">
                  <h5 class="alert-heading">Scan Done</h5>
                </div>
                <div v-else-if="result?.status === 'CACHED_CHECKER'">
                  <h5 class="alert-heading">Scan found in cache</h5>
                </div>
                <div v-for="item of messagesList" :class="messageClass(item)">
                  {{ item.text }}
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
                    <h5 class="alert-heading">Scan started. Please click Update</h5>
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

interface ImportMeta {
  env: {VITE_BACKEND_PORT: number, VITE_FOOTER_TEXT: string};
}

interface AppData {
  session_id: string;
  domain: string;
  loading: boolean;
  result: any;
  error: any;
  messagesList: any;
}

export default defineComponent({
  name: 'App',
  data() {
    return {
      session_id: '1',
      domain: '',
      loading: false,
      result: null,
      error: null,
      messagesList: null
    } as AppData
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
      const backendPort = (import.meta as unknown as ImportMeta).env.VITE_BACKEND_PORT || 48090
      return `${protocol}//${hostname}:${backendPort}`
    },
    apiDocsUrl() {
      return `${this.backendUrl}/api/docs`
    },
    footerText() {
      return (import.meta as unknown as ImportMeta).env.VITE_FOOTER_TEXT || ''
    }
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
        this.error = err.response?.data?.detail || err.message || 'An error occurred while starting the scan'
      } finally {
        this.loading = false
      }
    },
    messageClass(item: { type: number}) {
      switch (item.type) {
        case 0:
          return 'text-green'
        case 1:
          return 'text-orange'
        case 2:
          return 'text-red'
        default:
          return ''
      }
    },
    extractMessagesFromResultsChecker(results_checker: any) {
      if (typeof results_checker === 'string') {
        results_checker = JSON.parse(results_checker)
      }
      if (results_checker.domains.length) {
        this.extractMessages(results_checker.domains[0].requirements)
      }
    },
    extractMessages(requirements: {messages: {text: string, type: number}[]}[]) {
      this.messagesList = []
      for (const req of requirements) {
        for (const msg2 of req.messages) {
          this.messagesList.push(msg2)
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

  .text-green {
    color: green;
  }

  .text-orange {
    color: orange;
  }

  .text-red {
    color: red;
  }
}
</style>
