<template>
    <div class="box-layout">
        <div v-show="providerVersion">CSAF Provider</div><div class="align-right">{{ providerVersion }}</div>
        <div v-show="checkerVersion">CSAF Checker</div><div class="align-right">{{ checkerVersion }}</div>
        <div v-show="validatorVersion">CSAF Validator</div><div class="align-right">{{ validatorVersion }}</div>
    </div>
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

<style scoped>
.box-layout {
    display: grid;
    grid-template-columns: 120px 40px;
}
.align-right {
    justify-self: end;
}

</style>