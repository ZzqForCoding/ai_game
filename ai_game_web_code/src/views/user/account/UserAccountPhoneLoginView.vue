<template>
    <ContentField>
        <el-row>
            <el-col :span="8" :offset="8">
                <el-form ref="loginForm" :model="log_info" :rules="rules" label-width="50px" label-position="top" style="user-select: none;">
                    <el-form-item label="手机号" prop="phone">
                        <el-input placeholder="Please input phone" clearable v-model="log_info.phone">
                            <template #append>
                                <el-button>
                                    <span v-if="$store.state.utils.showVerifyCode">已发送({{ $store.state.utils.verifyCodeTime }})</span>
                                    <span v-else @click="send_msg">发送验证码</span>
                                </el-button>
                            </template>
                        </el-input>
                    </el-form-item>
                    <el-form-item label="验证码" prop="code">
                        <el-input oninput ="value=value.replace(/[^\d]/g,'')" placeholder="Please input verification code" clearable v-model="log_info.code" />
                    </el-form-item>
                    <SliderVerify prop="isLock" v-model="log_info.isLock" @change="handlerLock" class="verify" @checkVal="checkVal" />
                    <div class="verify-code-prompt" v-if="$store.state.utils.showVerifyCode">验证码在5分钟内有效，请及时填写！</div>
                    <el-form-item>
                        <el-button type="primary" style="width: 100%;" @click="phone_login">登录</el-button>
                    </el-form-item>
                </el-form>
            </el-col>
        </el-row>
    </ContentField>
</template>

<script>
import ContentField from '@/components/ContentField.vue';
import { GameUtils } from '@/assets/scripts/GameUtils';
import SliderVerify from '@/components/SliderVerify.vue'
import { useStore } from 'vuex'; 
import { unref, ref, reactive, onMounted } from 'vue';
import { ElMessage } from 'element-plus';
import $ from 'jquery';

export default {
    name: 'UserAccountPhoneLoginView',
    components: {
        ContentField,
        SliderVerify,
    },
    setup() {
        const store = useStore();
        let loginForm = ref(null);
        let log_info = reactive({
            phone: '',
            code: '',
            isLock: false,
        });

        onMounted(() => {
            if(store.state.utils.gameUtils === null) {
                store.commit("updateGameUtils", new GameUtils(store));
            }
        });

        const send_msg = () => {
            store.dispatch("send_msg", {
                phone: log_info.phone,
                flag: "login",
            });
        }

        const phone_login = async() => {
            const form = unref(loginForm);
            await form.validate(valid => {
                if(log_info.isLock === false) {
                    ElMessage({
                        showClose: true,
                        message: '请拖动滑块完成验证',
                        type: 'error',
                    });
                    return;
                }
                if(valid) {
                    $.ajax({
                        url: "https://aigame.zzqahm.top/backend/player/phone_login/",
                        type: "POST",
                        data: {
                            phone: log_info.phone,
                            code: log_info.code,
                        },
                        success(resp) {
                            if(resp.result === "success") {
                                store.dispatch("login_success", resp);
                                store.commit("updateShowVerifyCode", false);
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

        const handlerLock = (data) => {
            if(data) {
                log_info.isLock = true;
            }
        };

        const checkVal = async(callback) => {
            const form = unref(loginForm);
            await form.validate((valid) => {
                if(valid) {
                    callback(true);
                } else {
                    callback(false);
                }
            })
        };

        const checkPhoneValid = (rule, value, callback) => {
            if(!/^1[3-9]\d{9}$/.test(value)) {
                return callback(new Error("不是合法的电话号码"));
            }
            callback();
        }

        return {
            log_info,
            loginForm,
            send_msg,
            phone_login,
            handlerLock,
            checkVal,
            rules: {
                phone: [
                    { required: true, message: '手机号不得为空！', trigger: 'blur' },
                    { validator: checkPhoneValid, trigger: 'blur' },
                ],
                code: [
                    { required: true, message: '验证码不得为空！', trigger: 'blur' },
                    { min: 4, max: 4, message: '请输入4为数字', trigger: 'blur' },
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

.verify-code-prompt {
    margin-bottom: 18px;
    text-align: float;
    color: #666;
    font-size: 13px;
    font-weight: 600;
}
</style>