<template>
    <ContentField>
        <el-row>
            <el-col :span="8" :offset="8">
                <el-form :model="register_info" :rules="rules" ref="ruleForm" label-width="50px" label-position="top" style="user-select: none;">
                    <el-form-item label="帐号" prop="username">
                        <el-input v-model="register_info.username" placeholder="请输入账号" clearable />
                    </el-form-item>
                    <el-form-item label="密码" prop="password">
                        <el-input type="password" v-model="register_info.password" placeholder="请输入密码" clearable />
                    </el-form-item>
                    <el-form-item label="确认密码" prop="password_confirm">
                        <el-input type="password" v-model="register_info.password_confirm" placeholder="请输入确认密码" clearable />
                    </el-form-item>
                    <PasswordStrength v-model:passwordStr="register_info.password" style="padding-top: 10px;"></PasswordStrength>
                    <SliderVerify prop="isLock" v-model="register_info.isLock" @change="handlerLock" class="verify" />
                    <el-form-item>
                        <el-button type="primary" @click="register" style="width: 100%;">注册</el-button>
                    </el-form-item>
                </el-form>
            </el-col>
        </el-row>
    </ContentField>
</template>

<script>
import ContentField from '@/components/ContentField.vue'
import SliderVerify from '@/components/SliderVerify.vue'
import PasswordStrength  from '@/components/PasswordStrength.vue';
import { ref, reactive, unref } from 'vue';
import { useStore } from 'vuex';
import router from '@/router';
import $ from 'jquery';
import { ElMessage } from 'element-plus';

export default {
    name: 'UserAccountRegisterView',
    components: {
        ContentField,
        SliderVerify,
        PasswordStrength,
    },
    setup() {
        const store = useStore();
        const ruleForm = ref(null);
        let register_info = reactive({
            username: '',
            password: '',
            password_confirm: '',
            isLock: false,
        });

        const register = async() => {
            const form = unref(ruleForm);
            await form.validate((valid) => {
                if(register_info.isLock === false) {
                    ElMessage({
                        showClose: true,
                        message: '请拖动滑块完成验证',
                        type: 'error',
                    });
                    return;
                }
                if(valid) {
                    $.ajax({
                        url: "https://aigame.zzqahm.top/backend/player/register/",
                        type: "post",
                        data: register_info,
                        success(resp) {
                            if(resp.result === "success") {
                                store.dispatch("login", {
                                    username: register_info.username,
                                    password: register_info.password,
                                    success() {
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
                                    }
                                });
                            } else {
                                ElMessage({
                                    showClose: true,
                                    message: resp.result,
                                    type: 'error',
                                })
                            }
                        },
                        error() {
                        }
                    });
                }
            })
        };

        const handlerLock = async(data) => {
            if(data) {
                if(register_info.username === '' || register_info.password === '' || register_info.password_confirm === '' ||
                   !register_info.username || !register_info.password || !register_info.password_confirm) {
                    ElMessage({
                        showClose: true,
                        message: '请先输入用户名密码！',
                        type: 'error',
                    });
                }
                register_info.isLock = true;
                const form = unref(ruleForm);
                await form.validateField('isLock');
            }
        };

        const checkStatus = (rule, value, callback) => {
            if (!value) {
                return callback(new Error("请拖动滑块完成验证"));
            } else {
                if (register_info.username === '' || register_info.password === '' || register_info.password_confirm === '' ||
                   !register_info.username || !register_info.password || !register_info.password_confirm) {
                    setTimeout(() => {
                        register_info.isLock = false;
                        register_info.validateField('username');
                        register_info.validateField('password');
                        register_info.validateField('password_confirm');
                        return callback(new Error("验证未通过"));
                    }, 1);
                }
                callback();
            }
        };

        return {
            ruleForm,
            register_info,
            register,
            handlerLock,
            rules: {
                username: [
                    { required: true, message: '用户名称不得为空！', trigger: 'blur' },
                    { min: 3, max: 18, message: '长度在 3 到 18 个字符', trigger: 'blur' }
                ],
                password: [
                    { required: true, message: '密码不得为空！', trigger: 'blur' },
                    { min: 6, max: 18, message: '长度在 6 到 18 个字符', trigger: 'blur' }
                ],
                password_confirm: [
                    { required: true, message: '确认密码不得为空！', trigger: 'blur' },
                    { min: 6, max: 18, message: '长度在 6 到 18 个字符', trigger: 'blur' }
                ],
                isLock: [
                    { validator: checkStatus, trigger: 'blur' },
                ],
            },

        };
    }
}
</script>

<style scoped>
.password-progress {
    margin-top: 10px;
}
.verify {
    margin-bottom: 15px;
}
</style>