<template>
    <ContentField>
        <el-row>
            <el-col :span="8" :offset="8">
                <el-form ref="phoneForm" :model="phone_info" :rules="phone_rules" label-width="50px" label-position="top" style="user-select: none;" v-if="!isVerifySuccess">
                    <el-form-item label="手机号" prop="phone">
                        <el-input placeholder="Please input phone" clearable v-model="phone_info.phone">
                            <template #append>
                                <el-button>
                                    <span v-if="$store.state.utils.showVerifyCode">已发送({{ $store.state.utils.verifyCodeTime }})</span>
                                    <span v-else @click="send_msg">发送验证码</span>
                                </el-button>
                            </template>
                        </el-input>
                    </el-form-item>
                    <el-form-item label="验证码" prop="code">
                        <el-input oninput ="value=value.replace(/[^\d]/g,'')" placeholder="Please input verification code" clearable v-model="phone_info.code" />
                    </el-form-item>
                    <SliderVerify prop="isLock" v-model="password_info.isLock" @change="handlerLock" class="verify" @checkVal="checkVal" />
                    <div class="verify-code-prompt" v-if="$store.state.utils.showVerifyCode">验证码在5分钟内有效，请及时填写！</div>
                    <el-form-item>
                        <el-button type="primary" style="width: 100%;" @click="enterUpdatePassword">修改密码</el-button>
                    </el-form-item>
                </el-form>
                <el-form ref="passwordForm" :model="password_info" :rules="password_rules" label-width="50px" label-position="top" style="user-select: none;" v-else>
                    <el-form-item label="密码" prop="password">
                        <el-input type="password" placeholder="Please input password" clearable v-model="password_info.password" />
                    </el-form-item>
                    <el-form-item label="确认密码" prop="password_confirm">
                        <el-input type="password"  placeholder="Please input again" clearable v-model="password_info.password_confirm" />
                    </el-form-item>
                    <PasswordStrength v-model:passwordStr="password_info.password" style="padding-top: 10px;"></PasswordStrength>
                    <el-form-item>
                        <el-button type="primary" style="width: 100%;" @click="update_password">确认修改</el-button>
                    </el-form-item>
                </el-form>
            </el-col>
        </el-row>
    </ContentField>
</template>

<script>
import ContentField from '@/components/ContentField.vue';
import { GameUtils } from '@/assets/scripts/GameUtils';
import PasswordStrength  from '@/components/PasswordStrength.vue';
import SliderVerify from '@/components/SliderVerify.vue'
import { useStore } from 'vuex'; 
import { ref, unref, reactive, onMounted } from 'vue';
import { ElMessage } from 'element-plus';
import $ from 'jquery';
import router from '@/router/index'

export default {
    name: 'UserAccountUpdatePasswordView',
    components: {
        ContentField,
        PasswordStrength,
        SliderVerify,
    },
    setup() {
        const store = useStore();
        let phoneForm = ref(null);
        let passwordForm = ref(null);
        let phone_info = reactive({
            phone: '',
            code: '',
        });
        let password_info = reactive({
            password: '',
            password_confirm: '',
            state: '',
            isLock: false,
        });
        let isVerifySuccess = ref(false);

        onMounted(() => {
            if(store.state.utils.gameUtils === null) {
                store.commit("updateGameUtils", new GameUtils(store));
            }
        });

        const send_msg = () => {
            store.dispatch("send_msg", {
                phone: phone_info.phone,
                flag: "update_password",
            });
        }

        const enterUpdatePassword = async() => {
            const form = unref(phoneForm);
            await form.validate(valid => {
                if(password_info.isLock === false) {
                    ElMessage({
                        showClose: true,
                        message: '请拖动滑块完成验证',
                        type: 'error',
                    });
                    return;
                }
                if(valid) {
                    $.ajax({
                        url: "https://aigame.zzqahm.top/backend/player/verify_code/",
                        type: "post",
                        data: {
                            phone: phone_info.phone,
                            code: phone_info.code,
                        },
                        success(resp) {
                            if (resp.result === "success") {
                                isVerifySuccess.value = true;
                                password_info.state = resp.state;
                                ElMessage({
                                    showClose: true,
                                    message: '验证成功，请在五分钟内修改好密码！',
                                    type: 'success',
                                });
                            } else {
                                ElMessage({
                                    showClose: true,
                                    message: resp.result,
                                    type: 'error',
                                })
                            }
                        },
                    });
                }
            })
        }

        const update_password = async() => {
            const form = unref(passwordForm);
            await form.validate((valid) => {
                if(valid) {
                    $.ajax({
                        url: "https://aigame.zzqahm.top/backend/player/update_password/",
                        type: "post",
                        data: {
                            state: password_info.state,
                            password: password_info.password,
                            password_confirm: password_info.password_confirm,
                        },
                        success(resp) {
                            if (resp.result === "success") {
                                ElMessage({
                                    showClose: true,
                                    message: '修改成功，快去登陆吧！',
                                    type: 'success',
                                });
                                router.push({name: 'user_account_login'});
                            } else {
                                ElMessage({
                                    showClose: true,
                                    message: resp.result,
                                    type: 'error',
                                })
                            }
                        },
                    });
                }
            })
        }

        const checkPasswordPower = (rule, value, callback) => {
            if(!/[a-zA-Z0-9]{6,}/.test(value)) {
                return callback(new Error("密码未达到强度"));
            }
            callback();
        };

        const checkPhoneValid = (rule, value, callback) => {
            if(!/^1[3-9]\d{9}$/.test(value)) {
                return callback(new Error("不是合法的电话号码"));
            }
            callback();
        }

        const handlerLock = (data) => {
            if(data) {
                password_info.isLock = true;
            }
        };

        const checkVal = async(callback) => {
            const form = unref(phoneForm);
            await form.validate(valid => {
                if(valid) {
                    callback(true);
                } else {
                    callback(false);
                }
            })
        };

        return {
            phone_info,
            password_info,
            phoneForm,
            passwordForm,
            send_msg,
            isVerifySuccess,
            enterUpdatePassword,
            handlerLock,
            checkVal,
            update_password,
            phone_rules: {
                phone: [
                    { required: true, message: '手机号不得为空！', trigger: 'blur' },
                    { validator: checkPhoneValid, trigger: 'blur' },
                ],
                code: [
                    { required: true, message: '验证码不得为空！', trigger: 'blur' },
                    { min: 4, max: 4, message: '请输入4为数字', trigger: 'blur' },
                ],
            },
            password_rules: {
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
.verify-code-prompt {
    margin-bottom: 18px;
    text-align: float;
    color: #666;
    font-size: 13px;
    font-weight: 600;
}

.verify {
    margin-bottom: 15px;
}
</style>