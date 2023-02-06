<template>
    <el-row style="margin-top: 40px;">
        <el-col :span="5" :offset="2">
            <ProfileCard :info="playerInfo" />
        </el-col>
        <el-col :span="14" :offset="1">
            <el-card style="margin-top: 25px; user-select: none;">
                <template #header>
                    <div class="card-header">
                        <span>个人信息</span>
                    </div>
                </template>
                <el-row style="margin-top: 40px;">
                    <el-col :span="20" :offset="2">
                        <el-form ref="editForm" :label-position="labelPosition" label-width="180px" :model="personalEditInfo" :rules="rules" style="max-width: 600px">
                            <el-form-item label="头像">
                                <el-upload class="avatar-uploader"
                                    v-model:file-list="avatarList"
                                    list-type="picture-card"
                                    :before-upload="beforeAvatarUpload"
                                    :http-request="uploadAvatar"
                                    :on-change="handleChangePic"
                                    :on-preview="handlePreviewPic">
                                    <el-icon><Plus /></el-icon>
                                    <template #tip>
                                        <div class="el-upload__tip">
                                            jpg/png files with a size less than 2MB
                                        </div>
                                    </template>
                                </el-upload>
                                <el-dialog v-model="showImgDialog">
                                    <img w-full :src="dialogimageUrl" alt="Preview Image" />
                                </el-dialog>
                            </el-form-item>
                            <el-form-item label="用户名" prop="username">
                                <el-input placeholder="Please input username" clearable v-model="personalEditInfo.username" />
                            </el-form-item>
                            <el-form-item label="手机号">
                                <el-input placeholder="Please input phone" clearable v-model="personalEditInfo.phone" :disabled="$store.state.user.phone !== null && $store.state.user.phone !== ''">
                                    <template #append v-if="$store.state.user.phone === null || $store.state.user.phone === ''">
                                        <el-button @click="send_msg(personalEditInfo.phone)">
                                            <span v-if="$store.state.utils.showVerifyCode">已发送({{ $store.state.utils.verifyCodeTime }})</span>
                                            <span v-else>发送验证码</span>
                                        </el-button>
                                    </template>
                                </el-input>
                            </el-form-item>
                            <div class="verify-code-prompt" v-if="$store.state.utils.showVerifyCode">验证码在5分钟内有效，请及时填写！</div>
                            <el-form-item label="验证码" v-if="$store.state.utils.showVerifyCode" prop="verify_code">
                                <el-input placeholder="Please input verification code" clearable v-model="personalEditInfo.verify_code" />
                            </el-form-item>
                            <el-form-item label="职业" prop="job">
                                <el-input placeholder="Please input your job" clearable v-model="personalEditInfo.job" />
                            </el-form-item>

                            <el-form-item label="个性签名" prop="desp">
                                <el-input type="textarea" v-model="personalEditInfo.desp"/>
                            </el-form-item>
                            <el-form-item>
                                <el-button type="primary" style="width: 100%;" @click="updatePlayerInfo">更新</el-button>
                            </el-form-item>
                        </el-form>
                    </el-col>
                </el-row>
            </el-card>
        </el-col>
    </el-row>
</template>

<script>
import ProfileCard from '@/components/ProfileCard.vue';
import { GameUtils } from '@/assets/scripts/GameUtils';
import { useStore } from 'vuex'; 
import { reactive, ref, watchEffect, unref, onMounted } from 'vue';
import { ElMessage, ElMessageBox } from 'element-plus';
import { Plus } from '@element-plus/icons-vue';
import $ from 'jquery';

