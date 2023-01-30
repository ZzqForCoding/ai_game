<template>
    <el-row style="margin-top: 40px;">
        <el-col :span="5" :offset="2">
            <ProfileCard :info="spacePlayerInfo" @switchPannel="switchPannel" />
        </el-col>
        <el-col :span="14" :offset="1">
            <el-tabs class="tabs" type="border-card" v-model="pannelName">
                <el-tab-pane label="Bots" v-if="$store.state.user.id === userId" name="bots">
                    <UserBotIndexView :userId="userId" />
                </el-tab-pane>
                <el-tab-pane label="录像" name="records">
                    <RecordList :recordListUrl="'https://aigame.zzqahm.top/backend/record/getlist/' + userId + '/'" />
                </el-tab-pane>
                <el-tab-pane label="动态" name="freshnews">
                    <!-- 有什么新鲜事想告诉大家！快去发帖吧！ -->
                    <FreshNewsList
                        :freshNewsUrl="'https://aigame.zzqahm.top/backend/playervoice/freshnews/getlist/' + userId + '/'"
                        :showPostComment="false" />
                </el-tab-pane>
                <!-- <el-tab-pane label="发帖">
                    快去讨论讨论游戏叭！
                </el-tab-pane> -->
            </el-tabs>
        </el-col>
    </el-row>
</template>

<script>
import UserBotIndexView from '@/components/UserBotIndexView.vue';
import RecordList from '@/components/RecordList.vue';
import ProfileCard from '@/components/ProfileCard.vue';
import FreshNewsList from '@/components/FreshNewsList.vue';
import { useRoute } from 'vue-router';
import { onMounted, reactive, ref, watchEffect } from 'vue';
import $ from 'jquery';
import { useStore } from 'vuex';

export default {
    name: 'SpaceMainView',
    components: {
        UserBotIndexView,
        RecordList,
        ProfileCard,
        FreshNewsList,
    },
    setup() {
        const store = useStore();
        const route = useRoute();
        const userId = parseInt(route.params.userId);
        const spacePlayerInfo = reactive({
            'id': 0,
            'name': '',
            'photo': '',
            'job': '',
            'desp': '',
            'recordCnt': 0,
            'botCnt': 0,
            'freshNewsCnt': 0,
            'isSuperUser': false,
        });
        const pannelName = ref(null);

        
        
        watchEffect(()=>{
            spacePlayerInfo.botCnt = store.state.user.botCnt;
            spacePlayerInfo.recordCnt = store.state.user.recordCnt;
            spacePlayerInfo.freshNewsCnt = store.state.user.freshNewsCnt;
        });

        const getSpacePlayerInfo = () => {
            $.ajax({
                url: "https://aigame.zzqahm.top/backend/player/getinfo/" + userId + "/",
                type: "get",
                headers: {
                    "Authorization": "Bearer " + store.state.user.access,
                },
                success(resp) {
                    if (resp.result === "success") {
                        spacePlayerInfo.id = userId,
                        spacePlayerInfo.username = resp.player_info.username;
                        spacePlayerInfo.photo = resp.player_info.photo;
                        spacePlayerInfo.job = resp.player_info.job;
                        spacePlayerInfo.desp = resp.player_info.desp;
                        spacePlayerInfo.recordCnt = resp.player_info.recordCnt;
                        spacePlayerInfo.botCnt = resp.player_info.botCnt;
                        spacePlayerInfo.freshNewsCnt = resp.player_info.freshNewsCnt;
                        spacePlayerInfo.isSuperUser = resp.player_info.isSuperUser;

                        // 设置空间选择的pannel                        
                        if (spacePlayerInfo.id !== store.state.user.id) pannelName.value = "records";
                        else pannelName.value = "bots";
                    }
                },
                error() {
                    store.dispatch("logout");
                }
            });
        }

        const switchPannel = name => {
            pannelName.value = name;
        };

        onMounted(() => {
            getSpacePlayerInfo();
        });

        return {
            userId,
            spacePlayerInfo,
            pannelName,
            switchPannel,
        }
    }
}
</script>

<style scoped>

</style>