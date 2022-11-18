<template>
    <el-row style="margin-top: 40px;">
        <el-col :span="14" :offset="5">
            <el-card style="margin-top: 25px; user-select: none;">
                <template #header>
                    <div class="card-header">
                        <span class="ranklist-title">天梯分排行榜</span>
                        <el-button style="float: right;" type="primary" @click="findme">我</el-button>
                    </div>
                </template>
                <el-table :data="players" style="width: 100%;" highlight-current-row max-height="720"
                    table-layout="auto">
                    <el-table-column label="rank" align="center" prop="rank" width="140" />
                    <el-table-column label="玩家" align="center">
                        <template #default="scope">
                            <div class="player-container">
                                <div class="player-card" @click="enterPlayerSpace(scope.row.id)">
                                    <el-avatar shape="square" size="small" :src="scope.row.photo"
                                        style="margin-left: 10px;" />
                                    <span class="player-card-username">
                                        <span class="ranklist-username">
                                            {{ scope.row.username }}
                                        </span>
                                    </span>
                                </div>
                                <span v-if="is_find && $store.state.user.username === scope.row.username"
                                    style="height: 15px; margin-left: 5px;">
                                    <el-icon :size="15">
                                        <Back />
                                    </el-icon>
                                </span>
                            </div>
                        </template>
                    </el-table-column>
                    <el-table-column prop="rating" label="游戏" align="center" />
                </el-table>
            </el-card>
            <el-pagination class="player-pagination" background layout="total, prev, pager, next, jumper"
                :total="total_players" :page-size="10" v-model:current-page="current_page" pager-count="5"
                @current-change="pull_players" />
            {{ current_page }}
        </el-col>
    </el-row>
</template>

<script>
import { useStore } from 'vuex';
import $ from 'jquery';
import router from '@/router';
import { ref, onMounted } from 'vue';

export default {
    name: 'RankListIndexView',
    setup() {
        const store = useStore();
        let players = ref([]);
        let total_players = ref(0);
        let is_find = ref(false);
        let current_page = ref(1);

        const pull_players = page => {
            $.ajax({
                url: "https://aigame.zzqahm.top/backend/player/getranklist/",
                type: "get",
                data: {
                    page,
                },
                headers: {
                    "Authorization": "Bearer " + store.state.user.access,
                },
                success(resp) {
                    if (resp.result === "success") {
                        players.value = JSON.parse(resp.players);
                        total_players.value = resp.players_count;
                    }
                },
                error() {
                    store.dispatch("logout");
                }
            });
        };

        onMounted(() => {
            pull_players(1);
        });

        const findme = () => {
            $.ajax({
                url: "https://aigame.zzqahm.top/backend/player/getplayerpage/",
                type: "get",
                headers: {
                    "Authorization": "Bearer " + store.state.user.access,
                },
                success(resp) {
                     if (resp.result === "success") {
                        current_page.value = resp.page;
                       pull_players(current_page.value);
                         is_find.value = true;
                    }
                },
                error() {
                    store.dispatch("logout");
                }
            });
        }

        const enterPlayerSpace = userId => {
            router.push({ 
                name: "myspace_index",
                params: {
                    userId
                }
            });
        }

        return {
            players,
            total_players,
            pull_players,
            findme,
            is_find,
            current_page,
            enterPlayerSpace,
        }
    }
}
</script>

<style scoped>
.ranklist-title {
    font-size: 20px;
    font-weight: 600;
}

.player-container {
    display: flex;
    align-items: center;
    justify-content: center;
}

.player-card {
    cursor: pointer;
    border: 1px solid #ccc;
    border-radius: 5px;
    height: 35px;
    width: 90px;
    display: flex;
    align-items: center;
    justify-content: space-around;
}

.player-card:hover {
    transform: scale(1.02);
    background-color: #ccc;
    transition: 100ms;
}

.ranklist-username {
    user-select: text;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    width: 50px;
    color: #409EFF;
}

.player-card-username {
    display: flex;
    align-items: center;
}

.player-pagination {
    display: flex;
    justify-content: center;
    margin-top: 20px;
}

.player-pagination:deep(.el-pagination__total),
.player-pagination:deep(.el-pagination__jump) {
    color: white;
}
</style>