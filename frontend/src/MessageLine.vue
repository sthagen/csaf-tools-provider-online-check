<template>
    <div class="small-bottom-margin">
        <span v-if="type === 2" :class="messageClass">ERROR</span>
        <span v-else-if="type === 1" :class="messageClass">WARN</span>
        <span v-else :class="messageClass">PASS</span>
        {{ text }}
    </div>
</template>
<script lang="ts">
import { defineComponent } from 'vue'
export default defineComponent({
    props: {
        type: Number,
        text: String
    },
    computed: {
        messageClass() {
            switch (this.type) {
                case 0:
                    return 'text-green'
                case 1:
                    return 'text-orange'
                case 2:
                    return 'text-red'
                default:
                    return ''
            }
        }
    }
})
</script>

<style scoped>

.text-green {
color: green;
}
.text-orange {
color: orange;
}
.text-red {
color: red;
}
.small-bottom-margin {
    margin-bottom: 12px;
}
</style>

