<template>
    <div class="gamemap" ref="parent">
        <canvas ref="canvas" tabindex="0" @contextmenu.prevent="" style="height: 100%;"></canvas>
        <ResultBoard v-if="$store.state.pk.loser != 'none'" />
    </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import ResultBoard from '@/components/ResultBoard.vue';
import { GameMap as SnakeGameMap } from '@/assets/scripts/Snake/GameMap';
import { GameMap as GobangGameMap } from '@/assets/scripts/Gobang/GameMap';
import { GameMap as ReversiGameMap } from '@/assets/scripts/Reversi/GameMap';
import { useStore } from 'vuex';

export default {
    name: 'GameMap',
    components: {
        ResultBoard,
    },
    props: {
        game: {
            type: Number,
            required: true,
        }
    },
    setup(props) {
        const store = useStore();
        let parent = ref(null);
        let canvas = ref(null);

        onMounted(() => {
            store.commit("updateGameResult", {loser: 'none', status: 'none'});
            if(props.game === 2) {
                store.commit(
                    "updateGameObject",
                    new SnakeGameMap(canvas.value.getContext('2d'), parent.value, store)
                );
            } else if(props.game === 1) {
                store.commit(
                    "updateGameObject",
                    new GobangGameMap(canvas.value.getContext('2d'), parent.value, store)
                );
            } else if(props.game === 3) {
                store.commit(
                    "updateGameObject",
                    new ReversiGameMap(canvas.value.getContext('2d'), parent.value, store)
                );
            }
        });

        return {
            parent,
            canvas,
        }
    }
}
</script>

<style scoped>
div.gamemap {
    width: 100%;
    height: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
}

div.gamemap > canvas {
    outline:none;
}
</style>