<template>
    <div class="container">
        <div class="row">
            <div class="col-3">
                <div class="card">
                    <div class="card-body">
                        <img :src="$store.state.user.photo" alt="" style="width: 100%;">
                    </div>
                </div>
            </div>
            <div class="col-9">
                <div class="card">
                    <div class="card-header">
                        <span style="font-size: 130%;">我的Bot</span>
                        <button type="button" class="btn btn-primary float-end" data-bs-toggle="modal" data-bs-target="#add-bot">
                            创建Bot
                        </button>
                        <!-- Modal -->
                        <div class="modal fade" id="add-bot" tabindex="-1">
                            <div class="modal-dialog modal-xl">
                                <div class="modal-content">
                                    <div class="modal-header">
                                        <h5 class="modal-title">创建Bot</h5>
                                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                                    </div>
                                    <div class="modal-body">
                                        <div class="mb-3">
                                            <label for="add-bot-title" class="form-label">名称</label>
                                            <input v-model="bot.title" type="text" class="form-control" id="add-bot-title" placeholder="请输入Bot名称">
                                        </div>
                                        <div class="mb-3">
                                            <label for="add-bot-game" class="form-label">游戏</label>
                                            <select v-model="bot.game" id="add-bot-game" class="form-select">
                                                <option value="0" selected>请选择游戏</option>
                                                <option :key="game.id" :value="game.id" v-for="game in games">{{ game.name }}</option>
                                            </select>
                                        </div>
                                        <div class="mb-3">
                                            <label for="add-bot-description" class="form-label">简介</label>
                                            <input v-model="bot.description" type="text" class="form-control" id="add-bot-description" placeholder="请输入Bot简介">
                                        </div>
                                        <div class="mb-3">
                                            <label class="form-label">代码</label>
                                            <VAceEditor
                                                v-model:value="bot.content"
                                                @init="editorInit"
                                                lang="c_cpp"
                                                theme="textmate"
                                                style="height: 300px" />
                                        </div>
                                    </div>
                                    <div class="modal-footer">
                                        <button type="button" class="btn btn-primary" @click="add_bot">创建</button>
                                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">取消</button>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="card-body">
                        <table class="table table-striped table-hover">
                            <thead>
                                <tr>
                                    <th>名称</th>
                                    <th class="select-column">
                                        <select class="game-selects" v-model="game_select">
                                            <option value="0" selected>全部</option>
                                            <option :key="game.id" :value="game.id" v-for="game in games">{{ game.name }}</option>
                                        </select>
                                    </th>
                                    <th>创建时间</th>
                                    <th>操作</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-for="b in bots" :key="b.id">
                                    <td>{{ b.title }}</td>
                                    <td>{{ b.game }}</td>
                                    <td>{{ b.createtime }}</td>
                                    <td>
                                        <button type="button" class="btn btn-secondary" style="margin-right: 10px;" data-bs-toggle="modal" :data-bs-target="'#update-bot-modal-' + b.id">修改</button>

                                        <!-- Modal -->
                                        <div class="modal fade" :id="'update-bot-modal-' + b.id" tabindex="-1">
                                            <div class="modal-dialog modal-xl">
                                                <div class="modal-content">
                                                    <div class="modal-header">
                                                        <h5 class="modal-title">修改Bot</h5>
                                                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                                                    </div>
                                                    <div class="modal-body">
                                                        <div class="mb-3">
                                                            <label for="update-bot-title" class="form-label">名称</label>
                                                            <input v-model="b.title" type="text" class="form-control" id="add-bot-title" placeholder="请输入Bot名称">
                                                        </div>
                                                        <div class="mb-3">
                                                            <label for="update-bot-description" class="form-label">简介</label>
                                                            <input v-model="b.description" type="text" class="form-control" id="add-bot-description" placeholder="请输入Bot简介">
                                                        </div>
                                                        <div class="mb-3">
                                                            <label class="form-label">代码</label>
                                                            <VAceEditor
                                                                v-model:value="b.content"
                                                                @init="editorInit"
                                                                lang="c_cpp"
                                                                theme="textmate"
                                                                style="height: 300px" />
                                                        </div>
                                                    </div>
                                                    <div class="modal-footer">
                                                        <button type="button" class="btn btn-primary" @click="update_bot(b)">保存修改</button>
                                                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">取消</button>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>

                                        <button type="button" class="btn btn-danger" data-bs-toggle="modal" :data-bs-target="'#delete-bot-modal-' + b.id">删除</button>

                                        <!-- Modal -->
                                        <div class="modal fade" :id="'delete-bot-modal-' + b.id" tabindex="-1">
                                            <div class="modal-dialog">
                                                <div class="modal-content">
                                                    <div class="modal-header">
                                                        <h5 class="modal-title">删除Bot</h5>
                                                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                                                    </div>
                                                    <div class="modal-body">
                                                        确认删除名称为 {{ b.title }} 的Bot吗?
                                                    </div>
                                                    <div class="modal-footer">
                                                        <button type="button" class="btn btn-danger" @click="remove_bot(b)">确认删除</button>
                                                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">取消</button>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import $ from 'jquery';
