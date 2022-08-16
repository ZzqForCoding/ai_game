<template>
    <el-container>
        <el-aside width="200px" >
            <div class="aside-header">
                    <svg t="1660362934898" class="icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="1502" width="25" height="25"><path d="M661.333333 490.666667c-36.266667 0-64 27.733333-64 64s27.733333 64 64 64 64-27.733333 64-64-27.733333-64-64-64M362.666667 490.666667c-36.266667 0-64 27.733333-64 64s27.733333 64 64 64 64-27.733333 64-64-27.733333-64-64-64" fill="#2F3CF4" p-id="1503"></path><path d="M128 320c0-23.466667 19.2-42.666667 42.666667-42.666667h170.666666l-61.866666-155.733333c-8.533333-21.333333 2.133333-46.933333 23.466666-55.466667 21.333333-8.533333 46.933333 2.133333 55.466667 23.466667l74.666667 185.6h155.733333l74.666667-185.6c8.533333-21.333333 34.133333-32 55.466666-23.466667 21.333333 8.533333 32 34.133333 23.466667 55.466667L682.666667 277.333333h170.666666c23.466667 0 42.666667 19.2 42.666667 42.666667v597.333333c0 23.466667-19.2 42.666667-42.666667 42.666667H170.666667c-23.466667 0-42.666667-19.2-42.666667-42.666667V320z m85.333333 42.666667v512h597.333334V362.666667H213.333333zM1024 725.333333V512c0-23.466667-19.2-42.666667-42.666667-42.666667s-42.666667 19.2-42.666666 42.666667v213.333333c0 23.466667 19.2 42.666667 42.666666 42.666667s42.666667-19.2 42.666667-42.666667M42.666667 768c23.466667 0 42.666667-19.2 42.666666-42.666667V512c0-23.466667-19.2-42.666667-42.666666-42.666667s-42.666667 19.2-42.666667 42.666667v213.333333c0 23.466667 19.2 42.666667 42.666667 42.666667" fill="#2F3CF4" p-id="1504"></path></svg>
                    <span style="margin-left: 5px;">King Of Bots</span>
            </div>
            <el-menu
                class="el-aside-menu" 
                background-color="rgb(13,66,118)"
                text-color="#CCCCCC"
                active-text-color="#fff"
                :collapse="isCollapse"
            >
                <el-scrollbar class="aside-scrollbar">
                    <el-sub-menu index="1">
                        <template #title>
                            <el-icon :size="30"><Grid /></el-icon>
                            <span>Apps</span>
                        </template>
                        <el-menu-item-group>
                            <!-- <router-link class="link-text" :to="{name: 'pk_index', params: { game: '绕蛇' }}">
                                <el-menu-item index="1-1">
                                    <span style="margin-left: 5px;"> 贪吃蛇</span>
                                </el-menu-item>
                            </router-link>
                            <router-link class="link-text" :to="{name: 'pk_index', params: { game: '五子棋' }}">
                                <el-menu-item index="1-2">
                                    <span style="margin-left: 5px;"> 五子棋</span>
                                </el-menu-item>
                            </router-link> -->
                            <el-menu-item index="1-3" disabled>敬请期待...</el-menu-item>
                        </el-menu-item-group>
                      </el-sub-menu>

                    <router-link class="link-text" :to="{name: 'record_index'}">
                        <el-menu-item index="2">
                            <el-icon :size="30"><HomeFilled /></el-icon>
                            <template #title>首页</template>
                        </el-menu-item>
                    </router-link>

                    <router-link class="link-text" :to="{name: 'ranklist_index'}">
                        <el-menu-item index="3">
                            <el-icon :size="30"><DataLine /></el-icon>
                            <template #title>排行榜</template>
                        </el-menu-item>
                    </router-link>

                    
                    <router-link class="link-text" :to="{name: 'discussion_index'}">
                        <el-menu-item index="4">
                            <el-icon :size="30"><Comment /></el-icon>
                            <template #title>讨论区</template>
                        </el-menu-item>
                    </router-link>

                    
                    <router-link class="link-text" :to="{name: 'message_board_index'}">
                        <el-menu-item index="5">
                            <el-icon :size="30">
                                <Edit />
                            </el-icon>
                            <template #title>留言板</template>
                        </el-menu-item>
                    </router-link>
                    
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
        <el-container>
            <el-header>
                
                <el-menu
                    :default-active="activeIndex"
                    class="el-menu-demo"
                    mode="horizontal"
                    :ellipsis="false"
                    @select="handleSelect"
                >
                    <div class="current-page">
                        {{ page }}
                    </div>

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
                                <el-dropdown-menu>
                                    <router-link class="link-text" :to="{name: 'user_bot_index'}">
                                        <el-dropdown-item>我的Bot</el-dropdown-item>
                                    </router-link>
                                    <el-dropdown-item divided @click="logout">退出</el-dropdown-item>
                                </el-dropdown-menu>
                            </template>
                        </el-dropdown>

                    </el-menu-item>
                    <router-link v-if="!$store.state.user.is_login && !$store.state.user.pulling_info" class="link-text" :to="{name: 'user_account_login'}">
                        <el-menu-item index="1">
                            <span>
                                登录
                            </span>
                        </el-menu-item>
                    </router-link>
                    <router-link v-if="!$store.state.user.is_login && !$store.state.user.pulling_info" class="link-text" :to="{name: 'user_account_register'}">
                        <el-menu-item index="2">
                            <span>
                                注册
                            </span>
                        </el-menu-item>
                    </router-link>
                </el-menu>
            </el-header>
            <el-main>     
                <el-scrollbar class="main-scrollbar">
                    <router-view></router-view>
                </el-scrollbar>
            </el-main>
            <el-footer>
                <div class="footer">

                </div>
            </el-footer>
        </el-container>
    </el-container>
