<template>
    <el-row style="margin-top: 40px;">
        <!-- 图片切换栏，对战列表 -->
        <el-col :span="14" :offset="2">
            <el-card class="box-card" style="user-select: none;">
                <div class="card-header" style="height: 32px;">
                    <span style="line-height: 32px;">最新对局</span>
                    <el-button class="button" type="primary" style="float: right;" @click="showCreateGameDialog = true">创建游戏</el-button>

                    <el-dialog v-model="showCreateGameDialog" title="新建游戏">
                        <el-form
                            label-position="top"
                            label-width="100px"
                            :model="createGameInfo"
                            :rules="rules"
                            style="max-width: 100%;"
                            ref="createGameForm"
                        > 
                            <el-form-item label="操作方式">
                                <el-radio-group v-model="createGameInfo.operateSelect">
                                    <el-radio-button label="0">代码</el-radio-button>
                                    <el-radio-button label="1">亲自出马</el-radio-button>
                                </el-radio-group>
                            </el-form-item>
                            
                            <el-form-item label="游戏">
                                <el-radio-group v-model="createGameInfo.gameSelect">
                                    <el-radio-button v-for="game in games" :key="game.id" :label="game.id">{{ game.name }}</el-radio-button>
                                </el-radio-group>
                            </el-form-item>
                            <el-form-item label="选择Bot" v-if="parseInt(createGameInfo.operateSelect) === 0" prop="botSelect">
                                <el-select v-model="createGameInfo.botSelect" class="m-2" placeholder="Select">
                                    <el-option
                                        v-for="bot in bots"
                                        :key="bot.id"
                                        :label="bot.title"
                                        :value="bot.id"
                                        @click="selectBotCode(bot)"
                                    />
                                </el-select>
                                <el-popover
                                    v-if="createGameInfo.botSelect"
                                    placement="right"
                                    :width="270"
                                    trigger="click"
                                >
                                    <template #reference>
                                        <el-icon :size="15" class="zoom"><ZoomIn /></el-icon>
                                    </template>
                                    <div class="popover-code-title" style="user-select: none;">查看代码</div>
                                    <el-scrollbar height="300px">
                                        <pre class="popover-content" style="width: 250px;">{{ botContent }}</pre>
                                    </el-scrollbar>
                                </el-popover>
                            </el-form-item>
                        </el-form>
                        <template #footer>
                            <span class="dialog-footer">
                                <el-button type="primary" @click="confirmGameDialog(createGameInfo.gameSelect)">进入游戏</el-button>
                                <el-button @click="showCreateGameDialog = false">取消</el-button>
                            </span>
                        </template>
                    </el-dialog>
                </div>
            </el-card>
            <RecordList recordListUrl="https://aigame.zzqahm.top/backend/record/getlist/" />
        </el-col>
        <el-col :span="5" :offset="1">
            <el-card class="message" style="user-select: none;">
                <template #header>
                  <div class="card-header">
                    <span>公共聊天区</span>
                  </div>
                </template>
                
                <el-card class="messages" shadow="never">
                    <el-scrollbar max-height="320px" ref="msgScroll">
                        <div class="message-content" v-for="msg in $store.state.record.hall_msgs" :key="msg.id">
                            <div class="username">
                                {{ msg.username }}
                            </div>
                            <div class="main">
                                <el-avatar class="photo" size="small" :src="msg.photo" />
                                <el-button round  :type="$store.state.user.username === msg.username ? 'primary' : ''">{{ msg.text }}</el-button>
                            </div>
                        </div>
                    </el-scrollbar>
                </el-card>
                
                <el-card class="message-send" shadow="never">
                    <el-form @submit.prevent="">
                        <el-input
                            class="message-input"
                            :autosize="{ minRows: 6, maxRows: 6 }"
                            type="textarea"
                            placeholder="Please input message..."
                            v-model="message"
                            resize="none"
                            @keydown.enter="enterSendMsg"
                        />
                        <el-button class="sendBtn" type="primary" @click="sendMsg" size="small">发送</el-button>
                    </el-form>
                </el-card>
            </el-card>
        </el-col>
    </el-row>
</template>

<script>
import { onMounted, onUnmounted, h, ref, unref, reactive, watch } from 'vue';
import { ElNotification } from 'element-plus'
import $ from 'jquery';
import { useStore } from 'vuex';
import router from '@/router';
import RecordList from '@/components/RecordList.vue';

