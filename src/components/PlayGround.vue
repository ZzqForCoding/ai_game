<template>
    <div class="playground">
        <GameMap :game="game"></GameMap>
    </div>
</template>

<script>
import GameMap from './GameMap.vue'

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