<template>
    <el-card style="margin-top: 25px; user-select: none;">
        <el-table :data="records" style="width: 100%;" highlight-current-row max-height="720" table-layout="auto">
            <el-table-column prop="createtime" align="center" label="对局时间" />
            <el-table-column prop="game" label="游戏" align="center" width="190" />
            <el-table-column label="玩家" align="center" width="250">
                <template #default="scope">
                    <div class="player-container">
                        <div class="player-card" @click="enterPlayerSpace(scope.row.a_id)">
                            <el-avatar shape="square" size="small" :src="scope.row.a_photo" />
                            <span class="player-card-username">
                                <span class="records-username">
                                    {{ scope.row.a_username }}
                                </span>
                            </span>
                            <span class="player-result" v-if="scope.row.result === 'B'" style="color: #0099CC;">
                                +5
                            </span>
                            <span class="player-result" v-else-if="scope.row.result === 'A'" style="color: #FF0000;">
                                -2
                            </span>
                            <span class="player-result" v-else-if="scope.row.result === 'all'" style="color: #0099CC;">
                                +0
                            </span>
                        </div>
                        <span class="player-desb">
                            VS
                        </span>
                        <div class="player-card" @click="enterPlayerSpace(scope.row.b_id)">
                            <el-avatar shape="square" size="small" :src="scope.row.b_photo" />
                            <span class="player-card-username">
                                <span class="records-username">
                                    {{ scope.row.b_username }}
                                </span>
                            </span>
                            <span class="player-result" v-if="scope.row.result === 'B'" style="color: #ff0000;">
                                -2
                            </span>
                            <span class="player-result" v-else-if="scope.row.result === 'A'" style="color: #0099CC;">
                                +5
                            </span>
                            <span class="player-result" v-else-if="scope.row.result === 'all'" style="color: #0099CC;">
                                +0
                            </span>
                        </div>
                    </div>
                </template>
            </el-table-column>

            <el-table-column fixed="right" label="Operations" align="center">
                <template #default="scope">
                    <el-button @click="see_record(scope.row.id)" color="#6666CC">查看录像</el-button>
                </template>
            </el-table-column>
        </el-table>
    </el-card>
    <el-pagination 
        class="record-pagination" 
        background 
        layout="total, prev, pager, next, jumper" 
        :total="total_records"
        :page-size="10"
        pager-count="5"
        @current-change="pull_records"
    />
</template>

<script>
import $ from 'jquery';
import { useStore } from 'vuex';
import router from '@/router';
import { ref, onMounted } from 'vue';

export default {
    name: 'RecordList',
    props: {
        recordListUrl: {
            type: String,
            required: true
        }
    },
    setup(props) {
        const store = useStore();
        let records = ref([]);
        let total_records = ref(0);

        const pull_records = page => {
            $.ajax({
                url: props.recordListUrl,
                type: "get",
                data: {
                    page,
                },
                headers: {
                    "Authorization": "Bearer " + store.state.user.access,
                },
                success(resp) {
                    if(resp.result === "success") {
                        records.value = JSON.parse(resp.records);
                        total_records.value = resp.records_count;
                    }
                },
                error() {
                    store.dispatch("logout");
                }
            });
        };

        onMounted(() => {
            pull_records(1);
        });

        const stringTo2D = map => {
            let g = [];
            for(let i = 0, k = 0; i < 13; i++) {
                let line = [];
                for(let j = 0; j < 14; j++, k++) {
                    if(map[k] === '0') line.push(0);
                    else line.push(1);
                }
                g.push(line);
            }
            return g;
        }

        const see_record = recordId => {
            for(const record of records.value) {
                if(record.id === recordId) {
                    store.commit("updateIsRecord", true);
                    if(record.game_id === 2) {
                        store.commit("updateSnakeGame", {
                            map: stringTo2D(record.map),
                            a_id: record.a_id,
                            b_id: record.b_id,
                        });
                    } else if(record.game_id === 1 || record.game_id === 3) {
                        // 当加上随机优先后，可以带firstMove参数
                        store.commit("updateChessGame", {
                            a_id: record.a_id,
                            b_id: record.b_id,
                        });
                    }
                    store.commit("updateSteps", {
                        a_steps: record.a_steps,
                        b_steps: record.b_steps,
                    });
                    store.commit("updateRecordLoser", record.result);
                    store.commit("updatePlayerInfo", {
                        a_username: record.a_username,
                        a_photo: record.a_photo,
                        a_language: record.a_language,
                        b_username: record.b_username,
                        b_photo: record.b_photo,
                        b_language: record.b_language,
                    });
                    store.commit("updateIsRobot", {
                        a_is_robot: record.a_is_robot,
                        b_is_robot: record.b_is_robot
                    });
                    store.commit("updateBackPage", "record_index");
                    router.push({
                        name: 'record_content',
                        params: {
                            recordId,
                        },
                        query: {
                            game: record.game_id,
                        }
                    });
                    break;
                }
            }
        };

        const enterPlayerSpace = userId => {
            router.push(
                {
                    name: "myspace_index",
                    params: {
                        userId
                    }
                }
            );
        }

        return {
            records,
            see_record,
            total_records,
            pull_records,
            enterPlayerSpace,
        }
    }
}
</script>

<style scoped>
.player-container {
    display: flex;
    align-items: center;
    justify-content: space-around;
}

.player-card {
    cursor: pointer;
    border: 1px solid #ccc;
    border-radius: 5px;
    height: 50px;
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

.player-desb {
    color: #FF0033;
    font-size: 12px;
}

.player-result {
    background-color: #CCCCCC;
    width: 25px;
    height: 17px;
    text-align: center;
    font-size: 13px;
    line-height: 17px;
}

.records-username {
    user-select: text;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    width: 35px;
    color: #409EFF;
}

.record-pagination {
    display: flex;
    justify-content: center;
    margin-top: 20px;
}

.record-pagination:deep(.el-pagination__total),
.record-pagination:deep(.el-pagination__jump) {
    color: white;
}
</style>