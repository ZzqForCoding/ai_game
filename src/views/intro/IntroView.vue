<template>
    
    <el-row style="margin-top: 40px;" v-if="show === 'create'">
        <el-col :span="4" :offset="4">
            <div style="display: flex; align-items: center; margin-left: 10px;">
                <h1 style="color: white;">标题：{{ title }}</h1>
            </div>
        </el-col>

        <el-col :span="3" :offset="9" style="display: flex; justify-content: space-around; align-items: center;">
            <el-tooltip
                class="box-item"
                effect="dark"
                :content="lastSaveTime"
                placement="bottom-start"
                v-if="flag === 'create'"
            >
                <el-icon style="color: white;"><Clock /></el-icon>
            </el-tooltip>
            <el-button @click="backToPreview" style="margin-left: 10px;">
                <el-icon style="vertical-align: middle;">
                    <ArrowLeft />
                </el-icon>
                <span>返回</span>
            </el-button>
            <el-button @click="onPreview" type="success">预览</el-button>
            <el-button @click="onSubmit" type="primary" style="margin-right:40px;">保存</el-button>
        </el-col>
        <el-col :span="16" :offset="4">
            <el-input v-model="title" size="large" placeholder="Please input title" clearable />
        </el-col>
        <el-col :span="16" :offset="4" style="margin-top: 40px;">
            <v-md-editor
                v-model="mdValue"
                left-toolbar="undo redo clear | h bold italic strikethrough quote todo-list | ul ol table hr | link image code emoji | save"
                height="500px"
                @copy-code-success="handleCopyCodeSuccess"
                @upload-image="handleUploadImage"
                @save="save"
                @change="change"
                :disabled-menus="[]"
                :include-level="[1, 2, 3, 4, 5, 6]"
            >
            </v-md-editor>
        </el-col>
    </el-row>

            
    <el-row style="margin-top: 40px;" v-if="show === 'preview'">
        <el-col :span="2" :offset="4" style="display: flex; align-items: center;" v-if="$store.state.user.isSuperUser">
            <el-button style="margin-left: 10px;" v-if="startPreview" @click="backToCreate">
                <el-icon style="vertical-align: middle;">
                    <ArrowLeft />
                </el-icon>
                <span>Back</span>
            </el-button>
            <el-tooltip
                class="box-item"
                effect="dark"
                content="提示：此说明是临时显示，网站固定显示id为1的说明！"
                placement="right"
                v-else-if="createPreview"
            >
                <el-icon style="color: white;"><InfoFilled /></el-icon>
            </el-tooltip>
        </el-col>
        <el-col :span="3" :offset="11" style="display: flex; justify-content: space-around; align-items: center;" v-if="$store.state.user.isSuperUser && !startPreview">
            <el-button style="margin-right: 10px;" @click="onEdit">Edit</el-button>
            <el-button type="primary" @click="onCreate">Create</el-button>
        </el-col>
        <el-col :span="16" :offset="4" style="margin-top: 20px;">
            <MDPreview :previewValue="previewValue" />
        </el-col>
    </el-row>
</template>

<script>
import MDPreview from '@/components/MDPreview.vue';
import { ref, onMounted } from 'vue';
import { ElMessage } from 'element-plus';
import { useStore } from 'vuex'; 
import $ from 'jquery';

