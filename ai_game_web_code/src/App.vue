<template>
    <el-container>
        <el-aside width="200px" style="user-select: none;">
            <div class="aside-header" >
                <!-- <svg t="1660362934898" class="icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="1502" width="25" height="25"><p
                    ath d="M661.333333 490.666667c-36.266667 0-64 27.733333-64 64s27.733333 64 64 64 64-27.733333 64-64-27.733333-64-64-64M362.666667 490.666667c-36.266667 0-64 27.733333-64 64s27.733333 64 64 64 64-27.733333 64-64-27.733333-64-64-64" fill="#2F3CF4" p-id="1503"></p><path d="M128 320c0-23.466667 19.2-42.666667 42.666667-42.666667h170.666666l-61.866666-155.733333c-8.533333-21.333333 2.133333-46.933333 23.466666-55.466667 21.333333-8.533333 46.933333 2.133333 55.466667 23.466667l74.666667 185.6h155.733333l74.666667-185.6c8.533333-21.333333 34.133333-32 55.466666-23.466667 21.333333 8.533333 32 34.133333 23.466667 55.466667L682.666667 277.333333h170.666666c23.466667 0 42.666667 19.2 42.666667 42.666667v597.333333c0 23.466667-19.2 42.666667-42.666667 42.666667H170.666667c-23.466667 0-42.666667-19.2-42.666667-42.666667V320z m85.333333 42.666667v512h597.333334V362.666667H213.333333zM1024 725.333333V512c0-23.466667-19.2-42.666667-42.666667-42.666667s-42.666667 19.2-42.666666 42.666667v213.333333c0 23.466667 19.2 42.666667 42.666666 42.666667s42.666667-19.2 42.666667-42.666667M42.666667 768c23.466667 0 42.666667-19.2 42.666666-42.666667V512c0-23.466667-19.2-42.666667-42.666666-42.666667s-42.666667 19.2-42.666667 42.666667v213.333333c0 23.466667 19.2 42.666667 42.666667 42.666667" fill="#2F3CF4" p-id="1504"></path></svg> -->
                <img src="https://img.zzqahm.top/aigame_platform/avatar/icon1.png" alt="" style="width: 30px; height: 30px;">
                <span style="margin-left: 5px;">AIGame Platform</span>
            </div>
            <el-menu
                class="el-aside-menu" 
                background-color="rgb(13,66,118)"
                text-color="#CCCCCC"
                active-text-color="#fff"
                :collapse="isCollapse"
            >
                <el-scrollbar class="aside-scrollbar">
                    <!-- <el-sub-menu index="1">
                        <template #title>
                            <el-icon :size="30"><Grid /></el-icon>
                            <span>Apps</span>
                        </template>
                        <el-menu-item-group>
                            <router-link class="link-text" :to="{name: 'pk_index', params: { game: '绕蛇' }}">
                                <el-menu-item index="1-1">
                                    <span style="margin-left: 5px;"> 贪吃蛇</span>
                                </el-menu-item>
                            </router-link>
                            <router-link class="link-text" :to="{name: 'pk_index', params: { game: '五子棋' }}">
                                <el-menu-item index="1-2">
                                    <span style="margin-left: 5px;"> 五子棋</span>
                                </el-menu-item>
                            </router-link>
                            <el-menu-item index="1-3" disabled>敬请期待...</el-menu-item>
                        </el-menu-item-group>
                    </el-sub-menu> -->

                    
                    <el-sub-menu index="1">
                        <template #title>
                            <el-icon :size="28"><QuestionFilled /></el-icon>
                            <span>网站介绍</span>
                        </template>
                        <el-menu-item-group>
                            <router-link class="link-text" :to="{name: 'intro_index'}">
                                <el-menu-item index="1-1">
                                    <span style="margin-left: 5px;"> 网站说明 </span>
                                </el-menu-item>
                            </router-link>
                            <router-link class="link-text" :to="{name: 'game_intro_index'}">
                                <el-menu-item index="1-2">
                                    <span style="margin-left: 5px;"> 游戏介绍 </span>
                                </el-menu-item>
                            </router-link>
                            <router-link class="link-text" :to="{name: 'code_helper_index'}">
                                <el-menu-item index="1-3">
                                    <span style="margin-left: 5px;"> 代码编写指南 </span>
                                </el-menu-item>
                            </router-link>
                            <!-- <router-link class="link-text" :to="{name: 'func_intro_index'}">
                                <el-menu-item index="1-4">
                                    <span style="margin-left: 5px;"> 功能介绍 </span>
                                </el-menu-item>
                            </router-link> -->
                        </el-menu-item-group>
                    </el-sub-menu>

                    <router-link class="link-text" :to="{name: 'record_index'}" v-if="$store.state.user.is_login">
                        <el-menu-item index="2">
                            <el-icon :size="30"><HomeFilled /></el-icon>
                            <template #title>首页</template>
                        </el-menu-item>
                    </router-link>
                    
                    <router-link class="link-text" :to="{name: 'fresh_news_index'}" v-if="$store.state.user.is_login">
                        <el-menu-item index="3">
                            <el-icon :size="30"><Promotion /></el-icon>
                            <template #title>动态</template>
                        </el-menu-item>
                    </router-link>

                    <router-link class="link-text" :to="{name: 'ranklist_index'}" v-if="$store.state.user.is_login">
                        <el-menu-item index="4">
                            <el-icon :size="30"><DataLine /></el-icon>
                            <template #title>排行榜</template>
                        </el-menu-item>
                    </router-link>

                    <!-- <router-link class="link-text" :to="{name: 'discussion_index'}">
                        <el-menu-item index="6">
                            <el-icon :size="30"><Comment /></el-icon>
                            <template #title>讨论区</template>
                        </el-menu-item>
                    </router-link>
                    
                    <router-link class="link-text" :to="{name: 'message_board_index'}">
                        <el-menu-item index="7">
                            <el-icon :size="30">
                                <Edit />
                            </el-icon>
                            <template #title>留言板</template>
                        </el-menu-item>
                    </router-link> -->
                    
                    <el-button @click="collapse" circle class="collapse-btn" color="#626aef">
                        <el-icon :size="17" v-if="isCollapse">
                            <Expand />
                        </el-icon>
                        <el-icon :size="17" v-else>
                            <Fold />
                        </el-icon>
                    </el-button>
                </el-scrollbar>
            </el-menu>
        </el-aside>
        <el-container class="right-container">
            <el-header style="user-select: none;">
                <el-menu
                    :default-active="activeIndex"
                    mode="horizontal"
                    :ellipsis="false"
                    @select="handleSelect"
                >
                    <div class="current-page">
                        <span v-if="$store.state.backPage !== ''" class="back-menu" @click="showConfirmBack">
                            <el-icon :size="25"><Back /></el-icon>
                        </span>
                        {{ page }}
                    </div>

                    <el-dialog
                        v-model="showBackDialog"
                        title="Warning"
                        width="30%"
                        align-center
                        draggable
                    >
                        <span v-if="$store.state.pk.status === 'playing'">
                            你确认退出游戏吗？
                        </span>
                        <span v-else-if="$store.state.pk.status === 'matching'">
                            你确认退出匹配吗？
                        </span>
                        <template #footer>
                            <span class="dialog-footer">
                                <el-button @click="showBackDialog = false">取消</el-button>
                                <el-button type="danger" @click="clickBack">确认</el-button
                            >
                            </span>
                        </template>
                    </el-dialog>

                    <div class="flex-grow" />

                    <el-menu-item v-if="$store.state.user.is_login" index="1" style="margin-right: 20px; height: 60px;">
                        <el-dropdown>
                            <span class="el-dropdown-link">
                                <el-avatar shape="square" :size="50" :src="$store.state.user.photo" style="margin-right: 15px;" />
                                <span class="username">
                                    {{ $store.state.user.username }}
                                </span>
                                <el-icon class="el-icon--right">
                                    <arrow-down />
                                </el-icon>
                            </span>
                            <template #dropdown>
                                <el-dropdown-menu style="user-select: none;">
                                    <router-link class="link-text" :to="{name: 'personal_info'}">
                                        <el-dropdown-item>个人信息</el-dropdown-item>
                                    </router-link>
                                    <router-link class="link-text" :to="{name: 'myspace_index', params: {userId: $store.state.user.id}}">
                                        <el-dropdown-item>我的空间</el-dropdown-item>
                                    </router-link>
                                    <el-dropdown-item divided @click="logout">退出</el-dropdown-item>
                                </el-dropdown-menu>
                            </template>
                        </el-dropdown>

                    </el-menu-item>
                    <router-link v-if="!$store.state.user.is_login" class="link-text" :to="{name: 'user_account_login'}">
                        <el-menu-item index="1">
                            <span>
                                登录
                            </span>
                        </el-menu-item>
                    </router-link>
                    <router-link v-if="!$store.state.user.is_login" class="link-text" :to="{name: 'user_account_register'}">
                        <el-menu-item index="2">
                            <span>
                                注册
                            </span>
                        </el-menu-item>
                    </router-link>
                </el-menu>
            </el-header>
            <el-main class="main" style="padding: 0; height: calc(100vh - 60px - 50px); ">     
                <el-scrollbar class="main-scrollbar">
                    <router-view :key="$route.fullPath"></router-view>
                </el-scrollbar>
            </el-main>
            <el-footer>
                <div class="footer">
                </div>
                <div class="footer-icon">
                    <svg t="1660657940962" class="icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="3310" width="25" height="25"><path d="M512 0C229.248 0 0 229.248 0 512s229.248 512 512 512 512-229.248 512-512S794.752 0 512 0z m0 896c-212.032 0-384-171.968-384-384S299.968 128 512 128s384 171.968 384 384-171.968 384-384 384z m94.08-513.408L512 192.064l-94.016 190.528-210.304 30.592 152.192 148.288-35.968 209.344L512 672l188.032 98.88-35.904-209.344 152.128-148.288-210.176-30.656z" fill="#ffffff" p-id="3311"></path></svg>
                </div>
            </el-footer>
        </el-container>
    </el-container>
