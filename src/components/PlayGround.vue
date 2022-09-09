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

</style>