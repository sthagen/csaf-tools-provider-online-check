/// <reference types="vite/client" />

interface ImportMetaEnv {
    readonly VITE_BACKEND_PORT: number
    readonly VITE_FOOTER_TEXT: string
}

interface ImportMeta {
    readonly env: ImportMetaEnv
}
