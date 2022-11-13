<template>
    <el-row>
        <el-col :span="14" :offset="2">
            <PlayGround :game="game" v-if="$store.state.pk.status === 'playing'" flag="pk" />
            <MatchGround v-if="$store.state.pk.status === 'matching'" :operate="operate" :botId="botId" />
        </el-col>

        <el-col :span="5" :offset="1" style="margin-top: 40px;">
            <el-card class="message" style="user-select: none;">
                <template #header>
                    <div class="card-header">
                        <span>公共聊天区</span>
                    </div>
                </template>

                <el-card class="messages" shadow="never">
                    <el-scrollbar max-height="150px" ref="msgScroll">
                        <div class="message-content" v-for="msg in $store.state.pk.msgs" :key="msg.id">
                            <div class="username">
                                {{ msg.username }}
                            </div>
                            <div class="main">
                                <el-avatar class="photo" size="small" :src="msg.photo" />
                                <el-button round :type="$store.state.user.username === msg.username ? 'primary' : ''">
                                    {{ msg.text }}
                                </el-button>
                            </div>
                        </div>
                    </el-scrollbar>
                </el-card>

                <el-card class="message-send" shadow="never">
                    <el-form @submit.prevent="">
                        <el-input class="message-input" :autosize="{ minRows: 6, maxRows: 6 }" type="textarea"
                            placeholder="Please input message..." v-model="message" resize="none"
                            @keydown.enter="enterSendMsg" />
                        <el-button class="sendBtn" type="primary" @click="sendMsg" size="small">发送</el-button>
                    </el-form>
                </el-card>
            </el-card>
            <!-- <el-card class="code-out-card" style="margin-top: 20px;"
                v-if="$store.state.pk.status === 'playing' && operate === 0">
                <template #header>
                    <div class="card-header">
                        <span>代码输出栏</span>
                    </div>
                </template>
                <el-scrollbar max-height="170px" style="height: 170px;">
                    <pre class="codeOutMsg">{{ $store.state.pk.codeOutMsg }}</pre>
                </el-scrollbar>
            </el-card> -->
        </el-col>
    </el-row>
</template>

