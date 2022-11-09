<template>
    <el-row style="margin-top: 40px;">
        <el-col :span="5" :offset="2">
            <!-- 个人信息 -->
            <el-card class="profile-card" shadow="always">
                <div class="background">
                </div>
                <div class="content">
                    <el-row>
                        <el-col :span="6" :offset="9">
                                <div class="photo">
                                    <img :src="spacePlayerInfo.photo" alt="" class="" style="user-select: none;">
                                </div>
                        </el-col>
                    </el-row>
                    <el-row>
                        <el-col :span="20" :offset="2">
                            <div class="username">
                                {{ spacePlayerInfo.username }}
                            </div>

                            <div class="profession">
                                Web Developer at Webestica
                            </div>

                            <div class="description">
                                I'd love to change the world, but they won’t give me the source code.
                            </div>

                            <div class="friend-num-container">
                                <div>
                                    <h6 class="num">256</h6>
                                    <small class="text">Post</small>
                                </div>
                                <div class="vertical-divider"></div>
                                <div>
                                    <h6 class="num">2.5K</h6>
                                    <small class="text">Followers</small>
                                </div>
                                <div class="vertical-divider"></div>
                                <div>
                                    <h6 class="num">365</h6>
                                    <small class="text">Records</small>
                                </div>
                            </div>

                            <div class="horizontal-divider"></div>
                        </el-col>
                    </el-row>
                </div>
            </el-card>
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
import { useRoute } from 'vue-router';
import { onMounted, reactive } from 'vue';
import $ from 'jquery';
import { useStore } from 'vuex'; 

export default {
    name: 'SpaceMainView',
    components: {
        UserBotIndexView,
        RecordList,
    },
    setup() {
        const route = useRoute();
        const userId = parseInt(route.params.userId);
        const spacePlayerInfo = reactive({
            'name': '',
            'photo': '',
        });
        const store = useStore();

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
                        console.log(spacePlayerInfo)
                    }
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
.el-card:deep(.el-card__body)  {
    padding: 0 0 !important;
}

.profile-card {
    border: none !important;
}
    
.profile-card .background {
    background-image: url('@/assets/images/01.jpg');
    background-position: center;
    background-size: cover;
    background-repeat: no-repeat;
    height: 50px;
}

.profile-card .photo > img {
    margin-top: -40px;
    border-radius: 10px 10px 0 0;
    border: 3px solid white;
    width: 100%;
    height: 100%;
}

.profile-card .username {
    text-align: center;
    font-size: 20px;
    font-weight: 700;
    height: 20px;
    line-height: 20px;
    margin-top: 18px;
    user-select: text;
}

.profile-card .profession {
    margin-top: 5px;
    color: #676A79;
    font-size: 12px;
    text-align: center;
}

.profile-card .description {
    color: #676A79;
    font-size: 13px;
    text-align: center;
    width: 90%;
    margin: 15px auto;
}

.profile-card .friend-num-container {
    display: flex;
    justify-content: space-between;
}

.profile-card .friend-num-container div:nth-child(1) {
    margin-left: 10px;
}

.profile-card .friend-num-container div:last-child {
    margin-right: 10px;
}

.profile-card .friend-num-container .num {
    text-align: center;
    height: 12px !important;
    line-height: 12px !important;
    margin-bottom: 0px;
}

.profile-card .friend-num-container .text {
    font-size: 8px;
    color: #676A79;
    user-select: none;
}

.profile-card .vertical-divider {
    height: 40px;
    border-left: 1px solid #CCCCCC;
    margin: 0 5px;
    padding: 8px 0;
}

.profile-card .horizontal-divider {
    width: 100%;
    border-top: 1px solid #CCCCCC;
    margin: 10px 0px;
    padding: 0 10px;
    margin-bottom: 15px;
}
</style>