export default {
    name: 'RecordIndexView',
    components: {
        RecordList,
    },
    setup() {
        const store = useStore();
        let games = ref([]);
        let bots = ref([]);
        let createGameForm = ref(null);
        let showCreateGameDialog = ref(false);
        let createGameInfo = reactive({
            operateSelect: 0,
            gameSelect: 1,
            botSelect: null,
        });
        let botContent = ref('');
        const socketUrl = "wss://aigame.zzqahm.top/wss/hall/?token=" + store.state.user.access;
        let message = ref('');
        let canSendMsg = ref(false);
        let msgScroll = ref(null);

        let socket = null;

        const get_games = () => {
            $.ajax({
                url: "https://aigame.zzqahm.top/backend/game/getlist/",
                type: "get",
                headers: {
                    "Authorization": "Bearer " + store.state.user.access,
                },
                success(resp) {
                    if(resp.result === "success") {
                        games.value = resp.games;
                    }
                },
            });
        };

        const refresh_bots = () => {
            $.ajax({
                url: "https://aigame.zzqahm.top/backend/player/bot/getlist_game/" + createGameInfo.gameSelect + '/',
                type: "get",
                data: {
                    userId: store.state.user.id,
                },
                headers: {
                    "Authorization": "Bearer " + store.state.user.access,
                },
                success(resp) {
                    if(resp.result === "success") {
                        bots.value = resp.bots;
                    }
                },
            });
        };

        refresh_bots();

        watch(() => createGameInfo.gameSelect, () => {
            refresh_bots();
            createGameInfo.botSelect = null;
            botContent.value = '';
        });

        const selectBotCode = bot => {
            botContent.value = bot.content;
        }

        onMounted(() => {
            ElNotification({
                title: 'Welcome',
                message: h('i', { style: 'color: teal' }, '欢迎来到King Of Bots游戏对战平台！'),
                offset: 70,
            });
            get_games();
            
            socket = new WebSocket(socketUrl);

            socket.onopen = () => {
                console.log("connected!");
                canSendMsg.value = true;
                store.commit("updateHallSocket", socket);
            };

            socket.onmessage = msg => {
                const data = JSON.parse(msg.data);
                if(data.username === store.state.user.username) return;
                if(data.event === "hall_message") {
                    store.commit("pushHallMsg", data.msg);
                    // const scroll = unref(msgScroll);
                    // scroll.setScrollTop(5000);
                }
            }

            socket.onclose = () => {
                canSendMsg.value = false;
                console.log("disconnected!");
            }
        });

        const confirmGameDialog = async(game) => {
            const form = unref(createGameForm);
            await form.validate(valid => {
                if(valid) {
                    showCreateGameDialog.value = false;
                    if(createGameInfo.operateSelect == 1) createGameInfo.botSelect = -1;
                    store.commit("updateBackPage", "record_index");
                    router.push({
                        name: 'pk_index',
                        params: {
                            game,
                        },
                        query: {
                            operate: createGameInfo.operateSelect,
                            bot_id: createGameInfo.botSelect,
                        }
                    });
                }
            })
        };

        onUnmounted(() => {
            socket.close();
        });
        
        const sendMsg = () => {
            if(!canSendMsg.value || message.value === "") return;
            store.state.record.hall_socket.send(JSON.stringify({
                event: "hall_message",
                username: store.state.user.username,
                photo: store.state.user.photo,
                text: message.value,
            }));
            canSendMsg.value = false;
            setTimeout(() => {
                canSendMsg.value = true;
            }, 1500);
            message.value = "";
            // const scroll = unref(msgScroll);
            // scroll.setScrollTop(scroll.scrollHeight);
        };

        const enterSendMsg = (e) => {
            if(e.ctrlKey && e.keyCode === 13) {   //用户点击了ctrl+enter触发
                message.value += '\n';
            } else { //用户点击了enter触发
                e.preventDefault();
                sendMsg();
            }  
        };

        return {
            games,
            showCreateGameDialog,
            confirmGameDialog,
            createGameInfo,
            bots,
            selectBotCode,
            botContent,
            createGameForm,
            rules: {
                botSelect: [
                    { required: true, message: '请选择Bot！', trigger: 'blur' },
                ],
            },
            message,
            sendMsg,
            enterSendMsg,
            msgScroll,
        }
    }
}
</script>

<style scoped>
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

.zoom {
    cursor: pointer;
    margin-left: 10px;
}

.popover-code-title {
    font-size: 17px;
    font-weight: 700;
    margin: 10px 10px;
}

.popover-content {
    margin: 0 10px;
}
</style>