</template>

<script>
import { useStore } from 'vuex';
import { useRoute } from 'vue-router';
import router from './router/index'
import { watch, ref } from 'vue';
import {
    Expand,
    Fold,
} from '@element-plus/icons-vue'

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

        const logout = () => {
            store.dispatch("logout");
            router.push({name: 'user_account_login'});
        };

        watch(() => route.name, () => {
            page.value = route.meta.description;
        });

        const collapse = () => {
            isCollapse.value = !isCollapse.value;
        }

        return {
            logout,
            page,
            collapse,
            isCollapse
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

.aside-scrollbar {
    height: 100vh;
}
 /* Chrome Safari */
/* html:-webkit-scrollbar {
    display: none;
}
*/

 /* firefox */
 /* IE 10+ */
/* html {
    scrollbar-width: none;
    -ms-overflow-style: none; 
    overflow-x: hidden;
    overflow-y: auto;

} */

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

.el-aside-menu .el-menu-item.is-active {
    background-color: #1890ff !important;
}

.flex-grow {
  flex-grow: 1;
}

.el-main {
    padding: 0px 0 !important;
    padding-bottom: 0px !important;
}

.el-header {
    padding: 0 0 !important;
}

.el-main {
    height: calc(100vh - 60px - 40px) !important;
    /* IE 10+ */
    /* firefox */
    /* scrollbar-width: none; 
    -ms-overflow-style: none; 
    overflow-x: hidden;
    overflow-y: auto; */
}
/* Chrome Safari */
/* .el-main::-webkit-scrollbar {
    display: none; 
} */


.el-footer {
    margin-top: 10px;
    height: 30px !important;
}

.main-scrollbar {
    height: calc(100vh - 60px - 40px) !important;
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
    width: 100px;
    font-size: 17px;
    display: flex;
    justify-content: center;
}

.collapse-btn {
    position: relative;
    top: 42vh;
    left: 15px;
}
</style>
