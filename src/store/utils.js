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
            state.matchTime = 0;
            state.gameUtils.initMatchTime();
            state.isMatch = isMatch;
        },
        updateMatchTime(state, matchTime) {
            state.matchTime = matchTime;
        },
    },
    actions: {

    },
    modules: {
    }
}
  