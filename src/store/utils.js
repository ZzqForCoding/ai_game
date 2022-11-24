import $ from 'jquery';

export default {
    state: {
        gameUtils: null,
        matchTime: 0,
        isMatch: false,
        verifyCodeTime: 300,
        showVerifyCode: false,
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
        updateShowVerifyCode(state, showVerifyCode) {
            state.gameUtils.initVerifyCodeTime();
            state.showVerifyCode = showVerifyCode;
        },
        updateVerifyCodeTime(state, verifyCodeTime) {
            state.verifyCodeTime = verifyCodeTime;
        },
    },
    actions: {
        uploadImage(context, data) {
            //填写获取签名的地址
            const getPolicyApiUrl = 'https://aigame.zzqahm.top/backend/player/img/apply/'; //获取oss签名的地址
            $.ajax({
                url: getPolicyApiUrl, 
                type: "GET",
                data: {
                    'filename': data.file.name,
                    'userId': data.userId,
                },
                success: resp => {
                    resp = $.parseJSON(resp)
                    let ossUrl = "https://player-avatar.oss-cn-shenzhen.aliyuncs.com";
                    let pos = data.file.name.lastIndexOf('.');
                    let fileName = ([1e7]+-1e3+-4e3+-8e3+-1e11).replace(/[018]/g, c => (c ^ crypto.getRandomValues(new Uint8Array(1))[0] & 15 >> c / 4).toString(16)) + data.file.name.substr(pos);
                    let accessUrl = resp.dir + '/' + fileName;
                    let sendData = new FormData();
                    sendData.append("OSSAccessKeyId", resp.accessid);
                    sendData.append("policy", resp.policy);
                    sendData.append("signature", resp.signature);
                    sendData.append("keys", resp.dir);
                    sendData.append("callback", resp.callback);
                    sendData.append("key", accessUrl);
                    sendData.append('success_action_status', 200); // 指定返回的状态码
                    sendData.append('type', data.file.type);
                    sendData.append('file', data.file);
                    $.ajax({
                        url: ossUrl, 
                        type: "POST",
                        cache: false,
                        contentType: false,
                        processData: false,
                        data: sendData,
                        success(resp) {
                            data.success(resp.imgUrl, fileName);
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
        },
        // 根据id获取gameIntro
        getGameIntro(context, data) {
            $.ajax({
                url: "https://aigame.zzqahm.top/backend/playervoice/game_intro/get/" + data.id,
                type: "get",
                success(resp) {
                    data.success(resp);
                },
                error() {
                    context.dispatch("logout");
                }
            });
        }
    },
    modules: {
    }
}
  