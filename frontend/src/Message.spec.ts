import { beforeEach, describe, expect, test } from 'vitest'
import { mount } from '@vue/test-utils'
import Message from './Message.vue'

describe("Testing Message...", () => {
    let message: any
    beforeEach(()=> {
        message = mount(Message , {props: { type: 0}})
    })
    test('messageClass', () => {
        expect(message.vm.messageClass).toBe('text-green')
        message = mount(Message , {props: { type: 1 }})
        expect(message.vm.messageClass).toBe('text-orange') 
        message = mount(Message , {props: { type: 2 }})
        expect(message.vm.messageClass).toBe('text-red')
        message = mount(Message , {props: { type: -1 }})
        expect(message.vm.messageClass).toBe('')
    })
})
