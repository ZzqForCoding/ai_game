<template>
    <div>
        
    </div>
</template>
 
<script>
import router from '@/router/index';
import { useRoute } from 'vue-router';
import { useStore } from 'vuex';
import $ from 'jquery';
import { ElMessage } from 'element-plus';
 
export default {
    name: 'UserAccountQQReceiveCodeView',
    setup() {
        const myRoute = useRoute();
        const store = useStore();

        $.ajax({
            url: "https://aigame.zzqahm.top/backend/player/qq/receive_code/", 
            type: "GET",
            data: {
                code: myRoute.query.code,
                state: myRoute.query.state
            },
            success(resp) {
                if(resp.result === "success") {
                    store.commit("updateToken", {
                        access: resp.access,
                        refresh: resp.refresh,
                    });
                    store.dispatch("refresh_access", resp.refresh);
                    ElMessage({
                        showClose: true,
                        message: '登录成功！',
                        type: 'success',
                    });
                    store.dispatch("getinfo", {
                        success() {
                            router.push({name: 'home'});
                        },
                        error() {
                            store.dispatch("logout");
                        }
                    });
                } else {
                    router.push({ name: "user_account_login" });
                }
            },
            error() {
            }
        });
    }
}
</script>
 
<style scoped>
 
</style>