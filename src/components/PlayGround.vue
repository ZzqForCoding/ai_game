<template>
    <div class="playground">
        <GameMap :game="game"></GameMap>
        <div v-if="flag === 'pk'" class="userinfo">
            <div class="userinfo-container">
                <div class="user-profile">
                    <img :src="$store.state.user.photo" alt="">
                    <span class="username">{{ $store.state.user.username }}</span>
                </div>
                <div class="body" :style="$store.state.pk.a_id == $store.state.user.id ? 'background-color: #4876EC; margin-left: 10px;' : 'background-color: #F94848; margin-left: 10px;'">
                    <div class="eye" />
                    <div class="eye" />
                </div>
            </div>
            <div class="userinfo-container">
                <div class="body" :style="$store.state.pk.a_id == $store.state.user.id ? 'background-color: #F94848; margin-right: 10px;' : 'background-color: #4876EC; margin-right: 10px;'">
                    <div class="eye" />
                    <div class="eye" />
                </div>
                <div class="user-profile">
                    <img :src="$store.state.pk.opponent_photo" alt="">
                    <span class="username">{{ $store.state.pk.opponent_username }}</span>
                </div>
            </div>
        </div>
        <div v-if="flag === 'record'" class="userinfo">
            <div class="userinfo-container">
                <div class="user-profile">
                    <img :src="$store.state.record.a_photo" alt="">
                    <span class="username">{{ $store.state.record.a_username }}</span>
                </div>
                <div class="body" style="background-color: #4876EC; margin-left: 10px;">
                    <div class="eye" />
                    <div class="eye" />
                </div>
            </div>
            <div class="userinfo-container">
                <div class="body" style="background-color: #F94848; margin-right: 10px;">
                    <div class="eye" />
                    <div class="eye" />
                </div>
                <div class="user-profile">
                    <img :src="$store.state.record.b_photo" alt="">
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