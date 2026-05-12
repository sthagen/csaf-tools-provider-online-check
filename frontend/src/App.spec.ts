import { beforeEach, describe, expect, test, vi } from 'vitest'
import { flushPromises, mount } from '@vue/test-utils'
import App from './App.vue'
import axios from 'axios'

describe("Testing App...", () => {

    let app: any
    beforeEach(()=> {
        app = mount(App)
    })

    test('messageClass', () => {
        expect(app.vm.messageClass({type: 0})).toBe('text-green')
        expect(app.vm.messageClass({type: 1})).toBe('text-orange')
        expect(app.vm.messageClass({type: 2})).toBe('text-red')
        expect(app.vm.messageClass({type: -1})).toBe('')
    }),
    test('extractMessages', () => {
        app.vm.extractMessages([{ messages: [{text: "Test1", type: 0}]}])
        expect(app.vm.messagesList).toStrictEqual([{text: "Test1", type: 0}])
        app.vm.extractMessages([{messages: undefined}])
        expect(app.vm.messagesList).toStrictEqual([])
    }),
    test('extractMessagesFromResultsChecker with json string', () =>{
        app.vm.extractMessagesFromResultsChecker(
            '{ "domains": [{"requirements": [{ "messages": [{"text": "Test1", "type": 0}]}]}]}'
        )
        expect(app.vm.messagesList).toStrictEqual([{text: "Test1", type: 0}])
    }),
    test('extractMessagesFromResultsChecker with requirements null', () => {
        app.vm.extractMessagesFromResultsChecker(
            '{ "domains": [{"requirements": null}]}'
        )
        expect(app.vm.messagesList).toBe(null)
    }),
    test('extractMessagesFromResultsChecker with object', () => {
        app.vm.extractMessagesFromResultsChecker(
            { "domains": [{"requirements": [{ "messages": [{"text": "Test1", "type": 0}]}]}]}
        )
        expect(app.vm.messagesList).toStrictEqual([{text: "Test1", type: 0}])
    }),
    test('resultClass', () => {
        const test_oracle = [
            ['ERROR', 'alert-danger'],
            ['UNDEFINED', 'alert-danger'],
            ['DONE_CHECKER', 'alert-success'],
            ['CACHED_CHECKER', 'alert-success'],
            ['DEFAULT', 'alert-info']                    
        ]
        for (const pair of test_oracle) {
            app.vm.result = { 'status': pair[0]}
            expect(app.vm.resultClass).toBe(pair[1])
        }
    }),
    test('backendUrl and apiDocsUrl', () => {
        const protocol = window.location.protocol
        const hostname = window.location.hostname
        vi.stubEnv('VITE_BACKEND_PORT', undefined)
        app = mount(App)
        expect(app.vm.backendUrl).toBe(`${protocol}//${hostname}:48090`)
        expect(app.vm.apiDocsUrl).toBe(`${protocol}//${hostname}:48090/api/docs`)
        vi.stubEnv('VITE_BACKEND_PORT', 33333)
        app = mount(App)
        expect(app.vm.backendUrl).toBe(`${protocol}//${hostname}:33333`)
        expect(app.vm.apiDocsUrl).toBe(`${protocol}//${hostname}:33333/api/docs`)

    }),
    test('footerText empty', () => {
        vi.stubEnv('VITE_FOOTER_TEXT', 'FooterTest1')
        app = mount(App)
        expect(app.vm.footerText).toBe('FooterTest1')
        vi.stubEnv('VITE_FOOTER_TEXT', undefined)
        app = mount(App)
        expect(app.vm.footerText).toBe('')

    }),
    test('startScan RUNNING', async () => {
        vi.spyOn(axios, 'post').mockImplementation(() => { return {data: {status: "RUNNING" }}})
        app.vm.domain = "Test"
        app.vm.startScan()
        await flushPromises()
        expect(app.vm.loading).toBe(false)
        expect(app.vm.result?.status).toBe('RUNNING')
    }),
    test('startScan CACHED_CHECKER', async () => {
        vi.spyOn(axios, 'post').mockImplementation(() => { 
            return {data: {
                status: "CACHED_CHECKER",
                results_checker: { "domains": [{"requirements": [{ "messages": [{"text": "Test1", "type": 0}]}]}]}
            }}
        })
        app.vm.domain = "Test"
        app.vm.startScan()
        await flushPromises()
        expect(app.vm.loading).toBe(false)
        expect(app.vm.result?.status).toBe('CACHED_CHECKER')
        expect(app.vm.messagesList).toStrictEqual([{text: 'Test1', type: 0}])

    })

})
