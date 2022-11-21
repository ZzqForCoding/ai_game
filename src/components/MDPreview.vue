<template>
    <el-card shadow="always" class="preview-card">
        <el-alert title="欢迎来到 AIGame PlatForm ！你可以点击 首页 来选择你感兴趣游戏的进行游玩~" type="success" />
        <el-card shadow="always" class="card" style="margin-top: 30px;">
            <v-md-preview :text="previewValue" :include-level="[1, 2, 3, 4, 5, 6]" height="400px" />
        </el-card>
    </el-card>
</template>

<script>
export default {
    name: 'MDPreview',
    props: {
        previewValue: {
            type: String,
            required: true
        }
    },
}
</script>

<style scoped>
.preview-card:deep(.el-card) {
    border-radius: 25px;
}
</style>