<template>
    <h6>Versions</h6>
    <div>CSAF Provider Scan beta1</div>
    <div v-show="checkerVersion">CSAF checker {{ checkerVersion }}</div>
    <div v-show="validatorVersion">CSAF validators {{ validatorVersion }}</div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
    props: {
        checkerVersion: String,
        validatorVersion: String
    }
})
</script>

<style scoped></style>