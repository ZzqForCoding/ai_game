import { createRouter, createWebHistory } from 'vue-router'
import PkIndexView from '@/views/pk/PkIndexView'
import RankListIndexView from '@/views/ranklist/RankListIndexView'
import RecordIndexView from '@/views/record/RecordIndexView'
import RecordContentView from '@/views/record/RecordContentView'
import DiscussionView from '@/views/discussion/DiscussionView'
import MessageBoardView from '@/views/message_board/MessageBoardView'
import UserBotIndexView from '@/views/user/bots/UserBotIndexView'
import NotFound from '@/views/error/NotFound'
import UserAccountLoginView from '@/views/user/account/UserAccountLoginView'
import UserAccountRegisterView from '@/views/user/account/UserAccountRegisterView'
import store from '@/store'

const routes = [
    {
        path: '/',
        name: 'home',
        redirect: '/record/',
        meta: {
            requestAuth: true,
            description: '首页',
            isRoot: false,
        }
    },
    {
        path: '/pk/:game/',
        name: 'pk_index',
        component: PkIndexView,
        meta: {
            requestAuth: true,
            description: 'game',
            isRoot: false,
        }
    },
    {
        path: '/record/',
        name: 'record_index',
        component: RecordIndexView,
        meta: {
            requestAuth: true,
            description: '对战列表',
            isRoot: true,
        }
    },
    {
        path: "/record/:recordId/",
        name: "record_content",
        component: RecordContentView,
        meta: {
            requestAuth: true,
            description: '对战界面',
            isRoot: false,
        }
    },
    {
        path: '/ranklist/',
        name: 'ranklist_index',
        component: RankListIndexView,
        meta: {
            requestAuth: true,
            description: '排行榜',
            isRoot: true,
        }
    },
    {
        path: '/discussion/',
        name: 'discussion_index',
        component: DiscussionView,
        meta: {
            requestAuth: true,
            description: '讨论区',
            isRoot: true,
        }
    },
    {
        path: '/message_board/',
        name: 'message_board_index',
        component: MessageBoardView,
        meta: {
            requestAuth: true,
            description: '留言板',
            isRoot: true,
        }
    },
    {
        path: '/user/bot/',
        name: 'user_bot_index',
        component: UserBotIndexView,
        meta: {
            requestAuth: true,
            description: '我的Bot',
            isRoot: true,
        }
    },
    {
        path: '/user/account/login/',
        name: 'user_account_login',
        component: UserAccountLoginView,
        meta: {
            requestAuth: false,
            description: '登录',
            isRoot: true,
        }
    },
    {
        path: '/user/account/register/',
        name: 'user_account_register',
        component: UserAccountRegisterView,
        meta: {
            requestAuth: false,
            description: '注册',
            isRoot: true,
        }
    },
    {
        path: '/404/',
        name: '404',
        component: NotFound,
        meta: {
            requestAuth: false,
            description: '',
            isRoot: true,
        }
    },
    {
        path: '/:catchAll(.*)',
        redirect: '/404/',
    },
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

router.beforeEach((to, from, next) => {
    if(to.meta.isRoot) store.commit("updateBackPage", "");
    if(to.meta.requestAuth && !store.state.user.is_login) {
        next({name: "user_account_login"});
    } else {
        next();
    }
})

export default router
