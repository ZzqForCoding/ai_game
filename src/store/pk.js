export default {
  state: {
    status: "matching", // matching表示匹配界面，playing表示对战界面
    socket: null,
    opponent_username: "",
    opponent_photo: "",
    gamemap: null,
    a_id: 0,
    a_sx: 0,
    a_sy: 0,
    b_id: 0,
    b_sx: 0,
    b_sy: 0,
    gameObject: null,
    loser: "none",
    type: "none",
    msgs: [],
    canSendMsg: false,
  },
  getters: {
  },
  mutations: {
    updateSocket(state, socket) {
        state.socket = socket;
    },
    updateOpponent(state, opponent) {
        state.opponent_username = opponent.username;
        state.opponent_photo = opponent.photo;
    },
    updateStatus(state, status) {
        state.status = status;
    },
    updateGame(state, game) {
        state.gamemap = game.map;
        state.a_id = game.a_id;
        state.a_sx = game.a_sx;
        state.a_sy = game.a_sy;
        state.b_id = game.b_id;
        state.b_sx = game.b_sx;
        state.b_sy = game.b_sy;
    },
    updateGameObject(state, gameobject) {
        state.gameObject = gameobject;
    },
    updateGameResult(state, result) {
        state.loser = result.loser;
        state.type = result.status;
    },
    pushMsg(state, msg) {
        msg.id = state.msgs.length + 1;
        state.msgs.push(msg);
    },
    clearMsg(state) {
        state.msgs = [];
    },
    updateCanSendMsg(state, canSendMsg) {
        state.canSendMsg = canSendMsg;
    }
  },
  actions: {
 
  },
  modules: {
  }
}
