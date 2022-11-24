<template>
    <div>
        
    </div>
</template>
 
<script>
import router from '@/router/index';
import { useRoute } from 'vue-router';
import { useStore } from 'vuex';
import $ from 'jquery';
 
export default {
    name: 'UserAccountAcWingWebReceiveCodeView',
    setup() {
        const myRoute = useRoute();
        const store = useStore();
        
        $.ajax({
            url: "https://aigame.zzqahm.top/backend/player/acwing/web/receive_code/", 
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
                    router.push({name: 'record_index'});
                    store.commit("updatePullingInfo", false);
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