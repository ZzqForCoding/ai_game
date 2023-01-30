<template>
    <el-row style="margin-top: 40px;">
        <el-col :span="16" :offset="4" style="margin-top: 20px;">
            <MDPreview :previewValue="previewValue" />
        </el-col>
    </el-row>
</template>

<script>
import MDPreview from '@/components/MDPreview.vue';
import { ref } from 'vue';

export default {
    name: 'FuncIntroView',
    components: {
        MDPreview,
    },
    setup() {
        let previewValue = ref('# 功能介绍');

        return {
            previewValue,
        }
    }
}
</script>

<style scoped>
</style>