<template>
    <el-row>
        <el-col :span="14" :offset="2">
            <PlayGround :game="game" flag="record" />
        </el-col>
        
        <el-col :span="5" :offset="1" style="margin-top: 40px;">
        </el-col>
    </el-row>
</template>

<script>
import PlayGround from '@/components/PlayGround.vue';
import { useRoute } from 'vue-router';

export default {
    components: {
        PlayGround,
    },
    setup() {
        const route = useRoute();
        const game = parseInt(route.params.game);

        return {
            game,
        }
    }
}
</script>

<style scoped>
</style>