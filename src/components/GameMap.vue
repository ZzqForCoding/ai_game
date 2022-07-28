<template>
    <div class="gamemap" ref="parent">
        <canvas ref="canvas" tabindex="0" @contextmenu.prevent=""></canvas>
    </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { GameMap } from '@/assets/scripts/GameMap';

export default {
    name: 'GameMap',
    setup() {
        let parent = ref(null);
        let canvas = ref(null);

        onMounted(() => {
            new GameMap(canvas.value.getContext('2d'), parent.value);
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