<template>
    <ContentField>
        <el-row>
            <el-col :span="8" :offset="8">
                <el-form :model="log_info" :rules="rules" ref="ruleForm" label-width="50px" label-position="top"
                    style="user-select: none;">
                    <el-form-item label="帐号" prop="username">
                        <el-input v-model="log_info.username" placeholder="请输入账号" clearable />
                    </el-form-item>
                    <el-form-item label="密码" prop="password">
                        <el-input type="password" v-model="log_info.password" placeholder="请输入密码" clearable />
                    </el-form-item>
                    <!-- <el-form-item prop="isLock"> -->
                    <SliderVerify v-model="log_info.isLock" @change="handlerLock" class="verify" />
                    <!-- </el-form-item> -->
                    <!-- <div class="third-login">
                        <el-tooltip
                            class="box-item"
                            effect="dark"
                            content="AcWing一键登录"
                            placement="bottom"
                        >
                            <div @click="acwing_login">
                                <img src="https://cdn.acwing.com/media/article/image/2022/09/06/1_32f001fd2d-acwing_logo.png" alt="">
                            </div>
                        </el-tooltip>
                    </div> -->
                    <div class="third-login">
                        <el-tooltip class="box-item" effect="dark" content="QQ一键登录" placement="bottom">
                            <div @click="qq_login">
                                <img style="width: 25px;"
                                    src="https://wiki.connect.qq.com/wp-content/uploads/2013/10/03_qq_symbol-1-250x300.png"
                                    alt="">
                            </div>
                        </el-tooltip>
                    </div>
                    <el-form-item>
                        <el-button type="primary" @click="login" style="width: 100%;">登录</el-button>
                    </el-form-item>
                </el-form>
            </el-col>
        </el-row>
    </ContentField>
</template>

<script>
import ContentField from '@/components/ContentField.vue'
import SliderVerify from '@/components/SliderVerify.vue'
import { ref, reactive, unref } from 'vue'
import { useStore } from 'vuex'
import router from '@/router'
import { ElMessage } from 'element-plus'
import $ from 'jquery'

export default {
    name: 'UserAccountLoginView',
    components: {
        ContentField,
        SliderVerify,
    },
    setup() {
        const store = useStore();
        const ruleForm = ref(null);
        let log_info = reactive({
            username: '',
            password: '',
            isLock: false,
        });

        const login = async() => {
            const form = unref(ruleForm);
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
                    store.dispatch("login", {
                       ...log_info,
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
                         },
                        error() {
                           ElMessage({
                                showClose: true,
                                message: '用户名或密码错误！',
                                type: 'error',
                            });
                         }
                    });
                }
            })
        };
 
       const handlerLock = async(data) => {
            if (data) {
                if(log_info.username === '' || log_info.password === '' || !log_info.username || !log_info.password) {
                    ElMessage({
                        showClose: true,
                        messae: '请先输入用户名密码！',
                        type:  'error',
                    });
                }
                log_info.isLock = true;
                const form = unref(ruleForm);
                await form.validateField('isLock');
            }
        };

        const checkStatus = (rule, value, callback) => {
            if (!value) {
                return callback(new Error("请拖动滑块完成验证"));
            } else {
                if (log_info.username === '' || log_info.password === ''
                    || !log_info.username || !log_info.password) {
                    setTimeout(() => {
                        log_info.isLock = false;
                        log_info.validateField('username');
                        log_info.validateField('password');
                        return callback(new Error("验证未通过"));
                    }, 1);
                }
                callback();
            }
        };

        const acwing_login = () => {
            $.ajax({
                url: "https://aigame.zzqahm.top/backend/player/acwing/web/apply_code/",
                type: "GET",
                success(resp) {
                    if(resp.result === "success") {
                        window.location.replace(resp.apply_code_url)
                    }
                },
                error() {
                }
            });
        }

        const qq_login = () => {
            $.ajax({
                url: "https://aigame.zzqahm.top/backend/player/qq/apply_code/",
                success(resp) {
                    if(resp.result === "success") {
                        window.location.replace(resp.apply_code_url)
                    }
                },
                error() {
                }
            });
         }

        return {
            ruleForm,
            log_info,
            login,
            handlerLock,
            rules: {
                username: [
                    { required: true, message: '用户名称不得为空！', trigger: 'blur' },
                    // { min: 3, max: 18, message: '长度在 3 到 18 个字符', trigger: 'blur' }
                ],
                password: [
                    { required: true, message: '密码不得为空！', trigger: 'blur' },
                    // { min: 5, max: 18, message: '长度在 5 到 18 个字符', trigger: 'blur' }
                ],
                isLock: [
                    {  validator: checkStatus, trigger: 'blur' },
                ],
            },
            acwing_login,
            qq_login,
        };
    }
}
</script>

<style scoped>
.third-login {
    display: flex;
    align-items: center;
    justify-content: space-evenly;
    height: 50px;
}

.third-login div {
    cursor: pointer;
}

.third-login:deep(.el-tooltip__trigger) {
    margin: 0 0 !important;
}
</style>