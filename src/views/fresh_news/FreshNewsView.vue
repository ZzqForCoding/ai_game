<template>
    <el-row style="margin-top: 40px;">
        <el-col :span="5" :offset="2">
            <ProfileCard :info="playerInfo" />
        </el-col>
        <el-col :span="14" :offset="1">
            <FreshNewsList freshNewsUrl="https://aigame.zzqahm.top/backend/playervoice/freshnews/getlist/" showPostComment="true" />
        </el-col>
    </el-row>
</template>

<script>
import ProfileCard from '@/components/ProfileCard.vue';
import FreshNewsList from '@/components/FreshNewsList.vue';
import { reactive,watchEffect } from 'vue';
import { useStore } from 'vuex';

export default {
    name: 'FreshNewsView',
    components: {
        ProfileCard,
        FreshNewsList,
    },
    setup() {
        const store = useStore();
        const playerInfo = reactive({
            'id': store.state.user.id,
            'username': store.state.user.username,
            'photo': store.state.user.photo,
            'job': store.state.user.job,
            'desp': store.state.user.desp,
            'recordCnt': store.state.user.recordCnt,
            'botCnt': store.state.user.botCnt,
            'freshNewsCnt': store.state.user.freshNewsCnt,
        });
        
        watchEffect(()=>{
            playerInfo.freshNewsCnt = store.state.user.freshNewsCnt;
        });
        return {
            playerInfo,
        }
    }
}
 </script>

<style scoped>
</style>