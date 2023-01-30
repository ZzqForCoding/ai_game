<template>
    <ContentField>
        <el-row>
            <el-col :span="8" :offset="8">
                <el-form :model="log_info" :rules="rules" ref="ruleForm" label-width="50px" label-position="top"
                    style="user-select: none;">
                    <el-form-item label="帐号" prop="username">
                        <el-input v-model="log_info.username" placeholder="请输入用户名或手机号码" clearable />
                    </el-form-item>
                    <el-form-item label="密码" prop="password">
                        <el-input type="password" v-model="log_info.password" placeholder="请输入密码" clearable />
                    </el-form-item>
                    <!-- <el-form-item prop="isLock"> -->
                    <SliderVerify v-model="log_info.isLock" @change="handlerLock" class="verify" @checkVal="checkVal" />
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
                        <el-tooltip class="box-item" effect="dark" content="手机验证码登录" placement="bottom">
                            <div @click="phone_login">
                                <svg t="1669366661899" class="icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="2754" width="32" height="32"><path d="M820.409449 797.228346q0 25.19685-10.07874 46.866142t-27.716535 38.299213-41.322835 26.204724-50.897638 9.574803l-357.795276 0q-27.212598 0-50.897638-9.574803t-41.322835-26.204724-27.716535-38.299213-10.07874-46.866142l0-675.275591q0-25.19685 10.07874-47.370079t27.716535-38.80315 41.322835-26.204724 50.897638-9.574803l357.795276 0q27.212598 0 50.897638 9.574803t41.322835 26.204724 27.716535 38.80315 10.07874 47.370079l0 675.275591zM738.771654 170.330709l-455.559055 0 0 577.511811 455.559055 0 0-577.511811zM510.992126 776.062992q-21.165354 0-36.787402 15.11811t-15.622047 37.291339q0 21.165354 15.622047 36.787402t36.787402 15.622047q22.173228 0 37.291339-15.622047t15.11811-36.787402q0-22.173228-15.11811-37.291339t-37.291339-15.11811zM591.622047 84.661417q0-8.062992-5.03937-12.598425t-11.086614-4.535433l-128 0q-5.03937 0-10.582677 4.535433t-5.543307 12.598425 5.03937 12.598425 11.086614 4.535433l128 0q6.047244 0 11.086614-4.535433t5.03937-12.598425z" p-id="2755"></path></svg>
                            </div>
                        </el-tooltip>
                        <el-tooltip class="box-item" effect="dark" content="忘记密码" placement="bottom">
                            <div @click="forget_password">
                                <svg t="1669386022314" class="icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="1964" width="32" height="32"><path d="M269.04 694.68c-14.936 0-27.088-11.928-27.088-26.608V423.792h433.424v68.408c14.096 1.2 27.696 4.088 40.632 8.448V383.16H201.32v284.912c0 37.144 30.32 67.24 67.72 67.24h231.52a173.208 173.208 0 0 1-12.04-40.632H269.04zM661.832 383.16H621.2v-40.64c0-91.368-76.296-162.528-162.528-162.528-88.36 0-162.528 74.152-162.528 162.528v40.64h-40.632v-40.64c0-110.776 92.384-203.168 203.168-203.168 109.384 0 203.168 88.624 203.168 203.168v40.64z" fill="" p-id="1965"></path><path d="M451.888 491.512h13.552a20.32 20.32 0 0 1 20.312 20.312V606.64a20.328 20.328 0 0 1-20.336 20.32h-13.544a20.32 20.32 0 0 1-20.32-20.32V511.832a20.352 20.352 0 0 1 20.336-20.32zM660.352 519.584c-80.744 0-146.176 65.448-146.176 146.168 0 80.736 65.44 146.176 146.176 146.176 80.728 0 146.176-65.448 146.176-146.176 0-80.72-65.448-146.168-146.176-146.168z m1.496 252.48c-61.2 0-110.808-49.592-110.808-110.808 0-61.192 49.6-110.8 110.808-110.8s110.808 49.6 110.808 110.8c0 61.216-49.6 110.808-110.808 110.808z" fill="" p-id="1966"></path><path d="M657.168 710.952h13.104v11.848h-13.104z" fill="" p-id="1967"></path><path d="M649.168 702.952h29.104v27.848h-29.104z" fill="" p-id="1968"></path><path d="M667.768 590.592c-24.528-0.408-40.128 11.648-46.768 36.168h10.6c5.816-19.952 17.864-29.72 36.168-29.304 17.872 1.24 27.648 10.392 29.312 27.44 1.248 9.56-5.608 19.128-20.576 28.68-12.888 8.328-19.128 18.304-18.712 29.936v6.232h10.6v-5.608c-0.416-10.392 4.16-18.496 13.72-24.32 18.712-9.976 27.44-22.032 26.192-36.168-2.088-20.784-15.592-31.808-40.536-33.056z" fill="" p-id="1969"></path><path d="M676.392 697.752h-26.6V683.52c-0.512-14.304 7.008-26.736 22.368-36.656 8.328-5.312 17.992-13.232 16.992-20.92-1.32-13.472-7.872-19.512-21.936-20.496h-0.552c-8.808 0-21.224 2.448-27.376 23.552l-1.68 5.768h-27.056l2.736-10.096c7.456-27.528 25.88-42.088 53.288-42.088l1.328 0.008c36.864 1.84 46.624 22.904 48.368 40.256 1.552 17.672-8.68 32.448-30.392 44.032-6.64 4.064-9.792 9.512-9.496 16.936l0.008 13.936z" fill="" p-id="1970"></path></svg>
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
                        success(resp) {
                            if(resp.result === "success") {
                                store.dispatch("login_success", resp);
                            } else {
                                ElMessage({
                                    showClose: true,
                                    message: resp.result,
                                    type: 'error',
                                });
                            }
                        },
                    });
                }
            })
        };
 
       const handlerLock = (data) => {
            if (data) {
                log_info.isLock = true;
            }
        };

        const checkVal = async(callback) => {
            const form = unref(ruleForm);
            await form.validate(valid => {
                if(valid) {
                    callback(true);
                } else {
                    callback(false);
                }
            })
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

        const phone_login = () => {
            store.commit("updateBackPage", "user_account_login");
            router.push({name: 'user_account_phone_login'});
        }

        const forget_password = () => {
            store.commit("updateBackPage", "user_account_login");
            router.push({name: 'user_account_forget_password'});
        }

        return {
            ruleForm,
            log_info,
            login,
            handlerLock,
            checkVal,
            rules: {
                username: [
                    { required: true, message: '用户名不得为空！', trigger: 'blur' },
                ],
                password: [
                    { required: true, message: '密码不得为空！', trigger: 'blur' },
                ],
            },
            acwing_login,
            qq_login,
            phone_login,
            forget_password,
        };
    }
}
</script>

<style scoped>
.third-login {
    display: flex;
    align-items: center;
    justify-content: center;
    height: 50px;
}

.third-login div {
    cursor: pointer;
    margin: 10px;
}
</style>