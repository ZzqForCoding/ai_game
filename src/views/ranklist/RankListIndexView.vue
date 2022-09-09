<template>
    <el-row style="margin-top: 40px;">
        <el-col :span="14" :offset="5">
            <el-card style="margin-top: 25px; user-select: none;">
                <template #header>
                    <div class="card-header">
                        <span class="ranklist-title">天梯分排行榜</span>
                    </div>
                </template>
                <el-table :data="players" style="width: 100%;" highlight-current-row max-height="720" table-layout="auto">
                    <el-table-column label="玩家" align="center" >
                        <template #default="scope">
                            <div class="userinfo">
                                <el-avatar shape="square" size="small" :src="scope.row.photo" />
                                <span class="player-card-username">
                                    <el-link type="primary" >
                                        <span class="ranklist-username">
                                            {{ scope.row.username }}
                                        </span>
                                    </el-link>
                                </span>
                            </div>
                        </template>
                    </el-table-column>
                    <el-table-column prop="rating" label="游戏" align="center" />
                </el-table>
            </el-card>
            <el-pagination 
                class="record-pagination" 
                background 
                layout="total, prev, pager, next, jumper" 
                :total="total_players"
                :page-size="10"
                pager-count="5"
                @current-change="pull_players"
            />
        </el-col>
    </el-row>
</template>

<script>
import { useStore } from 'vuex';
import $ from 'jquery';
import { ref, onMounted } from 'vue';

export default {
    name: 'RankListIndexView',
    setup() {
        const store = useStore();
        let players = ref([]);
        let total_players = ref(0);

        const pull_players = page => {
            $.ajax({
                url: "https://aigame.zzqahm.top/player/getranklist/",
                type: "get",
                data: {
                    page,
                },
                headers: {
                    "Authorization": "Bearer " + store.state.user.access,
                },
                success(resp) {
                    players.value = JSON.parse(resp.players);
                    total_players.value = resp.players_count;
                },
            });
        };

        onMounted(() => {
            pull_players(1);
        });

        return {
            players,
            total_players,
            pull_players,
        }
    }
}
</script>

<style scoped>
.ranklist-title {
    font-size: 20px;
    font-weight: 600;
}

.userinfo {
    display: flex;
    align-items: center;
    justify-content: center;
}

.ranklist-username {
    user-select: text;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    width: 60px;
}

.record-pagination {
    display: flex;
    justify-content: center;
    margin-top: 20px;
}

.record-pagination /deep/.el-pagination__total, .record-pagination /deep/.el-pagination__jump {
    color: white;
}
</style>