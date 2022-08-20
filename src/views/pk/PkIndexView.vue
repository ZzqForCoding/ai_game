<template>
    <el-row>
        <el-col :span="14" :offset="2">
            <PlayGround :game="game" v-if="$store.state.pk.status === 'playing'" />
            <MatchGround v-if="$store.state.pk.status === 'matching'" />
        </el-col>
        
        <el-col :span="5" :offset="1" style="margin-top: 40px;">
            <el-card class="message">
                <template #header>
                  <div class="card-header">
                    <span>公共聊天区</span>
                  </div>
                </template>
                
                <el-card class="message-content" shadow="never">
                    <el-scrollbar max-height="320px">
                        <div class="message-container">
                            <div class="username">
                                zzq
                            </div>
                            <div class="main">
                                <el-avatar class="phone" size="small" src="https://cdn.acwing.com/media/user/profile/photo/29231_lg_3e166b549d.jpg" />
                                <el-button round >你好</el-button>
                            </div>
                        </div>
                        
                        <div class="message-container">
                            <div class="username">
                                Sam Lanson
                            </div>
                            <div class="main">
                                <el-avatar class="phone" size="small" src="https://social.webestica.com/assets/images/avatar/07.jpg" />
                                <el-button type="primary" round >我不好</el-button>
                            </div>
                        </div>
                        <div class="message-container">
                            <div class="username">
                                zzq
                            </div>
                            <div class="main">
                                <el-avatar class="phone" size="small" src="https://cdn.acwing.com/media/user/profile/photo/29231_lg_3e166b549d.jpg" />
                                <el-button round >你好</el-button>
                            </div>
                        </div>
                        
                        <div class="message-container">
                            <div class="username">
                                Sam Lanson
                            </div>
                            <div class="main">
                                <el-avatar class="phone" size="small" src="https://social.webestica.com/assets/images/avatar/07.jpg" />
                                <el-button type="primary" round >我不好</el-button>
                            </div>
                        </div>
                        <div class="message-container">
                            <div class="username">
                                zzq
                            </div>
                            <div class="main">
                                <el-avatar class="phone" size="small" src="https://cdn.acwing.com/media/user/profile/photo/29231_lg_3e166b549d.jpg" />
                                <el-button round >你好</el-button>
                            </div>
                        </div>
                        
                        <div class="message-container">
                            <div class="username">
                                Sam Lanson
                            </div>
                            <div class="main">
                                <el-avatar class="phone" size="small" src="https://social.webestica.com/assets/images/avatar/07.jpg" />
                                <el-button type="primary" round >我不好</el-button>
                            </div>
                        </div>
                        <!-- <el-button type="primary" round style="float: right;">我不好</el-button> -->
                    </el-scrollbar>
                </el-card>
                
                <el-card class="message-send" shadow="never">
                    <el-input
                        class="message-input"
                        :autosize="{ minRows: 6, maxRows: 6 }"
                        type="textarea"
                        placeholder="Please input message..."
                        v-model="message"
                        resize="none"
                    />
                    <el-button class="sendBtn" type="primary" @click="onSubmit" size="small">发送</el-button>
                </el-card>
            </el-card>
        </el-col>
    </el-row>
</template>

<script>
import PlayGround from '@/components/PlayGround.vue';
import MatchGround from '@/components/MatchGround.vue';
import { onMounted, onUnmounted } from 'vue';
import { useRoute } from 'vue-router';
import { useStore } from 'vuex';

export default {
    name: 'PkIndexView',
    components: {
        PlayGround,
        MatchGround,
    },
    setup() {
        const route = useRoute();
        const store = useStore();
        const game = route.params.game;
        const socketUrl = "wss://aigame.zzqahm.top/wss/multiplayer/snake/?token=" + store.state.user.access;
        let socket = null;
        if(game === "绕蛇") {
            onMounted(() => {
                store.commit("updateOpponent", {
                    username: "我的对手",
                    photo: "https://cdn.acwing.com/media/article/image/2022/08/09/1_1db2488f17-anonymous.png",
                });
                socket = new WebSocket(socketUrl);

                socket.onopen = () => {
                    console.log("connected!");
                    store.commit("updateSocket", socket);
                };

                socket.onmessage = msg => {
                    const data = JSON.parse(msg.data);
                    if(data.event === "start_match" && data.game) store.commit("updateGame", data.game);
                    if(data.username === store.state.user.username) return;
                    if(data.event === "start_match") {
                        store.commit("updateOpponent", {
                            username: data.username,
                            photo: data.photo,
                        });
                        setTimeout(() => {
                            store.commit("updateStatus", "playing");
                        }, 200);
                    } else if(data.event === "move") {
                        console.log(data)
                        const game = store.state.pk.gameObject;
                        const [snake0, snake1] = game.snakes;
                        snake0.set_direction(data.a_direction);
                        snake1.set_direction(data.b_direction);
                    } else if(data.event === "result") {
                        console.log(data);
                        const game = store.state.pk.gameObject;
                        const [snake0, snake1] = game.snakes;
    
                        if(data.loser === "all" || data.loser === "A") {
                            snake0.status = "die";
                        }
                        if(data.loser === "all" || data.loser === "B") {
                            snake1.status = "die";
                        }
                        store.commit("updateLoser", data.loser);
                    }
                }

                socket.onclose = () => {
                    console.log("disconnected!");
                }
            });

            onUnmounted(() => {
                socket.close();
                store.commit("updateStatus", "matching");
            });
        }

        return {
            game,
        }
    }
}
</script>

<style scoped>

.message /deep/.el-card__body {
    padding: 0px 0px !important;
}

.message /deep/.el-card__header {
    padding: 10px 10px !important;
}

.message-content /deep/.el-card__body {
    display: flex;
    flex-direction: column;
    padding: 5px 10px !important;
    padding-left: 1px;
    padding-right: 1px;
}

.message-content .message-container {
    margin: 10px 0;
}

.message-content .message-container .main {
    display: flex;
    align-items: center;
}

.message-content .message-container .username {
    color: grey;
    font-size: 8px;
    line-height: 10px;
    height: 10px;
    margin-bottom: 3px;
    margin-left: 6px;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    width: 45px;
}

.message-content .message-container .phone {
    margin: 0 4px;
}

.message /deep/.message-content {
    height: 320px;
}

.message /deep/.el-card__body {
    height: 480px !important;
}

.message-send /deep/.el-card__body {
    padding: 0px 0px !important;
}

.message-send .sendBtn {
    position: relative;
    float: right;
    top: -37px;
    margin-right: 5px;
}

.message-send .message-input {
    margin-top: 30px;
}
</style>