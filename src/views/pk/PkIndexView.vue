<template>
    <PlayGround :game="game">
        
    </PlayGround>
</template>

<script>
import PlayGround from '@/components/PlayGround.vue'
import { useRoute } from 'vue-router';

export default {
    name: 'PkIndexView',
    components: {
        PlayGround,
    },
    setup() {
        const route = useRoute();
        const game = route.params.game;

        return {
            game,
        }
    }
}
</script>

<style scoped>

</style>