<template>
    <el-row style="margin-top: 40px;">
        <el-col :span="20" :offset="2">
            <el-carousel indicator-position="outside" height="150px">
                <el-carousel-item v-for="image in images" :key="image.id">
                    <img :src="image.url" class="carousel-image-type">
                </el-carousel-item>
            </el-carousel>
        </el-col>
        <el-col :span="14" :offset="2">
            <el-card class="box-card" style="user-select: none;">
                <div class="card-header" style="height: 32px;">
                    <span style="line-height: 32px;">最新对局</span>
                    <el-button class="button" type="primary" style="float: right;" @click="showCreateGameDialog = true">
                        创建游戏</el-button>

                    <el-dialog v-model="showCreateGameDialog" title="新建游戏">
                        <el-form label-position="top" label-width="100px" :model="createGameInfo" :rules="rules"
                            style="max-width: 100%;" ref="createGameForm">
                            <el-form-item label="操作方式">
                                <el-radio-group v-model="createGameInfo.operateSelect">
                                    <el-radio-button label="0">代码</el-radio-button>
                                    <el-radio-button label="1">亲自出马</el-radio-button>
                                </el-radio-group>
                            </el-form-item>

                            <el-form-item label="游戏">
                                <el-radio-group v-model="createGameInfo.gameSelect">
                                    <el-radio-button v-for="game in games" :key="game.id" :label="game.id">{{ game.name
                                    }}</el-radio-button>
                                </el-radio-group>
                            </el-form-item>
                            <el-form-item label="选择Bot" v-if="parseInt(createGameInfo.operateSelect) === 0"
                                prop="botSelect">
                                <el-select v-model="createGameInfo.botSelect" class="m-2" placeholder="Select">
                                    <el-option v-for="bot in bots" :key="bot.id" :label="bot.title" :value="bot.id"
                                        @click="selectBotCode(bot)" />
                                </el-select>
                                <el-popover v-if="createGameInfo.botSelect" placement="right" :width="270"
                                    trigger="click">
                                    <template #reference>
                                        <el-icon :size="15" class="zoom">
                                            <ZoomIn />
                                        </el-icon>
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
                                <el-button type="primary" @click="confirmGameDialog(createGameInfo.gameSelect)">进入游戏
                                </el-button>
                                <el-button @click="showCreateGameDialog = false">取消</el-button>
                            </span>
                        </template>
                    </el-dialog>
                </div>
            </el-card>
            <RecordList recordListUrl="https://aigame.zzqahm.top/backend/record/getlist/" />
        </el-col>
        <el-col :span="5" :offset="1">
            <el-card class="message-card" style="user-select: none;">
                <template #header>
                    <div class="card-header">
                        <span>公共聊天区</span>
                    </div>
                </template>

                <el-card class="message-body" shadow="never">
                    <el-scrollbar max-height="250px">
                        <div class="message-content" v-for="msg in $store.state.record.hall_msgs" :key="msg.id">
                            <div class="username">
                                {{ msg.username }}
                            </div>
                            <div class="main">
                                <el-avatar class="photo info-scale" size="small" :src="msg.photo" @click="enterPlayerSpace(msg.userId)" />
                                <el-button round :type="$store.state.user.username === msg.username ? 'primary' : ''">
                                    {{ msg.text }}
                                </el-button>
                            </div>
                        </div>
                    </el-scrollbar>
                </el-card>
                <el-card class="message-send" shadow="never">
                    <el-form @submit.prevent="">
                        <el-input class="message-input" type="textarea"
                            placeholder="Please input message..." v-model="message" resize="none"
                            @keydown.enter="enterSendMsg" />
                        <el-button class="sendBtn" type="primary" @click="sendMsg" size="small">发送</el-button>
                    </el-form>
                </el-card>
            </el-card>
            <el-card class="box-card" style="margin-top: 40px;">
                <template #header>
                    <div class="card-header">
                        <span>{{ chartTitle }}</span>
                        <el-dropdown style="float: right;">
                            <span class="el-dropdown-link">
                                <el-button text style="float: right">
                                    <el-icon style="vertical-align: middle;"><ArrowDownBold /></el-icon>
                                </el-button>
                            </span>
                            <template #dropdown>
                            <el-dropdown-menu>
                                <el-dropdown-item @click="selectChart(0)">网站注册及访问量图</el-dropdown-item>
                                <el-dropdown-item @click="selectChart(1)">语言熟练度图</el-dropdown-item>
                            </el-dropdown-menu>
                            </template>
                        </el-dropdown>
                        
                    </div>
                </template>
                <div id="myEcharts" :style="{ height: '360px' }"></div>
            </el-card>
        </el-col>
    </el-row>
</template>

