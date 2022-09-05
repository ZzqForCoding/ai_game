<template>
    <div class="playground">
        <GameMap :game="game"></GameMap>
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
        }
    },
    setup() {
        const store = useStore();

        onUnmounted(() => {
            store.commit("updateOpponent", {
                username: "我的对手",
                photo: "https://cdn.acwing.com/media/article/image/2022/08/09/1_1db2488f17-anonymous.png",
            }); 
            store.commit("updateCanSendMsg", false);
        });
    }
}
</script>

<style scoped>
div.playground {
    width: 92%;
    height: 92%;
    margin: 40px auto;
    margin-bottom: 0px;
}

</style>