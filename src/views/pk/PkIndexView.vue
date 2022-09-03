<template>
    <el-row>
        <el-col :span="14" :offset="2">
            <PlayGround :game="game" v-if="$store.state.pk.status === 'playing'" />
            <MatchGround v-if="$store.state.pk.status === 'matching'" :operate="operate" :botId="botId" />
        </el-col>
        
        <el-col :span="5" :offset="1" style="margin-top: 40px;">
            <el-card class="message" style="user-select: none;">
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
        const game = parseInt(route.params.game);
        const operate = route.query.operate;
        const botId = route.query.bot_id;
        const socketUrl = "wss://aigame.zzqahm.top/wss/multiplayer/snake/?token=" + store.state.user.access;
        let socket = null;
        // 绕蛇
        if(game === 2) {
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

                const transDir = d => {
                    if(d <= 1) d += 2;
                    else d -= 2;
                    return d;
                }

                socket.onmessage = msg => {
                    const data = JSON.parse(msg.data);
                    console.log(data);
                    if(data.username === store.state.user.username) return;
                    if(data.event === "start_game") {
                        store.commit("updateOpponent", {
                            username: data.username,
                            photo: data.photo,
                        });
                        store.commit("updateGame", data.game);
                        setTimeout(() => {
                            store.commit("updateStatus", "playing");
                        }, 2000);
                    } else if(data.event === "move") {
                        const game = store.state.pk.gameObject;
                        const [snake0, snake1] = game.snakes;
                        if(store.state.user.id === store.state.pk.a_id) {
                            snake0.set_direction(data.a_direction);
                            snake1.set_direction(data.b_direction);
                        } else {
                            snake0.set_direction(transDir(data.b_direction));
                            snake1.set_direction(transDir(data.a_direction));
                        }
                    } else if(data.event === "result") {
                        const game = store.state.pk.gameObject;
                        const [snake0, snake1] = game.snakes;
    
                        if(data.loser === "all") {
                            snake0.status = "die", snake1.status = "die";
                        } else if(data.loser === "A" && store.state.user.id === store.state.pk.a_id || data.loser === "B" && store.state.user.id === store.state.pk.b_id) {
                            snake0.status = "die";
                        } else if(data.loser === "A" && store.state.user.id === store.state.pk.b_id || data.loser === "B" && store.state.user.id === store.state.pk.a_id) {
                            snake1.status = "die";
                        }
                        store.commit("updateGameResult", {
                            loser: data.loser,
                            status: data.status,
                        });
                        console.log(data);
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
            operate,
            botId,
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
    line-height: 14px;
    height: 15px;
    margin-bottom: 3px;
    margin-left: 6px;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    width: 80px;
    user-select: text;
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