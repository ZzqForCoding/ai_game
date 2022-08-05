import $ from 'jquery';

export default {
    state: {
        id: 0,
        username: "",
        photo: "",
        access: "",
        refresh: "",
        is_login: false,
        pulling_info: true, // 是否在拉取信息
        interval_func: 0,
    },
    getters: {
    },
    mutations: {
        updateUser(state, user) {
            state.id = user.id;
            state.username = user.username;
            state.photo = user.photo;
            state.is_login = user.is_login;
        },
        updateToken(state, data) {
            localStorage.setItem("aigame.access", data.access);
            localStorage.setItem("aigame.refresh", data.refresh);
            state.access = data.access;
            state.refresh = data.refresh;
        },
        logout(state) {
            state.id = 0;
            state.username = "";
            state.photo = "";
            state.access = "";
            state.refresh = "";
            state.is_login = false;
        },
        updatePullingInfo(state, pulling_info) {
            state.pulling_info = pulling_info;
        },
        setIntervalFunc(state, interval_func) {
            let t = localStorage.getItem('interval_func');
            if(t !== null) {
                clearInterval(t);
            }
            state.interval_func = interval_func;
            localStorage.setItem("setIntervalFunc", interval_func);
        },
    },
    actions: {
        login(context, data) {
            $.ajax({
                url: "https://aigame.zzqahm.top/player/token/",
                type: "post",
                data: {
                    username: data.username,
                    password: data.password,
                },
                success(resp) {
                    context.commit("updateToken", resp);
                    context.dispatch("refresh_access", resp.refresh);
                    data.success(resp);
                },
                error(resp) {
                    data.error(resp);
                }
            });
        },
        getinfo(context, data) {
            $.ajax({
                url: "https://aigame.zzqahm.top/player/getinfo/",
                type: "get",
                headers: {
                    "Authorization": "Bearer " + context.state.access,
                },
                success(resp) {
                    if(resp.result === "success") {
                        context.commit("updateUser", {
                            ...resp,
                            is_login: true,
                        });
                        data.success();
                    } else {
                        data.error();
                    }
                },
                error(resp) {
                    data.error(resp);
                }
            });
        },
        logout(context) {
            localStorage.removeItem("aigame.access");
            localStorage.removeItem("aigame.refresh");
            
            clearInterval(localStorage.getItem("setIntervalFunc"));
            context.commit("logout");
        },
        refresh_access(context, refresh) {
            // 每4.5min刷新jwt
            let func = setInterval(() => {
                $.ajax({
                    url: "https://aigame.zzqahm.top/player/token/refresh/",
                    type: "post",
                    data: {
                        refresh: refresh,
                    },
                    success(resp) {
                        context.state.access = resp.access;
                    }
                });
            }, 4.5 * 60 * 1000);
            context.commit("setIntervalFunc", func);
        },    
    },
    modules: {
    }
}