<template>
    <el-row style="margin-top: 20px;">
        <el-col :span="9" :offset="2">
            <div class="user-photo">
                <img :src="$store.state.user.photo" alt="">
            </div>
            <div class="user-username">
                {{ $store.state.user.username }}
            </div>
        </el-col>
        <el-col :span="9" :offset="2">
            <div class="user-photo">
                <img :src="$store.state.pk.opponent_photo" alt="">
            </div>
            <div class="user-username">
                {{ $store.state.pk.opponent_username }}
            </div>
        </el-col>
        <el-col :span="2" :offset="11" style="margin-top: 30px;">
            <el-button round class="match_btn" @click="click_match">{{ match_btn_info }}</el-button>
        </el-col>
    </el-row>
</template>

<script>
import { ref } from 'vue';
import { useStore } from 'vuex';

export default {
    name: 'MatchGround',
    setup() {
        const store = useStore();
        let match_btn_info = ref('开始匹配')

        const click_match = () => {
            if(match_btn_info.value === "开始匹配") {
                match_btn_info.value = "取消匹配";
                store.state.pk.socket.send(JSON.stringify({
                    event: "start_match",
                    username: store.state.user.username,
                    photo: store.state.user.photo,
                }));
            } else {
                match_btn_info.value = "开始匹配";
                store.state.pk.socket.send(JSON.stringify({
                    event: "stop_match",
                    username: store.state.user.username,
                    photo: store.state.user.photo,
                }));
            }
        }

        return {
            match_btn_info,
            click_match,
        }
    }
}
</script>

<style scoped>
div.user-photo {
    text-align: center;
    padding-top: 10vh;
}
 
div.user-photo > img {
    border-radius: 50%;
    width: 30vh;
}

div.user-username {
    text-align: center;
    font-size: 24px;
    font-weight: 600;
    color: white;
    padding-top: 2vh;
}

.match-btn {
    width: 100%;
}
</style>