</template>

<script>
import { useStore } from 'vuex';
import { useRoute } from 'vue-router';
import router from './router/index';
import { watch, ref, onMounted, h } from 'vue';
import {
    Expand,
    Fold,
} from '@element-plus/icons-vue';
import { ElNotification } from 'element-plus';

export default {
    name: 'App',
    components: {
        Expand,
        Fold,
    },
    setup() {
        const store = useStore();
        const route = useRoute();
        const page = ref('');
        let isCollapse = ref(false);
        let showBackDialog = ref(false);

        const logout = () => {
            store.dispatch("logout");
        };

        watch(() => route.name, () => {
            page.value = route.meta.description;
        });

        const collapse = () => {
            isCollapse.value = !isCollapse.value;
        }

        const showConfirmBack = () => {
            if(page.value === "对战界面") 
                showBackDialog.value = true
            else if(page.value === "回放界面") {
                router.push({name: 'record_index'});
            } else if(page.value === "手机验证码登录" || page.value === "找回密码") {
                router.push({name: 'user_account_login'});
            }
        }

        const clickBack = () => {
            showBackDialog.value = false;
            if(store.state.pk.status === 'playing') {
                // 添加断线重连
            } else if(store.state.pk.status === 'matching') {
                // 添加取消匹配
            }
            router.push({name: 'record_index'});
        }

        onMounted(() => {
            ElNotification({
                title: 'Welcome',
                message: h('i', { style: 'color: teal' }, '欢迎来到King Of Bots游戏对战平台！'),
                offset: 70,
            });
        });
        
        return {
            logout,
            page,
            collapse,
            isCollapse,
            showBackDialog,
            showConfirmBack,
            clickBack,
        }
    },
    // 当 Vue 加载完成后调用
    mounted() {
        const store = useStore();
        // 关闭浏览器清除localStorage
        // 方法二：通过在关闭浏览器前清除localStorage
        /**
         * 刷新页面 就算是简单helloworld都不小于5毫秒, 获取时间差来判断刷新与关闭页面
         */
        let start_stamp = 0, // 开始时间
        differ_time = 0; // 时间差
        window.onunload = () => {
            differ_time = new Date().getTime() - start_stamp;
            if (differ_time <= 5) {
                localStorage.removeItem("aigame.access");
                localStorage.removeItem("aigame.refresh");
                localStorage.removeItem("intervalFunc")
                localStorage.removeItem("user");
            }
        };
        window.onbeforeunload = () => {
            start_stamp = new Date().getTime();
        };
        // 刷新
        window.onload = () => {
            // 用户持久化登录
            let refresh = localStorage.getItem('aigame.refresh');
            if(refresh) store.dispatch("refresh_access", refresh);
            // 检测用户是否在线
            store.dispatch("connectHallSocket");
        }
    },
}
</script>

