<template>
    <div :class="messageClass">
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
</style>