<script>
import { onMounted, onUnmounted, ref, unref, reactive, watch, nextTick } from 'vue';
import $ from 'jquery';
import { useStore } from 'vuex';
import router from '@/router';
import RecordList from '@/components/RecordList.vue';
import * as echarts from "echarts";

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
        let chart = null;
        let chartTitle = ref('');
        
        let chartData = [
            {
                tooltip: {
                    trigger: 'axis'
                },
                legend: {
                    data: ['访问量', '注册']
                },
                toolbox: {
                    show: true,
                    feature: {
                        magicType: { show: true, type: ['line'] },
                        restore: { show: true },
                        saveAsImage: { show: true }
                    }
                },
                calculable: true,
                xAxis: [
                    {
                        type: 'category',
                        data: []
                    }
                ],
                yAxis: [
                    {
                        type: 'value',
                        axisLabel: {
                            formatter: '{value} 人'
                        }
                    }
                ],
                series: [
                    {
                        name: '访问量',
                        type: 'bar',
                        data: [],
                    },
                    {
                        name: '注册',
                        type: 'bar',
                        data: [],
                    }
                ]
            },
            {
                legend: {
                    data: ['熟练度']
                },
                tooltip: {
                    trigger: 'axis'
                },
                toolbox: {
                    show: true,
                    feature: {
                        saveAsImage: { show: true }
                    }
                },
                radar: {
                    shape: 'circle',
                    indicator: [
                        { name: 'C++', max: 1 },
                        { name: 'Java', max: 1 },
                        { name: 'Python', max: 1 },
                    ]
                },
                series: [
                    {
                        type: 'radar',
                        tooltip: {
                            trigger: 'item'
                        },
                        data: [
                            {
                                value: [],
                                name: '熟练度'
                            }
                        ]
                    }
                ]
            }
        ];

        const images = ref([
            {id: 1, url: "https://img.zzqahm.top/aigame_platform/avatar/background4.png"},
            {id: 2, url: "https://img.zzqahm.top/aigame_platform/avatar/background5.png"},
            {id: 3, url: "https://img.zzqahm.top/aigame_platform/avatar/background8.jpeg"}
        ]);

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
                error() {
                    store.dispatch("logout");
                }
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
                error() {
                    store.dispatch("logout");
                }
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
            get_games();
            
            socket = new WebSocket(socketUrl);

            socket.onopen = () => {
                console.log("connected!");
                canSendMsg.value = true;
                store.commit("updateHallSocket", socket);
            };

            socket.onmessage = msg => {
                const data = JSON.parse(msg.data);
                if(data.event === "hall_message") {
                    store.commit("pushHallMsg", data.msg);
                }
            }

            socket.onclose = () => {
                canSendMsg.value = false;
                console.log("disconnected!");
            }

            nextTick(() => {
                chart = echarts.init(document.getElementById("myEcharts"));
                get_chart_data();
            });
        });
        
        window.onresize = function() {
            //自适应大小
            chart.resize();
        };

        onUnmounted(() => {
            canSendMsg.value = false;
            socket.close();
            chart.dispose()
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
        
        const sendMsg = () => {
            canSendMsg.value = false;
            if(!canSendMsg.value || message.value === "" || message.value.trim() === "") return;
            setTimeout(() => {
                canSendMsg.value = true;
            }, 1500);
            store.state.record.hall_socket.send(JSON.stringify({
                event: "hall_message",
                userId: store.state.user.id,
                username: store.state.user.username,
                photo: store.state.user.photo,
                text: message.value,
            }));
            message.value = "";
        };

        const enterSendMsg = (e) => {
            e.preventDefault();
            sendMsg();
        };

        const enterPlayerSpace = userId => {
            router.push({ 
                name: "myspace_index",
                params: {
                    userId
                }
            });
        }

        const selectChart = idx => {
            chart.clear();
            setTimeout(() => {
                chart.setOption(chartData[idx], true);
            }, 100);
            if(idx === 0) {
                chartTitle.value = "网站注册及访问量图";
            } else if(idx === 1) {
                chartTitle.value = "语言熟练度图";
            }
        };

        const get_chart_data = () => {
           $.ajax({
                 url: 'https://aigame.zzqahm.top/backend/player/getchartdata/',
                type: "get",
                headers: {
                    "Authorization": "Bearer " + store.state.user.access,
                },
                success(resp) {
                    if(resp.result === "success") {
                        chartData[0].xAxis[0].data = resp['dates'];
                        chartData[0].series[0].data = resp['login_cnts'];
                        chartData[0].series[1].data = resp['register_cnts'];
                        chartData[1].series[0].data[0].value = resp['lang_skilled'];
                        selectChart(0);
                   }
                },
                error() {
                    store.dispatch("logout");
                }
            });
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
            enterPlayerSpace,
            images,
            selectChart,
            chartTitle,
            rules: {
                botSelect: [
                    { required: true, message: '请选择Bot！', trigger: 'blur' },
                ],
            },
            message,
            sendMsg,
            enterSendMsg,
        }
    }
}
</script>

<style scoped>
.message-card:deep(.el-card__body) {
    padding: 0px 0px !important;
}

.message-card:deep(.el-card__header) {
    padding: 10px 10px !important;
}

.message-body:deep(.el-card__body) {
    display: flex;
    flex-direction: column;
    padding: 5px 10px !important;
}

.message-body .message-content {
    margin: 5px 0;
    height: 60px;
}

.message-body .message-content .main {
    display: flex;
    align-items: center;
}

.message-body .message-content .username {
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

.message-body .message-content .photo {
    margin: 0 4px;
}

.message-card:deep(.message-body) {
    height: 250px;
}

.message-card:deep(.el-card__body) {
    height: 350px !important;
}

.message-input:deep(.el-textarea__inner) {
    height: 100px;
}

.message-send .sendBtn {
    position: relative;
    float: right;
    top: -30px;
    margin-right: 5px;
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

.info-scale:hover {
    transform: scale(1.2);
    transition: 100ms;
    cursor: pointer;
}

.carousel-image-type {
    width: 100%;
}
</style>