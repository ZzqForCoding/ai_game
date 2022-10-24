export default {
  state: {
    status: "matching", // matching表示匹配界面，playing表示对战界面
    socket: null,
    opponent_username: "",
    opponent_photo: "",
    gamemap: null,
    a_id: 0,
    a_language: "",
    a_is_robot: false,
    b_id: 0,
    b_language: "",
    b_is_robot: false,
    aCnt: 2, 
    bCnt: 2,
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
    // 带地图类游戏
    updateSnakeGame(state, game) {
        state.gamemap = game.map;
        state.a_id = parseInt(game.a_id);
        state.a_language = game.a_language;
        state.a_is_robot = Boolean(game.a_is_robot);
        state.b_id = parseInt(game.b_id);
        state.b_language = game.b_language;
        state.b_is_robot = Boolean(game.b_is_robot);
    },
    // 棋类游戏(还没实现棋类代码，因此与上方函数缺少一些参数)
    updateChessGame(state, game) {
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
    updateChessCnt(state, data) {
        state.aCnt = data.aCnt;
        state.bCnt = data.bCnt;
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
