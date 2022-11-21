<template>
    <el-row style="margin-top: 40px;">
        <el-col :span="16" :offset="4" style="margin-top: 20px;">
            <MDPreview :previewValue="previewValue" />
        </el-col>
    </el-row>
</template>

<script>
import MDPreview from '@/components/MDPreview.vue';
import { ref, onMounted } from 'vue';
import { useStore } from 'vuex'; 


export default {
    name: 'GameIntroView',
    components: {
        MDPreview,
    },
    setup() {
        const store = useStore();
        let previewValue = ref('');

        onMounted(() => {
            store.dispatch("getGameIntro", {
                id: 10,
                success(resp) {
                    previewValue.value = resp.data.content; 
                }
            });
        });

        return {
            previewValue,
        }
    }
}
</script>

<style scoped>

</style>