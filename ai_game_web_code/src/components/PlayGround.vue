<template>
    <div class="playground">
        <GameMap :game="game"></GameMap>
        <div v-if="flag === 'pk'" class="userinfo">
            <div class="userinfo-container">
                <div class="user-profile">
                    <img :src="$store.state.user.photo" alt="" style="user-select: none;" class="photo">
                    <span class="username">{{ $store.state.user.username }}</span>
                </div>
                <div class="chess" :style="$store.state.pk.a_id === $store.state.user.id ? 'background-color: white;' : 'background-color: black;'" v-if="game === 1" />
                <div class="body" :style="$store.state.pk.a_id === $store.state.user.id ? 'background-color: #4876EC;' : 'background-color: #F94848;'" v-if="game === 2">
                    <div class="eye" />
                    <div class="eye" />
                </div>
                <div v-if="game === 3" class="chess" :style="$store.state.pk.a_id === $store.state.user.id ? 'background-color: white;' : 'background-color: black;'" />
                <div  v-if="game === 3 && $store.state.pk.a_id === $store.state.user.id" style="color: white; font-size: 18px; font-weight: 600;">白子：{{ $store.state.pk.aCnt }}</div>
                <div  v-if="game === 3 && $store.state.pk.b_id === $store.state.user.id" style="color: black; font-size: 18px; font-weight: 600;">黑子：{{ $store.state.pk.bCnt }}</div>
                <div v-if="$store.state.pk.a_id === $store.state.user.id && $store.state.pk.a_is_robot">
                    <el-tag type="danger" class="mx-1" effect="dark" round>
                        {{ $store.state.pk.a_language }}
                    </el-tag>
                </div>
                <div v-else-if="$store.state.pk.b_id === $store.state.user.id && $store.state.pk.b_is_robot">
                    <el-tag type="danger" class="mx-1" effect="dark" round>
                        {{ $store.state.pk.b_language }}
                    </el-tag>
                </div>
            </div>
            <div class="round-msg" v-if="game === 1">
                <span>round</span>
                <img src="https://xingqiu-tuchuang-1256524210.cos.ap-shanghai.myqcloud.com/501/none.png" alt=""
                    v-if="$store.state.pk.firstMove === null">
                <div class="chess" v-else
                    :style="$store.state.pk.a_id === $store.state.pk.firstMove ? 'background-color: white;' : 'background-color: black;'"
                >
                </div>
            </div>
            <div class="direction-msg" v-else-if="game === 2">
                <span>direction</span>
                <img src="https://xingqiu-tuchuang-1256524210.cos.ap-shanghai.myqcloud.com/501/none.png" alt=""
                    v-if="$store.state.pk.dir === -1">
                <img src="https://xingqiu-tuchuang-1256524210.cos.ap-shanghai.myqcloud.com/501/up.png" alt=""
                    v-else-if="$store.state.pk.dir === 0">
                <img src="https://xingqiu-tuchuang-1256524210.cos.ap-shanghai.myqcloud.com/501/right.png" alt=""
                    v-else-if="$store.state.pk.dir === 1">
                <img src="https://xingqiu-tuchuang-1256524210.cos.ap-shanghai.myqcloud.com/501/down.png" alt=""
                    v-else-if="$store.state.pk.dir === 2">
                <img src="https://xingqiu-tuchuang-1256524210.cos.ap-shanghai.myqcloud.com/501/left.png" alt="" v-else>
            </div>
            <div class="round-msg" v-else-if="game === 3">
                <span>round</span>
                <img src="https://xingqiu-tuchuang-1256524210.cos.ap-shanghai.myqcloud.com/501/none.png" alt=""
                    v-if="$store.state.pk.firstMove === null">
                <div class="chess" v-else
                    :style="$store.state.pk.a_id === $store.state.pk.firstMove ? 'background-color: white;' : 'background-color: black;'"
                >
                </div>
            </div>
            <div class="userinfo-container">
                <div v-if="$store.state.pk.a_id === $store.state.user.id && $store.state.pk.b_is_robot">
                    <el-tag type="danger" class="mx-1" effect="dark" round>
                        {{ $store.state.pk.b_language }}
                    </el-tag>
                </div>
                <div v-else-if="$store.state.pk.b_id == $store.state.user.id && $store.state.pk.a_is_robot">
                    <el-tag type="danger" class="mx-1" effect="dark" round>
                        {{ $store.state.pk.a_language }}
                    </el-tag>
                </div>
                <div class="chess" :style="$store.state.pk.a_id === $store.state.user.id ? 'background-color: black;' : 'background-color: white;'" v-if="game === 1">
                </div>
                <div class="body" :style="$store.state.pk.a_id === $store.state.user.id ? 'background-color: #F94848;' : 'background-color: #4876EC;'" v-if="game === 2">
                    <div class="eye" />
                    <div class="eye" />
                </div>
                <div v-if="game === 3" class="chess" :style="$store.state.pk.a_id === $store.state.user.id ? 'background-color: black;' : 'background-color: white;'" />
                <div v-if="game === 3 && $store.state.pk.a_id === $store.state.user.id" style="color: white; font-size: 18px; font-weight: 600;">黑子：{{ $store.state.pk.bCnt }}</div>
                <div v-if="game === 3 && $store.state.pk.b_id === $store.state.user.id" style="color: black; font-size: 18px; font-weight: 600;">白子：{{ $store.state.pk.aCnt }}</div>
                <div class="user-profile">
                    <img :src="$store.state.pk.opponent_photo" alt="" style="user-select: none;" class="photo">
                    <span class="username">{{ $store.state.pk.opponent_username }}</span>
                </div>
            </div>
        </div>
        <div v-else class="userinfo">
            <div class="userinfo-container">
                <div class="user-profile">
                    <img :src="$store.state.record.a_photo" alt="" style="user-select: none;" class="photo">
                    <span class="username">{{ $store.state.record.a_username }}</span>
                </div>
                <div class="chess" style="background-color: white;" v-if="game === 1">
                </div>
                <div class="body" style="background-color: #F94848;" v-if="game === 2">
                    <div class="eye" />
                    <div class="eye" />
                </div>
                <div v-if="game === 3" class="chess" style="background-color: white;" />
                <div v-if="game === 3" style="color: white; font-size: 18px; font-weight: 600;">白子：{{ $store.state.pk.aCnt }}</div>
                <div v-if="$store.state.record.a_is_robot">
                    <el-tag type="danger" class="mx-1" effect="dark" round>
                        {{ $store.state.record.a_language }}
                    </el-tag>
                </div>
            </div>
            <div class="userinfo-container">
                <div v-if="$store.state.record.b_is_robot">
                    <el-tag type="danger" class="mx-1" effect="dark" round>
                        {{ $store.state.record.b_language }}
                    </el-tag>
                </div>
                <div class="chess" style="background-color: black;" v-if="game === 1">
                </div>
                <div class="body" style="background-color: #4876EC;" v-if="game === 2">
                    <div class="eye" />
                    <div class="eye" />
                </div>
                <div v-if="game === 3" class="chess" style="background-color: black;" />
                <div v-if="game === 3" style="color: black; font-size: 18px; font-weight: 600;">黑子：{{ $store.state.pk.bCnt }}</div>
                <div class="user-profile">
                    <img :src="$store.state.record.b_photo" alt="" style="user-select: none;" class="photo">
                    <span class="username">{{ $store.state.record.b_username }}</span>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import GameMap from './GameMap.vue'
