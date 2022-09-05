export default {
    state: {
        hall_socket: null,
        hall_msgs: [],
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
    },
    actions: {
   
    },
    modules: {
    }
  }
  