<script>
import PlayGround from '@/components/PlayGround.vue';
import MatchGround from '@/components/MatchGround.vue';
import { onMounted, onUnmounted, ref } from 'vue';
import { useRoute } from 'vue-router';
import { useStore } from 'vuex';
import { ElMessage } from 'element-plus';

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
        const operate = parseInt(route.query.operate);
        const botId = route.query.bot_id;
        let socketUrl = "";
        let message = ref('');
        let msgScroll = ref(null);

        store.commit("updateGameResult", { loser: 'none', status: 'none' });
        store.commit("updateOpponent", {
            username: "我的对手",
            photo: "https://cdn.acwing.com/media/article/image/2022/08/09/1_1db2488f17-anonymous.png",
        });
        store.commit("updateIsRecord", false);

        let socket = null;
        // 五子棋
        if (game === 1) {
            onMounted(() => {
                socketUrl = "wss://aigame.zzqahm.top/wss/multiplayer/gobang/?token=" + store.state.user.access;
                socket = new WebSocket(socketUrl);

                socket.onopen = () => {
                    console.log("connected!");
                    store.commit("updateSocket", socket);
                    store.commit("updateCanSendMsg", true);
                };

                socket.onmessage = msg => {
                    const data = JSON.parse(msg.data);
                    if (data.username === store.state.user.username) return;
                    if (data.event === "pk_message") {
                        if (!store.state.pk.canSendMsg) return;
                        store.commit("pushMsg", data.msg);
                        if (data.msg.username === store.state.user.username) {
                            store.commit("updateCanSendMsg", false);
                            setTimeout(() => {
                                store.commit("updateCanSendMsg", true);
                            }, 1500);
                        }
                        // const scroll = unref(msgScroll);
                        // scroll.setScrollTop(80000);
                    } else if (data.event === "start_game") {
                        store.commit("updateOpponent", {
                            username: data.username,
                            photo: data.photo,
                        });
                        store.commit("updateChessGame", data.game);
                        store.commit("updateCanSendMsg", true);
                        store.commit("updateIsMatch", false);
                        setTimeout(() => {
                            store.commit("updateStatus", "playing");
                            store.commit("clearMatchTime", 0);
                        }, 2000);
                    } else if (data.event === "result") {
                        store.commit("updateGameResult", {
                            loser: data.loser,
                            status: data.status,    // 超时还是非法操作
                        });
                        let round = parseInt(data['round']);
                        if (round === store.state.pk.a_id) {
                            store.state.pk.gameObject.players[0].set_chess(parseInt(data['x']), parseInt(data['y']));
                            store.commit("updateFirstMove", store.state.pk.b_id);
                        } else if (round === store.state.pk.b_id) {
                            store.state.pk.gameObject.players[1].set_chess(parseInt(data['x']), parseInt(data['y']));
                            store.commit("updateFirstMove", store.state.pk.a_id);
                        }
                    } else if (data.event === "nextRound") {
                        let round = parseInt(data['round']);
                        if (round === store.state.pk.a_id) {
                            store.state.pk.gameObject.players[0].set_chess(parseInt(data['x']), parseInt(data['y']));
                            store.commit("updateFirstMove", store.state.pk.b_id);
                        } else if (round === store.state.pk.b_id) {
                            store.state.pk.gameObject.players[1].set_chess(parseInt(data['x']), parseInt(data['y']));
                            store.commit("updateFirstMove", store.state.pk.a_id);
                        }
                    } else if (data.event === "prompt") {
                        ElMessage(data.prompt);
                    }
                }

                socket.onclose = () => {
                    console.log("disconnected!");
                }
            });
        }
        // 绕蛇
        else if (game === 2) {
            onMounted(() => {
                socketUrl = "wss://aigame.zzqahm.top/wss/multiplayer/snake/?token=" + store.state.user.access;
                store.commit("updateMatchTime", 0);
                store.commit("clearMsg");
                socket = new WebSocket(socketUrl);

                socket.onopen = () => {
                    console.log("connected!");
                    store.commit("updateSocket", socket);
                };

                const transDir = d => {
                    if (d <= 1) d += 2;
                    else d -= 2;
                    return d;
                }

                socket.onmessage = msg => {
                    const data = JSON.parse(msg.data);
                    if (data.username === store.state.user.username) return;
                    if (data.event === "start_game") {
                        store.commit("updateOpponent", {
                            username: data.username,
                            photo: data.photo,
                        });
                        store.commit("updateSnakeGame", data.game);
                        store.commit("updateCanSendMsg", true);
                        store.commit("updateIsMatch", false);
                        setTimeout(() => {
                            store.commit("updateStatus", "playing");
                            store.commit("clearMatchTime", 0);
                        }, 2000);
                    } else if (data.event === "move") {
                        const game = store.state.pk.gameObject;
                        const [snake0, snake1] = game.snakes;
                        if (store.state.user.id === store.state.pk.a_id) {
                            store.commit("updateDir", data.a_direction);
                            snake0.set_direction(data.a_direction);
                            snake1.set_direction(data.b_direction);
                        } else {
                            store.commit("updateDir", transDir(data.b_direction));
                            snake0.set_direction(transDir(data.b_direction));
                            snake1.set_direction(transDir(data.a_direction));
                        }
                    } else if (data.event === "result") {
                        const game = store.state.pk.gameObject;
                        const [snake0, snake1] = game.snakes;
                        if (data.loser === "all") {
                            snake0.status = "die", snake1.status = "die";
                        } else if (data.loser === "A" && store.state.user.id === store.state.pk.a_id || data.loser === "B" && store.state.user.id === store.state.pk.b_id) {
                            snake0.status = "die";
                        } else if (data.loser === "A" && store.state.user.id === store.state.pk.b_id || data.loser === "B" && store.state.user.id === store.state.pk.a_id) {
                            snake1.status = "die";
                        }
                        store.commit("updateGameResult", {
                            loser: data.loser,
                            status: data.status,    // 超时还是非法操作
                        });
                    } else if (data.event === "pk_message") {
                        if (!store.state.pk.canSendMsg) return;
                        store.commit("pushMsg", data.msg);
                        if (data.msg.username === store.state.user.username) {
                            store.commit("updateCanSendMsg", false);
                            setTimeout(() => {
                                store.commit("updateCanSendMsg", true);
                            }, 1500);
                        }
                        // const scroll = unref(msgScroll);
                        // scroll.setScrollTop(80000);
                    } else if (data.event === "prompt") {
                        ElMessage(data.prompt);
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
        } else if(game === 3) {
            onMounted(() => {
                socketUrl = "wss://aigame.zzqahm.top/wss/multiplayer/reversi/?token=" + store.state.user.access;
                socket = new WebSocket(socketUrl);

                socket.onopen = () => {
                    console.log("connected!");
                    store.commit("updateSocket", socket);
                    store.commit("updateCanSendMsg", true);
                };

                socket.onmessage = msg => {
                    const data = JSON.parse(msg.data);
                    if (data.username === store.state.user.username) return;
                    if (data.event === "pk_message") {
                        if (!store.state.pk.canSendMsg) return;
                        store.commit("pushMsg", data.msg);
                        if (data.msg.username === store.state.user.username) {
                            store.commit("updateCanSendMsg", false);
                            setTimeout(() => {
                                store.commit("updateCanSendMsg", true);
                            }, 1500);
                        }
                        // const scroll = unref(msgScroll);
                        // scroll.setScrollTop(80000);
                    } else if (data.event === "start_game") {
                        store.commit("updateOpponent", {
                            username: data.username,
                            photo: data.photo,
                        });
                        // 修改函数名
                        store.commit("updateChessGame", data.game);
                        store.commit("updateCanSendMsg", true);
                        store.commit("updateIsMatch", false);
                        setTimeout(() => {
                            store.commit("updateStatus", "playing");
                            store.commit("clearMatchTime", 0);
                        }, 2000);
                    } else if (data.event === "result") {
                        store.commit("updateGameResult", {
                            loser: data.loser,
                            status: data.status,    // 超时还是非法操作
                        });
                        let round = parseInt(data['round']);
                        if (round === store.state.pk.a_id) {
                            store.state.pk.gameObject.players[0].set_chess(parseInt(data['x']), parseInt(data['y']));
                        } else if (round === store.state.pk.b_id) {
                            store.state.pk.gameObject.players[1].set_chess(parseInt(data['x']), parseInt(data['y']));
                        }
                    } else if (data.event === "nextRound") {
                        let round = parseInt(data['round']);
                        if (round === store.state.pk.a_id) {
                            store.state.pk.gameObject.players[0].set_chess(parseInt(data['x']), parseInt(data['y']));
                            store.state.pk.gameObject.adviseChess("black");
                            store.commit("updateFirstMove", store.state.pk.b_id);
                        } else if (round === store.state.pk.b_id) {
                            store.state.pk.gameObject.players[1].set_chess(parseInt(data['x']), parseInt(data['y']));
                            store.state.pk.gameObject.adviseChess("white");
                            store.commit("updateFirstMove", store.state.pk.a_id);
                        }
                    } else if (data.event === "toggleRound") {
                        setTimeout(() => {
                            store.commit("updateFirstMove", store.state.pk.firstMove === store.state.pk.a_id ? store.state.pk.b_id : store.state.pk.a_id);
                        }, 1000);
                    } else if (data.event === "prompt") {
                        ElMessage(data.prompt);
                    }
                }

                socket.onclose = () => {
                    console.log("disconnected!");
                }
            });
        }

        const sendMsg = () => {
            if (!store.state.pk.canSendMsg || message.value === "") return;
            store.state.pk.socket.send(JSON.stringify({
                event: "pk_message",
                username: store.state.user.username,
                photo: store.state.user.photo,
                text: message.value,
            }));
            message.value = "";
            // const scroll = unref(msgScroll);
            // scroll.setScrollTop(80000);
        };

        const enterSendMsg = (e) => {
            if (e.ctrlKey && e.keyCode === 13) {   //用户点击了ctrl+enter触发
                message.value += '\n';
            } else { //用户点击了enter触发
                e.preventDefault();
                sendMsg();
            }
        };

        return {
            game,
            operate,
            botId,
            message,
            sendMsg,
            enterSendMsg,
            msgScroll,
        }
    }
}
</script>

<style scoped>
.code-out-card:deep(.el-card__header) {
    padding: 10px 10px !important;
}

.code-out-card:deep(.el-card__body) {
    padding: 5px 5px !important;
}

.codeOutMsg {
    color: black;
    font-weight: 500;
    font-size: 15px;
    line-height: 20px;
    margin: 5px 5px;
}

.message:deep(.el-card__body) {
    padding: 0px 0px !important;
}

.message:deep(.el-card__header) {
    padding: 10px 10px !important;
}

.messages:deep(.el-card__body) {
    display: flex;
    flex-direction: column;
    padding: 5px 10px !important;
}

.messages .message-content {
    margin: 10px 0;
}

.messages .message-content .main {
    display: flex;
    align-items: center;
}

.messages .message-content .username {
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

.messages .message-content .photo {
    margin: 0 4px;
}

.message:deep(.messages) {
    height: 150px;
}

.message:deep(.el-card__body) {
    height: 280px !important;
}

.message-send:deep(.el-card__body) {
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