import { useStore } from 'vuex';
import { onUnmounted } from 'vue';

export default {
    name: 'PlayGround',
    components: {
        GameMap,
    },
    props: {
        game: {
            type: String,
            required: true,
        },
        flag: {
            type: String,
            required: true,
        }
    },
    setup() {
        const store = useStore();

        onUnmounted(() => {
            store.commit("updateCanSendMsg", false);
            store.commit("clearCodeOutMsg");
            store.commit("updateDir", -1);
            store.commit("updateFirstMove", null);
            // 还原黑白棋数量
            store.commit("updateChessCnt", {
                "aCnt": 2,
                "bCnt": 2
            });
        });
    }
}
</script>

<style scoped>
div.playground {
    width: 60vw;
    height: 70vh;
    margin: 40px auto;
    margin-bottom: 0px;
}

.userinfo {
    display: flex;
    justify-content: space-around;
}

.userinfo-container {
    display: flex;
    align-items: center;
    justify-content: space-around;
    width: 200px;
}

.userinfo .user-profile {
    display: flex;
    flex-direction: column;
}

.userinfo .photo {
    margin-top: 8px;
    border-radius: 50%;
    width: 45px;
}

.userinfo .username {
    margin-top: 7px;
    color: white;
    font-size: 17px;
    line-height: 15px;
    height: 15px;
    text-align: center;
}

.userinfo .chess {
    border-radius: 50%;
    width: 30px;
    height: 30px;
}

.userinfo .body {
    border-radius: 50%;
    width: 37px;
    height: 37px;
    display: flex;
    justify-content: space-around;
}

.userinfo .body .eye {
    margin-top: 10px;
    display: inline-block;
    background-color: black;
    width: 5px;
    height: 5px;
    border-radius: 50%;
}

@keyframes animateHeart {
    0% {
        transform: scale(1);
        transform-origin: center center;
        -webkit-animation-timing-function: ease-out;
        animation-timing-function: ease-out
    }

    10% {
        transform: scale(.91);
        -webkit-animation-timing-function: ease-in;
        animation-timing-function: ease-in
    }

    17% {
        transform: scale(.98);
        -webkit-animation-timing-function: ease-out;
        animation-timing-function: ease-out
    }

    33% {
        transform: scale(.87);
        -webkit-animation-timing-function: ease-in;
        animation-timing-function: ease-in
    }

    45% {
        transform: scale(1);
        -webkit-animation-timing-function: ease-out;
        animation-timing-function: ease-out
    }
}

.direction-msg, .round-msg {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 5vh;
    border-radius: 1vh;
    background-color: rgba(226, 237, 242, .3);
    margin-top: 20px;
    width: 180px;
    animation: animateHeart 1.5s ease-in-out infinite both;
}

.direction-msg span, .round-msg span {
    line-height: 5vh;
    font-weight: 600;
    font-size: 20px;
}

.direction-msg img, .round-msg img {
    height: 4vh;
    margin-left: 1vw;
}

.round-msg .chess {
    border-radius: 50%;
    width: 3.5vh;
    height: 3.5vh;
    margin-left: 1vw;
}
</style>