export default {
    name: 'IntroVie',
    components: {
        MDPreview,
    },
    setup() {
        Date.prototype.format = function(fmt) {
            var o = {
                'M+': this.getMonth() + 1, // 月份
                'd+': this.getDate(), // 日
                'h+': this.getHours(), // 小时
                'm+': this.getMinutes(), // 分
                's+': this.getSeconds(), // 秒
                'q+': Math.floor((this.getMonth() + 3) / 3), // 季度
                'S': this.getMilliseconds() // 毫秒
            }
            if (/(y+)/.test(fmt)) { fmt = fmt.replace(RegExp.$1, (this.getFullYear() + '').substr(4 - RegExp.$1.length)) }
            for (var k in o) {
                if (new RegExp('(' + k + ')').test(fmt)) { fmt = fmt.replace(RegExp.$1, (RegExp.$1.length === 1) ? (o[k]) : (('00' + o[k]).substr(('' + o[k]).length))) }
            }
            return fmt
        }

        const store = useStore();
        // preview，create
        let show = ref('preview');
        let title = ref('');
        let mdValue = ref('');
        let previewId = ref(0);
        let previewTitle = ref('');
        let previewValue = ref('');
        let autoSaveInterval = ref(null);
        let isModify = ref(false);
        let lastSaveTime = ref(new Date().format("自动保存：yyyy-MM-dd hh:mm:ss"));
        let startPreview = ref(false);      // 创建界面点击预览需要标记
        let createPreview = ref(false);     // 创建文章标记不会显示到首页
        let flag = ref('');                 // 标记是创建还是编辑

        const handleCopyCodeSuccess = () => {
            ElMessage({
                showClose: true,
                message: '复制成功',
                type: 'success',
            });
        };

        const handleUploadImage = (event, insertImage, files) => {
            let file = files[0];
            store.dispatch("uploadImage", {
                file, 
                userId: store.state.user.id,
                success(imgUrl, fileName) {
                    console.log(imgUrl, fileName)
                    insertImage({
                        url: imgUrl,
                        desc: fileName,
                        width: '700',
                        height: 'auto',
                    });
                }
            });
        };

        const save = () => {
            localStorage.setItem("intro-content-" + store.state.user.username, mdValue.value);
            localStorage.setItem("intro-title-" + store.state.user.username, title.value);
            ElMessage({
                showClose: true,
                message: '保存成功',
                type: 'success',
            });
            lastSaveTime.value = new Date().format("自动保存：yyyy-MM-dd hh:mm:ss");
            isModify.value = false;
        };

        const handleSave = () => {
            if(!isModify.value) return;
            save();
        };

        onMounted(() => {
            store.dispatch("getGameIntro", {
                id: 1,
                success(resp) {
                    previewId.value = resp.data.id;
                    previewTitle.value = resp.data.title;
                    previewValue.value = resp.data.content; 
                }
            });
        });

        const change = () => {
            isModify.value = true;
        };

        // 创建界面进行预览
        const onPreview = () => {
            stopAutoSave();
            previewValue.value = mdValue.value;
            show.value = "preview";
            startPreview.value = true;
        }

        // 创建界面返回预览界面
        const backToPreview = () => {
            flag.value = "";
            stopAutoSave();
            title.value = "";
            mdValue.value = "";
            store.dispatch("getGameIntro", {
                id: 1,
                success(resp) {
                    previewId.value = resp.data.id;
                    previewTitle.value = resp.data.title;
                    previewValue.value = resp.data.content; 
                }
            });
            show.value = "preview";
        }

        // 预览界面点击创建
        const onCreate = () => {
            flag.value = "create";
            show.value = "create";
            createPreview.value = false;
            if (localStorage.getItem("intro-content-" + store.state.user.username) !== null) {
                mdValue.value = localStorage.getItem("intro-content-" + store.state.user.username)
                title.value = localStorage.getItem("intro-title-" + store.state.user.username);
            }
            startAutoSave();
        }

        // 预览完毕回到创建界面
        const backToCreate = () => {
            if(flag.value !== "edit") startAutoSave();
            show.value = "create";
            startPreview.value = false;
        }

        // 预览界面点击编辑
        const onEdit = () => {
            flag.value = "edit";
            title.value = previewTitle.value;
            mdValue.value = previewValue.value;
            show.value = "create";
        }

        // 进入创建界面
        const startAutoSave = () => {
            console.log("自动保存开始")
            autoSaveInterval.value = setInterval(handleSave, 60 * 1000);
        }

        // 离开创建界面
        const stopAutoSave = () => {
            if(autoSaveInterval.value !== null) {
                localStorage.setItem("intro-content-" + store.state.user.username, mdValue.value);
                localStorage.setItem("intro-title-" + store.state.user.username, title.value);
                clearInterval(autoSaveInterval.value);
                autoSaveInterval.value = null;
                console.log("自动保存结束")
            }
        }

        const createGameIntro = () => {
            $.ajax({
                url: "https://aigame.zzqahm.top/backend/playervoice/game_intro/post/",
                type: "post",
                headers: {
                    "Authorization": "Bearer " + store.state.user.access,
                },
                data: {
                    title: title.value,
                    content: mdValue.value,
                    isPost: "True",
                },
                success(resp) {
                    if(resp.result === "success") {
                        localStorage.removeItem("intro-title-" + store.state.user.username, mdValue.value);
                        localStorage.removeItem("intro-content-" + store.state.user.username, mdValue.value);
                        show.value = "preview";
                        previewId.value = resp.id;
                        previewTitle.value = title.value;
                        previewValue.value = mdValue.value;
                        title.value = "";
                        mdValue.value = "";
                        stopAutoSave();
                        createPreview.value = true;
                    }
                },
                error() {
                    store.dispatch("logout");
                }
            });
        }

        const editGameIntro = () => {
            $.ajax({
                url: "https://aigame.zzqahm.top/backend/playervoice/game_intro/edit/",
                type: "post",
                headers: {
                    "Authorization": "Bearer " + store.state.user.access,
                },
                data: {
                    id: previewId.value,
                    title: title.value,
                    content: mdValue.value,
                    isPost: "True",
                },
                success(resp) {
                    if(resp.result === "success") {
                        show.value = "preview";
                        previewTitle.value = title.value;
                        previewValue.value = mdValue.value;
                        title.value = "";
                        mdValue.value = "";
                        stopAutoSave();
                        if(previewId.value !== 1) {
                            createPreview.value = true;
                        }
                    }
                },
                error() {
                    store.dispatch("logout");
                }
            });
        }

        const onSubmit = () => {
            if(flag.value === "create") {
                createGameIntro();
            } else {
                editGameIntro();
            }
        }

        return {
            show,
            title,
            mdValue,
            previewValue,
            handleCopyCodeSuccess,
            handleUploadImage,
            save,
            isModify,
            lastSaveTime,
            change,
            onPreview,
            backToPreview,
            onCreate,
            backToCreate,
            startPreview,
            onEdit,
            onSubmit,
            createPreview,
            flag,
        }
    },
}
</script>

<style scoped>
</style>