<template>
    <div class="gamemap" ref="parent">
        <canvas ref="canvas" tabindex="0" @contextmenu.prevent="" style="height: 100%;"></canvas>
    </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { GameMap as SnakeGameMap } from '@/assets/scripts/Snake/GameMap';
import { GameMap as GobangGameMap } from '@/assets/scripts/gobang/GameMap';

export default {
    name: 'GameMap',
    props: {
        game: {
            type: String,
            required: true,
        }
    },
    setup(props) {
        let parent = ref(null);
        let canvas = ref(null);

        onMounted(() => {
            if(props.game === "绕蛇") {
                console.log(123);
                new SnakeGameMap(canvas.value.getContext('2d'), parent.value);
            } else if(props.game === "五子棋") {
                console.log(456);
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