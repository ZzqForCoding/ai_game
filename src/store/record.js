import { ElNotification, ElMessage } from 'element-plus';
import { h } from 'vue';

export default {
    state: {
        hall_socket_url: "wss://aigame.zzqahm.top/wss/hall/?token=",
        hall_socket: null,
        hall_socket_heartbeat: null,
        hall_msgs: [],
        hall_can_send_msg: false,
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
                state.hall_can_send_msg = false;
                state.hall_socket.close();
            }
            state.hall_socket = socket;
        },
        updateHallSocketHeartbeat(state, hall_socket_heartbeat) {
            if(state.hall_socket_heartbeat) clearInterval(state.hall_socket_heartbeat);
            state.hall_socket_heartbeat = hall_socket_heartbeat;
        },
        updateHallCanSendMsg(state, hall_can_send_msg) {
            state.hall_can_send_msg = hall_can_send_msg;
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
        connectHallSocket(context) {
            let state = context.rootState;
            if(!state.record.hall_socket && state.user.is_login) {
                context.commit("updateHallSocket", new WebSocket(state.record.hall_socket_url + state.user.access));
                state.record.hall_socket.onopen = () => {
                    console.log("connected!");
                    ElMessage({
                        message: 'websocket连接成功',
                        type: 'success',
                    });
                };

                state.record.hall_socket.onmessage = msg => {
                    const data = JSON.parse(msg.data);
                    if(data.event === "hall_message") {
                        context.commit("pushHallMsg", data.msg);
                    } else if(data.event === "notification") {
                        ElNotification({
                            title: data.data.title,
                            message: h('i', { style: 'color: teal' }, "您的动态【" + data.data.msg + "】被【" + data.data.username + "】回复!"),
                        })
                    } else if(data.event === "verifycode_error") {
                        ElMessage({
                            showClose: true,
                            message: data.data.msg,
                            type: 'error',
                        })
                    }
                }

                state.record.hall_socket.onclose = () => {
                    console.log("disconnected!");
                    ElMessage({
                        message: 'websocket连接断开，请刷新页面或重新登录！',
                        type: 'warning',
                    })
                    context.commit("updateHallSocket", null);
                    context.commit("updateHallSocketHeartbeat", null);
                }
                let func = setInterval(() => {
                    state.record.hall_socket.send(JSON.stringify({
                        event: "heartbeat",
                        userId: state.user.id,
                    }));
                }, 4.75 * 60 * 1000);
                context.commit("updateHallSocketHeartbeat", func);
                context.commit("updateHallCanSendMsg", true);
            }
        }
    },
    modules: {
    }
  }
  