import { ref, reactive, onMounted, watch } from 'vue';
import { useStore } from 'vuex';
import { VAceEditor } from 'vue3-ace-editor';
import * as ace from 'ace-builds';
import { Modal } from 'bootstrap/dist/js/bootstrap';
import { ElMessage } from 'element-plus';

export default {
    name: 'UserBotIndexView',
    components: {
        VAceEditor,
    },
    setup() {
        ace.config.set(
            "basePath", 
            "https://cdn.jsdelivr.net/npm/ace-builds@" + require('ace-builds').version + "/src-noconflict/");

        const editorInit = () => {
            require("ace-builds/src-noconflict/ext-language_tools");
            require("ace-builds/src-noconflict/snippets/sql");
            require("ace-builds/src-noconflict/mode-sql");
            require("ace-builds/src-noconflict/theme-monokai");
            require("ace-builds/src-noconflict/mode-html");
            require("ace-builds/src-noconflict/mode-html_elixir");
            require("ace-builds/src-noconflict/mode-html_ruby");
            require("ace-builds/src-noconflict/mode-javascript");
            require("ace-builds/src-noconflict/mode-python");
            require("ace-builds/src-noconflict/snippets/less");
            require("ace-builds/src-noconflict/theme-chrome");
            require("ace-builds/src-noconflict/ext-static_highlight");
            require("ace-builds/src-noconflict/ext-beautify");
        }

        const store = useStore();
        let bots = ref([]);
        let games = ref([]);
        let game_select = ref(0);

        const bot = reactive({
            title: "",
            game: 0,
            description: "",
            content: "",
        });

        const refresh_bots = () => {
            $.ajax({
                url: "https://aigame.zzqahm.top/player/bot/getlist/",
                type: "get",
                headers: {
                    "Authorization": "Bearer " + store.state.user.access,
                },
                success(resp) {
                    bots.value = resp;
                },
            });
        };

        const refresh_games = () => {
            console.log(123);
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

        refresh_bots();

        onMounted(() => {
            refresh_games();
        });

        const add_bot = () => {
            $.ajax({
                url: "https://aigame.zzqahm.top/player/bot/add/",
                type: "post",
                data: {
                    title: bot.title,
                    game_id: bot.game,
                    description: bot.description,
                    content: bot.content,
                },
                headers: {
                    "Authorization": "Bearer " + store.state.user.access,
                },
                success(resp) {
                    if(resp.result === "success") {
                        bot.title = "";
                        bot.game = 0;
                        bot.description = "";
                        bot.content = "";
                        Modal.getInstance("#add-bot").hide();
                        refresh_bots();

                        ElMessage({
                            showClose: true,
                            message: '添加成功',
                            type: 'success',
                        });
                    } else {
                        ElMessage.error(resp.result);
                    }
                },
                error(resp) {
                    console.log(resp);   
                }
            });
        };

        const remove_bot = bot => {
            $.ajax({
                url: "https://aigame.zzqahm.top/player/bot/remove/",
                type: "post",
                data: {
                    bot_id: bot.id,
                },
                headers: {
                    "Authorization": "Bearer " + store.state.user.access,
                },
                success(resp) {
                    console.log(resp)
                    if(resp.result === "success") {
                        Modal.getInstance('#delete-bot-modal-' + bot.id).hide();
                        refresh_bots();
                        ElMessage({
                            showClose: true,
                            message: '删除成功',
                            type: 'success',
                        });
                    }
                }
            });
        };

        const update_bot = bot => {
            $.ajax({
                url: "https://aigame.zzqahm.top/player/bot/update/",
                type: "post",
                data: {
                    bot_id: bot.id,
                    title: bot.title,
                    description: bot.description,
                    content: bot.content,
                },
                headers: {
                    "Authorization": "Bearer " + store.state.user.access,
                },
                success(resp) {
                    if(resp.result === 'success') {
                        Modal.getInstance('#update-bot-modal-' + bot.id).hide();
                        refresh_bots();
                        ElMessage({
                            showClose: true,
                            message: '更新成功',
                            type: 'success',
                        });
                    } else {
                        ElMessage.error(resp.result);
                    }
                },
            });
        };
        
        const getlist_game = () => {
            console.log(456);
            $.ajax({
                url: "https://aigame.zzqahm.top/player/bot/getlist_game/",
                type: "get",
                data: {
                    game_id: game_select.value,
                },
                headers: {
                    "Authorization": "Bearer " + store.state.user.access,
                },
                success(resp) {
                    bots.value = resp;
                },
            });
        };

        watch(() => game_select.value, (userRecover) => {
            if(userRecover == 0) {
                refresh_bots();
            } else {
                getlist_game();
            }
        });

        return {
            bots,
            games,
            bot,
            add_bot,
            remove_bot,
            update_bot,
            editorInit,
            game_select,
        }
    }
}
</script>

<style scoped>
div.card {
    margin-top: 20px;
}

.game-selects {
    font-weight: bolder;
}

.game-selects > option {
    font-weight: bolder; 
}
</style>