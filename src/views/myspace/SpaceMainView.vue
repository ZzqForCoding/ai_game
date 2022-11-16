<template>
    <el-row style="margin-top: 40px;">
        <el-col :span="5" :offset="2">
            <ProfileCard :info="spacePlayerInfo" />
        </el-col>
        <el-col :span="14" :offset="1">
            <el-tabs class="tabs" type="border-card">
                <el-tab-pane label="Bots" v-if="$store.state.user.id === userId">
                    <UserBotIndexView :userId="userId" />
                </el-tab-pane>
                <el-tab-pane label="录像">
                    <RecordList :recordListUrl="'https://aigame.zzqahm.top/backend/record/getlist/' + userId + '/'" />
                </el-tab-pane>
                <el-tab-pane label="动态">
                    有什么新鲜事想告诉大家！快去发帖吧！
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
import { useRoute } from 'vue-router';
import { onMounted, reactive } from 'vue';
import $ from 'jquery';
import { useStore } from 'vuex'; 

export default {
    name: 'SpaceMainView',
    components: {
        UserBotIndexView,
        RecordList,
        ProfileCard,
    },
    setup() {
        const store = useStore();
        const route = useRoute();
        const userId = parseInt(route.params.userId);
        const spacePlayerInfo = reactive({
            'name': '',
            'photo': '',
            'job': '',
            'desp': ''
        });

        const getSpacePlayerInfo = () => {
            $.ajax({
                url: "https://aigame.zzqahm.top/backend/player/getinfo/" + userId + "/",
                type: "get",
                headers: {
                    "Authorization": "Bearer " + store.state.user.access,
                },
                success(resp) {
                    if(resp.result === "success") {
                        spacePlayerInfo.username = resp.player_info.username;
                        spacePlayerInfo.photo = resp.player_info.photo;
                        spacePlayerInfo.job = resp.player_info.job;
                        spacePlayerInfo.desp = resp.player_info.desp;
                   }
                },
                error() {
                    store.dispatch("logout");
                }
            });
        }

        onMounted(() => {
    getSpacePlayerInfo();
        });
 
        return {
            userId,
            spacePlayerInfo,
        }
     }
}
</script>

<style scoped>

</style>