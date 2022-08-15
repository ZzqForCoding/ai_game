<template>
    <div class="content-field">
        <el-row>
            <el-col :span="18" :offset="3">
                <el-card shadow="always" class="card">
                    <slot></slot>
                </el-card>
            </el-col>
        </el-row>
    </div>
</template>

<script>
    export default {
        name: 'ContentField',
    }
</script>

<style scoped>

div.content-field {
    margin-top: 40px;
}

.card {
    background-color: #FAFAFA;
}
</style>