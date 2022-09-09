export default {
    state: {
        hall_socket: null,
        hall_msgs: [],
        is_record: false,
        a_steps: "",
        b_steps: "",
        record_loser: "",
    },
    getters: {
    },
    mutations: {
        updateHallSocket(state, socket) {
            state.hall_socket = socket;
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
        }
    },
    actions: {
   
    },
    modules: {
    }
  }
  