<style>
/*隐藏文字*/
.el-menu--collapse .el-sub-menu__title span{
    display: none;
}
/*隐藏 > */
.el-menu--collapse .el-submenu__title .el-submenu__icon-arrow{
    display: none;
}
 /* Chrome Safari */
html:-webkit-scrollbar {
    display: none;
}


 /* firefox */
 /* IE 10+ */
html {
    scrollbar-width: none;
    -ms-overflow-style: none; 
    overflow-x: hidden;
    overflow-y: auto;

}

    
body {
    background-image: url('@/assets/images/background1.png');
    background-size: cover;
    margin: 0 0;
}

.aside-header {
    height: 60px;
    background-color: rgb(5,25,41);
    color: white;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 600;
}

.el-aside-menu {
    height: calc(100vh - 60px);
    border-right: none !important;
}

.aside-scrollbar {
    height: calc(100vh - 60px);
}

.el-aside-menu .el-menu-item.is-active {
    background-color: #1890ff !important;
}

.flex-grow {
  flex-grow: 1;
}

.right-container {
    height: 100vh !important;
}

.back-menu {
    margin-right: 10px; 
    display: flex;
    align-items: center;
    cursor: pointer;
}

.el-header {
    padding: 0 0 !important;
}

.el-footer {
    margin-top: 20px;
    height: 30px !important;
}

.main-scrollbar {
    height: calc(100vh - 60px - 50px) !important;
}

.footer {
    height: 1px;
    width: 100%;
    background-color: #fff;
}

.link-text {
    text-decoration: none;
}

.username {
    line-height: 60px;
    font-weight: 700;
    font-size: 17px;
}

.current-page {
    line-height: 60px;
    width: 200px;
    font-size: 17px;
    margin-left: 25px;
    display: flex;
}

.collapse-btn {
    margin: 15px 10px;
}

.footer-icon {
    position: relative;
    margin: -12.5px;
    display: flex;
    justify-content: center;
}
</style>