export default {
    name: 'PersonalInfoView',
    components: {
        ProfileCard,
        Plus,
    },
    setup() {
        const store = useStore();
        const playerInfo = reactive({
            'id': store.state.user.id,
            'username': store.state.user.username,
            'photo': store.state.user.photo,
            'job': store.state.user.job,
            'desp': store.state.user.desp,
            'recordCnt': store.state.user.recordCnt,
            'botCnt': store.state.user.botCnt,
            'freshNewsCnt': store.state.user.freshNewsCnt,
        });
        let showImgDialog = ref(false);
        let dialogimageUrl = ref('');
        let avatarList = ref([{
            'name': '1.jpg',
            'url': store.state.user.photo,
        }]);
        let personalEditInfo = reactive({
            photo: store.state.user.photo,
            username: store.state.user.username,
            job: store.state.user.job,
            desp: store.state.user.desp,
            phone: store.state.user.phone,
            verify_code: '',
        });
        let editForm = ref(null);

        watchEffect(()=>{
            playerInfo.username = store.state.user.username;
            playerInfo.photo = store.state.user.photo;
            playerInfo.job = store.state.user.job;
            playerInfo.desp = store.state.user.desp;
        })

        const beforeAvatarUpload = (rawFile) => {
            if (rawFile.type !== 'image/jpeg' && rawFile.type !== "image/png") {
                ElMessage.error('Avatar picture must be JPG/PNG format!')
                return false
            } else if (rawFile.size / 1024 / 1024 > 2) {
                ElMessage.error('Avatar picture size can not exceed 2MB!')
                return false
            }
            return true;
        };
 
        const handleChangePic = (file, fileList) => {
            if(fileList.length > 1) {
                fileList.splice(0, 1);
            }
        }

        // const updateAvatar = () => {
        //     $.ajax({
        //         url: "https://aigame.zzqahm.top/backend/player/img/update_avatar/", 
        //         type: "POST",
        //         headers: {
        //             "Authorization": "Bearer " + store.state.user.access,
        //         },
        //         data: {
        //             imgUrl: personalEditInfo.photo,  
        //         },
        //         success() {
        //             avatarList.value[0] = {
        //                 'name': ([1e7]+-1e3+-4e3+-8e3+-1e11).replace(/[018]/g, c =>(c ^ crypto.getRandomValues(new Uint8Array(1))[0] & 15 >> c / 4).toString(16)) + '.jpg',
        //                 'url': personalEditInfo.photo
        //             };
        //             return false;
        //         },
        //         error() {
        //             store.dispatch("logout");
        //             return true;
        //         }
        //     });
        // }

        const uploadAvatar = (data) => {
            let file = data.file;
            ElMessageBox.alert('由于平台无法盈利，因此租不起OSS对象存储服务器，因此暂时停止提供更改头像功能', '提示', {
                confirmButtonText: '取消',
                callback: () => {
                    store.dispatch("uploadImage", {
                        file, 
                        userId: store.state.user.id,
                        success(imgUrl) {
                            personalEditInfo.photo = imgUrl + '?x-oss-process=image/resize,h_500,m_lfit';
                        }
                    });
                },
            })
        }

        const handlePreviewPic = (file) => {
            showImgDialog.value = true;
            dialogimageUrl.value = file.url;
        }

        const updatePlayerInfo = async() => {
            const form = unref(editForm);
            await form.validate(valid => {
                if(valid) {
                    if(personalEditInfo.username === store.state.user.username &&
                       /* personalEditInfo.photo === store.state.user.photo && */
                       personalEditInfo.job === store.state.user.job &&
                       personalEditInfo.desp === store.state.user.desp &&
                       personalEditInfo.phone === store.state.user.phone) {
                        ElMessage({
                            message: '没有修改任何信息',
                            type: 'warning',
                        })
                        return;
                    }
                    $.ajax({
                        url: "https://aigame.zzqahm.top/backend/player/update_info/",
                        type: "POST",
                        headers: {
                            'Authorization': "Bearer " + store.state.user.access,
                        },
                        data: {
                            'username': personalEditInfo.username,
                            'job': personalEditInfo.job,
                            'desp': personalEditInfo.desp,
                        },
                        success(resp) {
                            if(resp.result === "success") {
                                if(personalEditInfo.phone !== store.state.user.phone) {
                                    let ret = bind_phone();
                                    if(ret) {
                                        return;
                                    }
                                }
                                // if(personalEditInfo.photo !== store.state.user.photo) {
                                //     let ret = updateAvatar();
                                //     if(ret) {
                                //         return;
                                //     }
                                // }
                                store.commit("updateUser", {
                                    'id': store.state.user.id,
                                    'username': personalEditInfo.username,
                                    'photo': personalEditInfo.photo,
                                    'is_login': store.state.user.is_login,
                                    'job': personalEditInfo.job,
                                    'desp': personalEditInfo.desp,
                                    'botCnt': store.state.user.botCnt,
                                    'recordCnt': store.state.user.recordCnt,
                                    'freshNewsCnt': store.state.user.freshNewsCnt,
                                    'isSuperUser': store.state.user.isSuperUser,
                                    'phone': personalEditInfo.phone,
                                });
                                ElMessage({
                                    showClose: true,
                                    message: '更新成功',
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
                        error() {
                            store.dispatch("logout");
                        }
                    });
                } 
            });
        }

        const bind_phone = () => {
            $.ajax({
                url: "https://aigame.zzqahm.top/backend/player/binding_phone/",
                type: "POST",
                headers: {
                    'Authorization': "Bearer " + store.state.user.access,
                },
                data: {
                    phone: personalEditInfo.phone,
                    code: personalEditInfo.verify_code.trim(),
                },
                success(resp) {
                    if(resp.result === "success") {
                        store.commit("updateShowVerifyCode", false);
                        return false;
                    } else {
                        ElMessage({
                            showClose: true,
                            message: resp.result,
                            type: 'error',
                        })
                        return true;
                    }
                },
                error() {
                    store.dispatch("logout");
                    return true;
                }
            });
        }

        const send_msg = phone => {
            store.dispatch("send_msg", {
                phone,
                flag: "binding",
            });
        }

        onMounted(() => {
            if(store.state.utils.gameUtils === null) {
                store.commit("updateGameUtils", new GameUtils(store));
            }
        });

         return {
            playerInfo,
            beforeAvatarUpload,
            handleChangePic,
            uploadAvatar,
            showImgDialog,
            dialogimageUrl,
            handlePreviewPic,
            avatarList,
            personalEditInfo,
            updatePlayerInfo,
            editForm,
            send_msg,
            rules: {
                username: [
                    { required: true, message: '用户名不得为空！', trigger: 'blur' },
                    { max: 15, message: '长度在 15 个字符之内', trigger: 'blur' }
                ],
                job: [
                    { max: 20, message: '长度在 20 个字符之内', trigger: 'blur' }
                ],
                desp: [
                    { max: 200, message: '长度在 200 个字符之内', trigger: 'blur' }
                ],
                verify_code: [
                    { required: true, message: '验证码不得为空！', trigger: 'blur' },
                ],
            },
        }
    }
}
</script>

<style scoped>

.avatar-uploader:deep(.el-upload-list__item-preview) {
    position: relative;
    left: 20px;
}

.avatar-uploader:deep(.el-upload-list__item-delete) {
    visibility: hidden;
}

.avatar-uploader:deep(.el-icon--close-tip) {
    visibility: hidden;
}

.verify-code-prompt {
    margin-bottom: 18px;
    text-align: center;
    color: #666;
    font-size: 13px;
    font-weight: 600;
}
</style>