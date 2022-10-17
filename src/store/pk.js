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
    a_language: "",
    a_is_robot: false,
    b_id: 0,
    b_sx: 0,
    b_sy: 0,
    b_language: "",
    b_is_robot: false,
    gameObject: null,
    loser: "none",
    type: "none",
    msgs: [],
    canSendMsg: false,
    codeOutMsg: "",
    firstMove: null,
    dir: -1,
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
    updateSnakeGame(state, game) {
        state.gamemap = game.map;
        state.a_id = parseInt(game.a_id);
        state.a_sx = game.a_sx;
        state.a_sy = game.a_sy;
        state.a_language = game.a_language;
        state.a_is_robot = Boolean(game.a_is_robot);
        state.b_id = parseInt(game.b_id);
        state.b_sx = game.b_sx;
        state.b_sy = game.b_sy;
        state.b_language = game.b_language;
        state.b_is_robot = Boolean(game.b_is_robot);
    },
    updateGobangGame(state, game) {
        state.a_id = parseInt(game.a_id);
        state.b_id = parseInt(game.b_id);
        state.firstMove = game.current_round;
    },
    updateFirstMove(state, firstMove) {
        state.firstMove = firstMove;
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
    },
    addCodeOutMsg(state, codeOutMsg) {
        state.codeOutMsg += codeOutMsg;
    },
    clearCodeOutMsg(state) {
        state.codeOutMsg = "";
    },
    updateDir(state, dir) {
        state.dir = dir;
    },
  },
  actions: {
 
  },
  modules: {
  }
}
