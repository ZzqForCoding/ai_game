<template>
    <ContentField>
        <el-row>
            <el-col :span="8" :offset="8">
                <el-form :model="register_info" :rules="rules" ref="ruleForm" label-width="50px" label-position="top" style="user-select: none;">
                    <el-form-item label="用户名" prop="username">
                        <el-input v-model="register_info.username" placeholder="请输入用户名" clearable />
                    </el-form-item>
                    <el-form-item label="密码" prop="password">
                        <el-input type="password" v-model="register_info.password" placeholder="请输入密码" clearable />
                    </el-form-item>
                    <el-form-item label="确认密码" prop="password_confirm">
                        <el-input type="password" v-model="register_info.password_confirm" placeholder="请输入确认密码" clearable />
                    </el-form-item>
                    <PasswordStrength v-model:passwordStr="register_info.password" style="padding-top: 10px;"></PasswordStrength>
                    <SliderVerify prop="isLock" v-model="register_info.isLock" @change="handlerLock" class="verify" @checkVal="checkVal" />
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
                                    success(data) {
                                        store.dispatch("login_success", data);
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

        const handlerLock = (data) => {
            if(data) {
                register_info.isLock = true;
            }
        };

        const checkPasswordPower = (rule, value, callback) => {
            if(!/[a-zA-Z0-9]{6,}/.test(value)) {
                return callback(new Error("密码未达到强度"));
            }
            callback();
        };

        const checkVal = async(callback) => {
            const form = unref(ruleForm);
            await form.validate((valid) => {
                if(valid) {
                    callback(true);
                } else {
                    callback(false);
                }
            })
        };

        return {
            ruleForm,
            register_info,
            register,
            handlerLock,
            checkVal,
            rules: {
                username: [
                    { required: true, message: '用户名不得为空！', trigger: 'blur' },
                    { min: 3, max: 18, message: '长度在 3 到 18 个字符', trigger: 'blur' }
                ],
                password: [
                    { required: true, message: '密码不得为空！', trigger: 'blur' },
                    { min: 6, max: 18, message: '长度在 6 到 18 个字符', trigger: 'blur' },
                    { validator: checkPasswordPower, trigger: 'blur' },
                ],
                password_confirm: [
                    { required: true, message: '确认密码不得为空！', trigger: 'blur' },
                    { min: 6, max: 18, message: '长度在 6 到 18 个字符', trigger: 'blur' }
                ],
            },

        };
    }
}
</script>

<style scoped>
.verify {
    margin-bottom: 15px;
}
</style>