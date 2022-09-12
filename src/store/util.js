export default {
    state: {
        gameUtils: null,
        matchTime: 0,
        isMatch: false,
    },
    getters: {
    },
    mutations: {
        updateGameUtils(state, gameUtils) {
            state.gameUtils = gameUtils;
        },
        updateIsMatch(state, isMatch) {
            state.isMatch = isMatch;
        },
        updateAddMatchTime(state, matchTime) {
            state.matchTime = matchTime;
        },
    },
    actions: {

    },
    modules: {
    }
}
  