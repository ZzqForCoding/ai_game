<template>
    <el-row style="margin-top: 40px;">
        <!-- 图片切换栏，对战列表 -->
        <el-col :span="14" :offset="2">
            <el-card class="box-card" style="user-select: none;">
                <template #header>
                    <div class="card-header">
                        <span>最新对局</span>
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
                                        <pre class="popover-content">{{ botContent }}</pre>
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
                </template>
            </el-card>
        </el-col>
        <el-col :span="5" :offset="1">
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
import { onMounted, h, ref, unref, reactive, watch } from 'vue';
import { ElNotification } from 'element-plus'
import $ from 'jquery';
import { useStore } from 'vuex';
import router from '@/router';

export default {
    name: 'RecordIndexView',
    setup() {
        const store = useStore();
        let games = ref([]);
        let bots = ref([]);
        let message = ref('');
        let createGameForm = ref(null);
        let showCreateGameDialog = ref(false);
        let createGameInfo = reactive({
            operateSelect: 0,
            gameSelect: 1,
            botSelect: null,
        });
        let botContent = ref('');

        const get_games = () => {
            $.ajax({
                url: "https://aigame.zzqahm.top/game/getlist/",
                type: "get",
                headers: {
                    "Authorization": "Bearer " + store.state.user.access,
                },
                success(resp) {
                    games.value = resp;
                },
            });
        };

        const refresh_bots = () => {
            $.ajax({
                url: "https://aigame.zzqahm.top/player/bot/getlist_game/",
                type: "get",
                data: {
                    game_id: createGameInfo.gameSelect,
                },
                headers: {
                    "Authorization": "Bearer " + store.state.user.access,
                },
                success(resp) {
                    bots.value = resp;
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
        });

        const confirmGameDialog = async(game) => {
            const form = unref(createGameForm);
            await form.validate(valid => {
                if(valid) {
                    showCreateGameDialog.value = false;
                    if(createGameInfo.operateSelect == 1) createGameInfo.botSelect = -1;
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

        return {
            message,
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
    line-height: 15px;
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