<template>
    <div class="playground">
        <GameMap :game="game"></GameMap>
        <div v-if="flag === 'pk'" class="userinfo">
            <div class="userinfo-container">
                <div class="user-profile">
                    <img :src="$store.state.user.photo" alt="" style="user-select: none;">
                    <span class="username">{{ $store.state.user.username }}</span>
                </div>
                <div class="chess" :style="$store.state.pk.a_id === $store.state.user.id ? 'background-color: white;' : 'background-color: black;'" v-if="game === 1">
                </div>
                <div class="body" :style="$store.state.pk.a_id === $store.state.user.id ? 'background-color: #4876EC;' : 'background-color: #F94848;'" v-if="game === 2">
                    <div class="eye" />
                    <div class="eye" />
                </div>
                <div v-if="$store.state.pk.a_id === $store.state.user.id ? $store.state.pk.a_is_robot : $store.state.pk.b_is_robot">
                    <svg t="1662877386013" class="icon" viewBox="0 0 1280 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="2479" width="30" height="30"><path d="M0 512v256c0 35.4 28.6 64 64 64h64V448H64c-35.4 0-64 28.6-64 64zM928 192H704V64c0-35.4-28.6-64-64-64s-64 28.6-64 64v128H352c-88.4 0-160 71.6-160 160v544c0 70.6 57.4 128 128 128h640c70.6 0 128-57.4 128-128V352c0-88.4-71.6-160-160-160zM512 832h-128v-64h128v64z m-64-240c-44.2 0-80-35.8-80-80s35.8-80 80-80 80 35.8 80 80-35.8 80-80 80z m256 240h-128v-64h128v64z m192 0h-128v-64h128v64z m-64-240c-44.2 0-80-35.8-80-80s35.8-80 80-80 80 35.8 80 80-35.8 80-80 80z m384-144h-64v384h64c35.4 0 64-28.6 64-64V512c0-35.4-28.6-64-64-64z" fill="#1296db" p-id="2480"></path></svg>
                </div>
                <div v-if="$store.state.pk.a_id === $store.state.user.id && $store.state.pk.a_is_robot">
                    <el-tag
                        type="danger"
                        class="mx-1"
                        effect="dark"
                        round
                    >
                        {{ $store.state.pk.a_language }}
                    </el-tag>
                </div>
                <div v-else-if="$store.state.pk.b_id === $store.state.user.id && $store.state.pk.b_is_robot">
                    <el-tag
                        type="danger"
                        class="mx-1"
                        effect="dark"
                        round
                    >
                        {{ $store.state.pk.b_language }}
                    </el-tag>
                </div>
            </div>
            <div class="userinfo-container">
                <div v-if="$store.state.pk.a_id === $store.state.user.id && $store.state.pk.b_is_robot">
                    <el-tag
                        type="danger"
                        class="mx-1"
                        effect="dark"
                        round
                    >
                        {{ $store.state.pk.b_language }}
                    </el-tag>
                </div>
                <div v-else-if="$store.state.pk.b_id == $store.state.user.id && $store.state.pk.a_is_robot">
                    <el-tag
                        type="danger"
                        class="mx-1"
                        effect="dark"
                        round
                    >
                        {{ $store.state.pk.a_language }}
                    </el-tag>
                </div>
                <div v-if="$store.state.pk.a_id === $store.state.user.id ? $store.state.pk.b_is_robot : $store.state.pk.a_is_robot">
                    <svg t="1662877386013" class="icon" viewBox="0 0 1280 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="2479" width="30" height="30"><path d="M0 512v256c0 35.4 28.6 64 64 64h64V448H64c-35.4 0-64 28.6-64 64zM928 192H704V64c0-35.4-28.6-64-64-64s-64 28.6-64 64v128H352c-88.4 0-160 71.6-160 160v544c0 70.6 57.4 128 128 128h640c70.6 0 128-57.4 128-128V352c0-88.4-71.6-160-160-160zM512 832h-128v-64h128v64z m-64-240c-44.2 0-80-35.8-80-80s35.8-80 80-80 80 35.8 80 80-35.8 80-80 80z m256 240h-128v-64h128v64z m192 0h-128v-64h128v64z m-64-240c-44.2 0-80-35.8-80-80s35.8-80 80-80 80 35.8 80 80-35.8 80-80 80z m384-144h-64v384h64c35.4 0 64-28.6 64-64V512c0-35.4-28.6-64-64-64z" fill="#1296db" p-id="2480"></path></svg>
                </div>
                <div class="chess" :style="$store.state.pk.a_id === $store.state.user.id ? 'background-color: black;' : 'background-color: white;'" v-if="game === 1">
                </div>
                <div class="body" :style="$store.state.pk.a_id === $store.state.user.id ? 'background-color: #F94848;' : 'background-color: #4876EC;'" v-if="game === 2">
                    <div class="eye" />
                    <div class="eye" />
                </div>
                <div class="user-profile">
                    <img :src="$store.state.pk.opponent_photo" alt="" style="user-select: none;">
                    <span class="username">{{ $store.state.pk.opponent_username }}</span>
                </div>
            </div>
        </div>
        <div v-else-if="flag === 'record'" class="userinfo">
            <div class="userinfo-container">
                <div class="user-profile">
                    <img :src="$store.state.record.a_photo" alt="" style="user-select: none;">
                    <span class="username">{{ $store.state.record.a_username }}</span>
                </div>
                <div class="chess" style="background-color: white;" v-if="game === 1">
                </div>
                <div class="body" style="background-color: #4876EC;" v-if="game === 2">
                    <div class="eye" />
                    <div class="eye" />
                </div>
                <div v-if="$store.state.record.a_is_robot">
                    <svg t="1662877386013" class="icon" viewBox="0 0 1280 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="2479" width="30" height="30"><path d="M0 512v256c0 35.4 28.6 64 64 64h64V448H64c-35.4 0-64 28.6-64 64zM928 192H704V64c0-35.4-28.6-64-64-64s-64 28.6-64 64v128H352c-88.4 0-160 71.6-160 160v544c0 70.6 57.4 128 128 128h640c70.6 0 128-57.4 128-128V352c0-88.4-71.6-160-160-160zM512 832h-128v-64h128v64z m-64-240c-44.2 0-80-35.8-80-80s35.8-80 80-80 80 35.8 80 80-35.8 80-80 80z m256 240h-128v-64h128v64z m192 0h-128v-64h128v64z m-64-240c-44.2 0-80-35.8-80-80s35.8-80 80-80 80 35.8 80 80-35.8 80-80 80z m384-144h-64v384h64c35.4 0 64-28.6 64-64V512c0-35.4-28.6-64-64-64z" fill="#1296db" p-id="2480"></path></svg>
                </div>
                <div v-if="$store.state.record.a_is_robot">
                    <el-tag
                        type="danger"
                        class="mx-1"
                        effect="dark"
                        round
                    >
                        {{ $store.state.record.a_language }}
                    </el-tag>
                </div>
            </div>
            <div class="userinfo-container">
                <div v-if="$store.state.record.b_is_robot">
                    <el-tag
                        type="danger"
                        class="mx-1"
                        effect="dark"
                        round
                    >
                        {{ $store.state.record.b_language }}
                    </el-tag>
                </div>
                <div v-if="$store.state.record.b_is_robot">
                    <svg t="1662877386013" class="icon" viewBox="0 0 1280 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="2479" width="30" height="30"><path d="M0 512v256c0 35.4 28.6 64 64 64h64V448H64c-35.4 0-64 28.6-64 64zM928 192H704V64c0-35.4-28.6-64-64-64s-64 28.6-64 64v128H352c-88.4 0-160 71.6-160 160v544c0 70.6 57.4 128 128 128h640c70.6 0 128-57.4 128-128V352c0-88.4-71.6-160-160-160zM512 832h-128v-64h128v64z m-64-240c-44.2 0-80-35.8-80-80s35.8-80 80-80 80 35.8 80 80-35.8 80-80 80z m256 240h-128v-64h128v64z m192 0h-128v-64h128v64z m-64-240c-44.2 0-80-35.8-80-80s35.8-80 80-80 80 35.8 80 80-35.8 80-80 80z m384-144h-64v384h64c35.4 0 64-28.6 64-64V512c0-35.4-28.6-64-64-64z" fill="#1296db" p-id="2480"></path></svg>
                </div>
                <div class="chess" style="background-color: black;" v-if="game === 1">
                </div>
                <div class="body" style="background-color: #F94848;" v-if="game === 2">
                    <div class="eye" />
                    <div class="eye" />
                </div>
                <div class="user-profile">
                    <img :src="$store.state.record.b_photo" alt="" style="user-select: none;">
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

.userinfo img {
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
</style>