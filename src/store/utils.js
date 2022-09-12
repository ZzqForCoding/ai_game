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
            state.gameUtils.initMatchTime();
            state.isMatch = isMatch;
        },
        clearMatchTime(state, matchTime) {
            state.matchTime = matchTime;
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
  