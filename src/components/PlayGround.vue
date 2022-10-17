<template>
    <div class="playground">
        <GameMap :game="game"></GameMap>
        <div v-if="flag === 'pk'" class="userinfo">
            <div class="userinfo-container">
                <div class="user-profile">
                    <img :src="$store.state.user.photo" alt="" style="user-select: none;" class="photo">
                    <span class="username">{{ $store.state.user.username }}</span>
                </div>
                <div class="chess"
                    :style="$store.state.pk.a_id === $store.state.user.id ? 'background-color: white;' : 'background-color: black;'"
                    v-if="game === 1">
                </div>
                <div class="body"
                    :style="$store.state.pk.a_id === $store.state.user.id ? 'background-color: #4876EC;' : 'background-color: #F94848;'"
                    v-if="game === 2">
                    <div class="eye" />
                    <div class="eye" />
                </div>
                <div
                    v-if="$store.state.pk.a_id === $store.state.user.id ? $store.state.pk.a_is_robot : $store.state.pk.b_is_robot">
                    <svg t="1662877386013" class="icon" viewBox="0 0 1280 1024" version="1.1"
                        xmlns="http://www.w3.org/2000/svg" p-id="2479" width="30" height="30">
                        <path
                            d="M0 512v256c0 35.4 28.6 64 64 64h64V448H64c-35.4 0-64 28.6-64 64zM928 192H704V64c0-35.4-28.6-64-64-64s-64 28.6-64 64v128H352c-88.4 0-160 71.6-160 160v544c0 70.6 57.4 128 128 128h640c70.6 0 128-57.4 128-128V352c0-88.4-71.6-160-160-160zM512 832h-128v-64h128v64z m-64-240c-44.2 0-80-35.8-80-80s35.8-80 80-80 80 35.8 80 80-35.8 80-80 80z m256 240h-128v-64h128v64z m192 0h-128v-64h128v64z m-64-240c-44.2 0-80-35.8-80-80s35.8-80 80-80 80 35.8 80 80-35.8 80-80 80z m384-144h-64v384h64c35.4 0 64-28.6 64-64V512c0-35.4-28.6-64-64-64z"
                            fill="#1296db" p-id="2480"></path>
                    </svg>
                </div>
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
            <div class="direction-msg" v-if="game === 2">
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
                <div
                    v-if="$store.state.pk.a_id === $store.state.user.id ? $store.state.pk.b_is_robot : $store.state.pk.a_is_robot">
                    <svg t="1662877386013" class="icon" viewBox="0 0 1280 1024" version="1.1"
                        xmlns="http://www.w3.org/2000/svg" p-id="2479" width="30" height="30">
                        <path
                            d="M0 512v256c0 35.4 28.6 64 64 64h64V448H64c-35.4 0-64 28.6-64 64zM928 192H704V64c0-35.4-28.6-64-64-64s-64 28.6-64 64v128H352c-88.4 0-160 71.6-160 160v544c0 70.6 57.4 128 128 128h640c70.6 0 128-57.4 128-128V352c0-88.4-71.6-160-160-160zM512 832h-128v-64h128v64z m-64-240c-44.2 0-80-35.8-80-80s35.8-80 80-80 80 35.8 80 80-35.8 80-80 80z m256 240h-128v-64h128v64z m192 0h-128v-64h128v64z m-64-240c-44.2 0-80-35.8-80-80s35.8-80 80-80 80 35.8 80 80-35.8 80-80 80z m384-144h-64v384h64c35.4 0 64-28.6 64-64V512c0-35.4-28.6-64-64-64z"
                            fill="#1296db" p-id="2480"></path>
                    </svg>
                </div>
                <div class="chess"
                    :style="$store.state.pk.a_id === $store.state.user.id ? 'background-color: black;' : 'background-color: white;'"
                    v-if="game === 1">
                </div>
                <div class="body"
                    :style="$store.state.pk.a_id === $store.state.user.id ? 'background-color: #F94848;' : 'background-color: #4876EC;'"
                    v-if="game === 2">
                    <div class="eye" />
                    <div class="eye" />
                </div>
                <div class="user-profile">
                    <img :src="$store.state.pk.opponent_photo" alt="" style="user-select: none;" class="photo">
                    <span class="username">{{ $store.state.pk.opponent_username }}</span>
                </div>
            </div>
        </div>
        <div v-else-if="flag === 'record'" class="userinfo">
            <div class="userinfo-container">
                <div class="user-profile">
                    <img :src="$store.state.record.a_photo" alt="" style="user-select: none;" class="photo">
                    <span class="username">{{ $store.state.record.a_username }}</span>
                </div>
                <div class="chess" style="background-color: white;" v-if="game === 1">
                </div>
                <div class="body" style="background-color: #4876EC;" v-if="game === 2">
                    <div class="eye" />
                    <div class="eye" />
                </div>
                <div v-if="$store.state.record.a_is_robot">
                    <svg t="1662877386013" class="icon" viewBox="0 0 1280 1024" version="1.1"
                        xmlns="http://www.w3.org/2000/svg" p-id="2479" width="30" height="30">
                        <path
                            d="M0 512v256c0 35.4 28.6 64 64 64h64V448H64c-35.4 0-64 28.6-64 64zM928 192H704V64c0-35.4-28.6-64-64-64s-64 28.6-64 64v128H352c-88.4 0-160 71.6-160 160v544c0 70.6 57.4 128 128 128h640c70.6 0 128-57.4 128-128V352c0-88.4-71.6-160-160-160zM512 832h-128v-64h128v64z m-64-240c-44.2 0-80-35.8-80-80s35.8-80 80-80 80 35.8 80 80-35.8 80-80 80z m256 240h-128v-64h128v64z m192 0h-128v-64h128v64z m-64-240c-44.2 0-80-35.8-80-80s35.8-80 80-80 80 35.8 80 80-35.8 80-80 80z m384-144h-64v384h64c35.4 0 64-28.6 64-64V512c0-35.4-28.6-64-64-64z"
                            fill="#1296db" p-id="2480"></path>
                    </svg>
                </div>
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
                <div v-if="$store.state.record.b_is_robot">
                    <svg t="1662877386013" class="icon" viewBox="0 0 1280 1024" version="1.1"
                        xmlns="http://www.w3.org/2000/svg" p-id="2479" width="30" height="30">
                        <path
                            d="M0 512v256c0 35.4 28.6 64 64 64h64V448H64c-35.4 0-64 28.6-64 64zM928 192H704V64c0-35.4-28.6-64-64-64s-64 28.6-64 64v128H352c-88.4 0-160 71.6-160 160v544c0 70.6 57.4 128 128 128h640c70.6 0 128-57.4 128-128V352c0-88.4-71.6-160-160-160zM512 832h-128v-64h128v64z m-64-240c-44.2 0-80-35.8-80-80s35.8-80 80-80 80 35.8 80 80-35.8 80-80 80z m256 240h-128v-64h128v64z m192 0h-128v-64h128v64z m-64-240c-44.2 0-80-35.8-80-80s35.8-80 80-80 80 35.8 80 80-35.8 80-80 80z m384-144h-64v384h64c35.4 0 64-28.6 64-64V512c0-35.4-28.6-64-64-64z"
                            fill="#1296db" p-id="2480"></path>
                    </svg>
                </div>
                <div class="chess" style="background-color: black;" v-if="game === 1">
                </div>
                <div class="body" style="background-color: #F94848;" v-if="game === 2">
                    <div class="eye" />
                    <div class="eye" />
                </div>
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