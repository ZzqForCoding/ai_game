<template>
    <ContentField>
        <div class="row justify-content-md-center">
            <div class="col-3">
                <form @submit.prevent="register">
                    <div class="mb-3">
                        <label for="username" class="form-label">用户名</label>
                        <input type="text" class="form-control" id="username" placeholder="请输入用户名" v-model="username">
                    </div>
                    <div class="mb-3">
                        <label for="password" class="form-label">密码</label>
                        <input type="password" class="form-control" id="password" placeholder="请输入密码" v-model="password">
                    </div>
                    <div class="mb-3">
                        <label for="password_confirm" class="form-label">确认密码</label>
                        <input type="password" class="form-control" id="password_confirm" placeholder="请输入确认密码" v-model="password_confirm">
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
import { ref } from 'vue';
import { useStore } from 'vuex';
import router from '@/router';
import $ from 'jquery';

export default {
    name: 'UserAccountRegisterView',
    components: {
        ContentField,
    },
    setup() {
        const store = useStore();
        let username = ref(null);
        let password = ref(null);
        let password_confirm = ref(null);
        let error_message = ref('');

        const register = () => {
            error_message.value = "";
            $.ajax({
                url: "https://aigame.zzqahm.top/player/register/",
                type: "post",
                data: {
                    username: username.value,
                    password: password.value,
                    password_confirm: password_confirm.value,
                },
                success(resp) {
                    if(resp.result === "success") {
                        store.dispatch("login", {
                            username: username.value,
                            password: password.value,
                            success() {
                                store.dispatch("getinfo", {
                                    success() {
                                        router.push({name: 'home'});
                                    }
                                });
                            }
                        });
                    } else {
                        error_message.value = resp.result;
                    }
                }
            });

            return {

            }
        };

        return {
            username,
            password,
            password_confirm,
            error_message,
            register,
        };
    }
}
</script>

<style scoped>
div.error-message {
    color: red;
}
</style>