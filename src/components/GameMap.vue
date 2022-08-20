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
import { GameMap as GobangGameMap } from '@/assets/scripts/gobang/GameMap';
import { useStore } from 'vuex';

export default {
    name: 'GameMap',
    components: {
        ResultBoard,
    },
    props: {
        game: {
            type: String,
            required: true,
        }
    },
    setup(props) {
        const store = useStore();
        let parent = ref(null);
        let canvas = ref(null);

        onMounted(() => {
            store.commit("updateLoser", 'none');
            if(props.game === "绕蛇") {
                store.commit(
                    "updateGameObject",
                    new SnakeGameMap(canvas.value.getContext('2d'), parent.value, store)
                );
            } else if(props.game === "五子棋") {
                new GobangGameMap(canvas.value.getContext('2d'), parent.value);
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