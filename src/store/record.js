export default {
    state: {
        hall_socket_url: "wss://aigame.zzqahm.top/wss/hall/?token=",
        hall_socket: null,
        hall_socket_heartbeat: null,
        hall_msgs: [],
        is_record: false,
        a_steps: "",
        b_steps: "",
        record_loser: "",
        a_username: "",
        a_photo: "",
        b_username: "",
        b_photo: "",
        a_is_robot: false,
        b_is_robot: false,
        a_language: "",
        b_language: "",
    },
    getters: {
    },
    mutations: {
        updateHallSocket(state, socket) {
            if(!socket && state.hall_socket !== null) {
                clearInterval(state.hall_socket_heartbeat);
                state.hall_socket.close();
            }
            state.hall_socket = socket;
        },
        updateHallSocketHeartbeat(state, hall_socket_heartbeat) {
            state.hall_socket_heartbeat = hall_socket_heartbeat;
        },
        pushHallMsg(state, msg) {
            msg.id = state.hall_msgs.length + 1;
            state.hall_msgs.push(msg);
        },      
        updateIsRecord(state, is_record) {
            state.is_record = is_record;
        },
        updateSteps(state, data) {
            state.a_steps = data.a_steps;
            state.b_steps = data.b_steps;
        },
        updateRecordLoser(state, loser) {
            state.record_loser = loser;
        },
        updatePlayerInfo(state, data) {
            state.a_username = data.a_username;
            state.a_photo = data.a_photo;
            state.a_language = data.a_language;
            state.b_username = data.b_username;
            state.b_photo = data.b_photo;
            state.b_language = data.b_language;
        },
        updateIsRobot(state, data) {
            state.a_is_robot = Boolean(data.a_is_robot);
            state.b_is_robot = Boolean(data.b_is_robot);
        },
    },
    actions: {
   
    },
    modules: {
    }
  }
  