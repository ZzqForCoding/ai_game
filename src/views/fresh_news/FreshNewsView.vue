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
import { reactive } from 'vue';
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
            'username': store.state.user.username,
            'photo': store.state.user.photo,
            'job': store.state.user.job,
            'desp': store.state.user.desp
        });

        return {
            playerInfo,
        }
    }
}
 </script>

<style scoped>
</style>