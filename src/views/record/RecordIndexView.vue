<template>
    <el-row style="margin-top: 40px;">
        <!-- 图片切换栏，对战列表 -->
        <el-col :span="14" :offset="2">
            <el-card class="box-card">
                <template #header>
                    <div class="card-header">
                        <span>最新对局</span>
                        <el-button class="button" type="primary" style="float: right;" @click="showCreateGameDialog = true">创建游戏</el-button>

                        <el-dialog v-model="showCreateGameDialog" title="新建游戏">
                            <el-form
                                label-position="top"
                                label-width="100px"
                                :model="currentOpBot"
                                style="max-width: 100%"
                            > 
                                <el-form-item label="操作方式">
                                    <el-radio-group v-model="operateSelect">
                                        <el-radio-button label="0">代码</el-radio-button>
                                        <el-radio-button label="1">键盘</el-radio-button>
                                    </el-radio-group>
                                </el-form-item>
                                    <el-form-item label="游戏">
                                        <el-radio-group v-model="gameSelect">
                                            <el-radio-button v-for="game in games" :key="game.id" :label="game.name">{{ game.name }}</el-radio-button>
                                        </el-radio-group>
                                    </el-form-item>
                                    <!-- 选择Bot，可查看Bot代码，不可编辑 -->
                                </el-form>
                            <template #footer>
                                <span class="dialog-footer">
                                    <el-button type="primary" @click="confirmGameDialog(gameSelect)">进入游戏</el-button>
                                    <el-button @click="showCreateGameDialog = false">取消</el-button>
                                </span>
                            </template>
                        </el-dialog>
                    </div>
                </template>
            </el-card>
        </el-col>
        <el-col :span="5" :offset="1">

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
import { onMounted, h, ref } from 'vue';
import { ElNotification } from 'element-plus'
import $ from 'jquery';
import { useStore } from 'vuex';
import router from '@/router';

export default {
    name: 'RecordIndexView',
    setup() {
        const store = useStore();
        let games = ref([]);
        let message = ref('');
        let showCreateGameDialog = ref(false);
        let operateSelect = ref(0);
        let gameSelect = ref('五子棋'); 

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

        onMounted(() => {
            ElNotification({
                title: 'Welcome',
                message: h('i', { style: 'color: teal' }, '欢迎来到King Of Bots游戏对战平台！'),
                offset: 70,
            });
            get_games();
        });

        const confirmGameDialog = game => {
            console.log(game);
            showCreateGameDialog.value = false;
            router.push({
                name: 'pk_index',
                params: {
                    game,
                }
            })
        }

        return {
            message,
            games,
            showCreateGameDialog,
            confirmGameDialog,
            operateSelect,
            gameSelect,
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