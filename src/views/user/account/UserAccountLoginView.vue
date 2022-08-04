<template>
    <ContentField v-if="!$store.state.user.pulling_info">
        <div class="row justify-content-md-center">
            <div class="col-3">
                <form @submit.prevent="login">
                    <div class="mb-3">
                        <label for="username" class="form-label">用户名</label>
                        <input type="text" class="form-control" id="username" placeholder="请输入用户名" v-model="username">
                    </div>
                    <div class="mb-3">
                        <label for="password" class="form-label">密码</label>
                        <input type="password" class="form-control" id="password" placeholder="请输入密码" v-model="password">
                    </div>
                    <div class="error-message">
                        {{ error_message}}
                    </div>
                    <button type="submit" class="btn btn-primary">提交</button>
                </form>
            </div>
        </div>
    </ContentField>
</template>

<script>
import ContentField from '@/components/ContentField.vue'
import { ref } from 'vue'
import { useStore } from 'vuex'
import router from '@/router'

export default {
    name: 'UserAccountLoginView',
    components: {
        ContentField,
    },
    setup() {
        const store = useStore();
        let username = ref(null);
        let password = ref(null);
        let error_message = ref('');

        const access = localStorage.getItem("aigame.access");
        const refresh = localStorage.getItem("aigame.refresh");
        if(access && refresh) {
            store.commit("updateToken", {
                access,
                refresh,
            })
            store.dispatch("getinfo", {
                success() {
                    router.push({name: "home"});
                    store.commit("updatePullingInfo", false);
                },
                error() {
                    store.commit("updatePullingInfo", false);
                }
            })
        } else {
            store.commit("updatePullingInfo", false);
        }
        

        const login = () => {
            error_message.value = "";
            store.dispatch("login", {
                username: username.value,
                password: password.value,
                success() {
                    store.dispatch("getinfo", {
                        success() {
                            router.push({name: 'home'});
                        }
                    });
                },
                error() {
                    error_message.value = "用户名或密码错误";
                }
            });
        };

        return {
            username,
            password,
            error_message,
            login,
        };
    }
}
</script>

<style scoped>
.error-message {
    color: red;
}
</style>