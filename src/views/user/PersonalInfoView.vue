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
                        <el-form :label-position="labelPosition" label-width="180px" :model="personalEditInfo" :rules="rules" style="max-width: 600px">

                            <el-form-item label="头像">
                                <el-upload class="avatar-uploader"
                                    v-model:file-list="avatarList"
                                    action="https://aigame.zzqahm.top/backend/player/upload_avatar/"
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
import { useStore } from 'vuex'; 
import { reactive, ref, watchEffect } from 'vue';
import { ElMessage } from 'element-plus';
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
            'username': store.state.user.username,
            'photo': store.state.user.photo,
            'job': store.state.user.job,
            'desp': store.state.user.desp
        });
        let showImgDialog = ref(false);
        let dialogimageUrl = ref('');
        let avatarList = ref([{
            'name': '1.jpg',
            'url': store.state.user.photo
        }]);
        let personalEditInfo = reactive({
            username: store.state.user.username,
            job: store.state.user.job,
            desp: store.state.user.desp,
        });

        watchEffect(()=>{
            playerInfo.username = store.state.user.username;
            playerInfo.photo = store.state.user.photo;
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

        const uuid = () => {
            return ([1e7]+-1e3+-4e3+-8e3+-1e11).replace(/[018]/g, c =>
                (c ^ crypto.getRandomValues(new Uint8Array(1))[0] & 15 >> c / 4).toString(16)
            );
        }

        const uploadAvatar = (data) => {
            let file = data.file;
            //填写获取签名的地址
            const getPolicyApiUrl = 'https://aigame.zzqahm.top/backend/player/upload_avatar/apply/'; //获取oss签名的地址
            $.ajax({
                url: getPolicyApiUrl, 
                type: "GET",
                data: {
                    'filename': file.name,
                    'userId': store.state.user.id
                },
                success: resp => {
                    resp = $.parseJSON(resp)
                    let ossUrl = "https://player-avatar.oss-cn-shenzhen.aliyuncs.com";
                    let pos = file.name.lastIndexOf('.');
                    let accessUrl = resp.dir + '/' + uuid() + file.name.substr(pos);
                    let sendData = new FormData();
                    sendData.append("OSSAccessKeyId", resp.accessid);
                    sendData.append("policy", resp.policy);
                    sendData.append("signature", resp.signature);
                    sendData.append("keys", resp.dir);
                    sendData.append("callback", resp.callback);
                    sendData.append("key", accessUrl);
                    sendData.append('success_action_status', 200); // 指定返回的状态码
                    sendData.append('type', file.type);
                    sendData.append('file', file);
                    $.ajax({
                        url: ossUrl, 
                        type: "POST",
                        cache: false,
                        contentType: false,
                        processData: false,
                        data: sendData,
                        success(resp) {
                            resp.imgUrl += '?x-oss-process=image/resize,h_500,m_lfit';
                            $.ajax({
                                url: "https://aigame.zzqahm.top/backend/player/upload_avatar/update_avatar/", 
                                type: "POST",
                                headers: {
                                    "Authorization": "Bearer " + store.state.user.access,
                                },
                                data: {
                                    imgUrl: resp.imgUrl,  
                                },
                                success() {
                                    avatarList.value[0] = {
                                        'name': file.name,
                                        'url': resp.imgUrl
                                    };
                                    store.commit("updateUser", {
                                        'id': store.state.user.id,
                                        'username': store.state.user.username,
                                        'photo': resp.imgUrl,
                                        'is_login': store.state.user.is_login,
                                        'job': store.state.user.job,
                                        'desp': store.state.user.desp,
                                    });
                                },
                                error() {
                                    store.dispatch("logout");
                                }
                            });
                        },
                        error() {
                            store.dispatch("logout");
                        }
                    });
                },
                error() {
                    store.dispatch("logout");
                }
            });
        }

        const handlePreviewPic = (file) => {
            showImgDialog.value = true;
            dialogimageUrl.value = file.url;
        }

        const updatePlayerInfo = () => {
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
                        ElMessage({
                            showClose: true,
                            message: '更新成功',
                            type: 'success',
                        });
                        playerInfo.job = personalEditInfo.job;
                        playerInfo.desp = personalEditInfo.desp;
                        store.commit("updateUser", {
                            'id': store.state.user.id,
                            'username': personalEditInfo.username,
                            'photo': store.state.user.photo,
                            'is_login': store.state.user.is_login,
                            'job': personalEditInfo.job,
                            'desp': personalEditInfo.desp,
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
</style>