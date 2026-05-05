<template>
    <div v-show="providerVersion">CSAF Provider {{ providerVersion }}</div>
    <div v-show="checkerVersion">CSAF Checker {{ checkerVersion }}</div>
    <div v-show="validatorVersion">CSAF Validator {{ validatorVersion }}</div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
    props: {
        providerVersion: String,
        checkerVersion: String,
        validatorVersion: String
    }
})
</script>

<style scoped></style>