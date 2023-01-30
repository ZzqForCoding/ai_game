<template>
    <!-- 个人信息 -->
    <el-card class="profile-card" shadow="always">
        <div class="background">
        </div>
        <div class="content">
            <el-row>
                <el-col :span="6" :offset="9">
                    <div class="photo">
                        <img v-if="info.photo !== ''" :src="info.photo" alt="" class="" style="user-select: none;">
                        <img v-else src="@/assets/images/loading.svg" alt="" style="user-select: none; background-color: white;">
                    </div>
                </el-col>
            </el-row>
            <el-row>
                <el-col :span="20" :offset="2">
                    <div class="username">
                        {{ info.username }}
                    </div>

                    <div class="profession">
                        <span>job：</span>
                        {{ info.job }}
                        <span v-if="!info.job || info.job.trim() === ''">-</span>
                    </div>

                    <div class="description">
                        <span>mood：</span>
                        {{ info.desp }}
                        <span v-if="!info.desp || info.desp.trim() === ''">-</span>
                    </div>

                    <div class="friend-num-container">
                        <div class="infoSelect" @click="switchPannel('bots')">
                            <h6 class="num">{{ info.botCnt }}</h6>
                            <small class="text">Bots</small>
                        </div>
                        <div class="vertical-divider"></div>
                        <div class="infoSelect" @click="switchPannel('records')">
                            <h6 class="num">{{ info.recordCnt }}</h6>
                            <small class="text">Records</small>
                        </div>
                        <div class="vertical-divider"></div>
                        <div class="infoSelect" @click="switchPannel('freshnews')">
                            <h6 class="num">{{ info.freshNewsCnt }}</h6>
                            <small class="text">Post</small>
                        </div>
                    </div>

                    <div class="horizontal-divider"></div>
                </el-col>
            </el-row>
        </div>
    </el-card>
</template>

<script>
import { useStore } from 'vuex'; 
import { ElMessage } from 'element-plus';
import { useRoute } from 'vue-router';
import router from '@/router';

export default {
    name: 'ProfileCard',
    props: {
        info: {
            type: Object,
            required: true
        }
    },
    setup(props, context) {
        const store = useStore();
        const route = useRoute();
        const switchPannel = name => {
            if(props.info.id !== store.state.user.id && name === "bots") {
                ElMessage.error("别人的代码不能查看哦!~");
                return;
            }
            if(route.name !== "myspace_index") {
                router.push(
                    {
                        name: "myspace_index",
                        params: {
                            userId: props.info.id,
                        }
                    }
                );
            }
            context.emit("switchPannel", name);
        }

        return {
            switchPannel,
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
    margin-top: 5px;
    user-select: text;
}

.profile-card .profession {
    margin-top: 15px;
    color: #676A79;
    font-size: 12px;
    text-align: center;
}

.profile-card .description {
    color: #676A79;
    font-size: 13px;
    text-align: center;
    width: 90%;
    margin: 30px auto;
    height: 50px;
    word-break: break-word;
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

.profile-card .friend-num-container .infoSelect {
    user-select: none;
}

.profile-card .friend-num-container .infoSelect:hover {
    transform: scale(1.2);
    cursor: pointer;
    transition: 100ms;
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