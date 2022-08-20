<template>
    <div class="result-board">
        <div v-if="$store.state.pk.loser === 'all'" class="all">
            <div class="user-profile">
                <img :src="$store.state.user.photo" alt="">
                <span class="username">{{ $store.state.user.username }}</span>
            </div>
            <span class="user-state">
                平
            </span>
            <div class="user-profile">
                <img :src="$store.state.pk.opponent_photo" alt="">
                <span class="username">{{ $store.state.pk.opponent_username }}</span>
            </div>
        </div>
        <div v-else-if="$store.state.pk.loser === 'A' && $store.state.pk.a_id === parseInt($store.state.user.id) || $store.state.pk.loser === 'B' && $store.state.pk.b_id === parseInt($store.state.user.id)" class="lose">
            <div class="user-profile">
                <img :src="$store.state.user.photo" alt="">
                <span class="username">{{ $store.state.user.username }}</span>
            </div>
            <span class="user-state">
                输
            </span>
        </div>
        <div v-else class="win">
            <div class="user-profile">
                <img :src="$store.state.user.photo" alt="">
                <span class="username">{{ $store.state.user.username }}</span>
            </div>
            <span class="user-state">
                赢
            </span>
        </div>
        <div style="text-align: center;">
            <el-button color="rgb(255, 193, 7)" round @click="restart">再来一局</el-button>
            <el-button round @click="back">回到主页</el-button>
        </div>
    </div>
</template>

<script>
import router from '../router/index';
import { useStore } from 'vuex';

export default {
    name: "ResultBoard",
    setup() {
        const store = useStore();

        const restart = () => {
            store.commit("updateStatus", "matching");
            store.commit("updateLoser", 'none');
            store.commit("updateOpponent", {
                username: "我的对手",
                photo: "https://cdn.acwing.com/media/article/image/2022/08/09/1_1db2488f17-anonymous.png",
            });
        };

        const back = () => {
            router.push({name: 'record_index'});
            store.commit("updateStatus", "matching");
            store.commit("updateLoser", 'none');
            store.commit("updateOpponent", {
                username: "我的对手",
                photo: "https://cdn.acwing.com/media/article/image/2022/08/09/1_1db2488f17-anonymous.png",
            });
        };

        return {
            restart,
            back,
        }
    }
}
</script>

<style scoped>
div.result-board {
    background-color: rgba(50, 50, 50, 0.5);
    height: 120px;
    width: 18vw;
    position: absolute;
    border-radius: 20px;
}

div.result-board div.all {
    display: flex;
    justify-content: space-around;
    align-items: center;
    height: 80px;
}

div.all div.user-profile {
    width: 30%;
    text-align: center;
    display: flex;
    align-items: center;
    flex-direction: column;
}

div.user-profile .username {
    font-size: 12px;
    color: #cccccc;
    line-height: 12px;
}

div.user-profile > img {
    border-radius: 50%;
    width: 6vh;
 }

.user-state {
    font-size: 25px;
    color: white;
    font-style: italic;
}

div.win, div.lose {
    display: flex;
    align-items: center;
    justify-content: center;
    height: 80px;
}

div.win div.user-profile {
    display: flex;
    align-items: center;
    margin-right: 10px;
    flex-direction: column;
}

div.win div.user-profile .username {
    margin-top: 5px;
}

div.lose div.user-profile .username {
    margin-top: 5px;
}

div.lose div.user-profile {
    display: flex;
    align-items: center;
    margin-right: 10px;
    flex-direction: column;
}

</style>