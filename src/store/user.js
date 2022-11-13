import $ from 'jquery';
import router from '@/router';

export default {
    state: {
        id: JSON.parse(localStorage.getItem('user')) === null ? 0 : JSON.parse(localStorage.getItem('user')).id,
        username: JSON.parse(localStorage.getItem('user')) === null ? "" : JSON.parse(localStorage.getItem('user')).username,
        photo: JSON.parse(localStorage.getItem('user')) === null ? "" : JSON.parse(localStorage.getItem('user')).photo,
        access: localStorage.getItem('aigame.access') === null ? "" : localStorage.getItem('aigame.access'),
        refresh: localStorage.getItem('aigame.refresh') === null ? "" : localStorage.getItem('aigame.refresh'),
        is_login: JSON.parse(localStorage.getItem('user')) === null ? false : JSON.parse(localStorage.getItem('user')).is_login,
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

            localStorage.setItem("user",  JSON.stringify(user));
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
        setIntervalFunc(state, interval_func) {
            let t = localStorage.getItem('setIntervalFunc');
            if(t !== null) {
                clearInterval(t);
            }
            state.interval_func = interval_func;
            localStorage.setItem("setIntervalFunc", interval_func);
        },
        updatePhoto(state, imgUrl) {
            state.photo = imgUrl;
        },
    },
    actions: {
        login(context, data) {
            $.ajax({
                url: "https://aigame.zzqahm.top/backend/player/token/",
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
                error() {
                    context.dispatch("logout");
                }
            });
        },
        getinfo(context, data) {
            $.ajax({
                url: "https://aigame.zzqahm.top/backend/player/getinfo/",
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
                error() {
                    context.dispatch("logout");
                }
            });
        },
        logout(context) {
            clearInterval(localStorage.getItem("setIntervalFunc"));
            localStorage.removeItem("aigame.access");
            localStorage.removeItem("aigame.refresh");
            localStorage.removeItem("setIntervalFunc")
            localStorage.removeItem("user");
            
            context.commit("logout");
            router.push({ name: "user_account_login" });
        },
        refresh_access(context, refresh) {
            // 每4.5min刷新jwt
            let func = setInterval(() => {
                $.ajax({
                    url: "https://aigame.zzqahm.top/backend/player/token/refresh/",
                    type: "post",
                    data: {
                        refresh,
                    },
                    success(resp) {
                        // 若直接更新state更新不成功，需要使用mutations中的方法进行更新
                        context.commit("updateToken", {
                            access: resp.access,
                            refresh,
                        });
                        $.ajax({
                            url: "https://aigame.zzqahm.top/backend/player/token/update/",
                            type: "post",
                            headers: {
                                "Authorization": "Bearer " + resp.access,
                            },
                            data: {
                                token: resp.access,
                            },
                            error() {
                                context.dispatch("logout");
                            }
                        });
                    },
                    error() {
                        context.dispatch("logout");
                    }
                });
            }, 55 * 60 * 1000);
            context.commit("setIntervalFunc", func);
        },    
    },
    modules: {
    }
}