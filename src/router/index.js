import { createRouter, createWebHistory } from 'vue-router'
import PkIndexView from '@/views/pk/PkIndexView'
import RankListIndexView from '@/views/ranklist/RankListIndexView'
import RecordIndexView from '@/views/record/RecordIndexView'
import RecordContentView from '@/views/record/RecordContentView'
import DiscussionView from '@/views/discussion/DiscussionView'
import FreshNewsView from '@/views/fresh_news/FreshNewsView'
import MessageBoardView from '@/views/message_board/MessageBoardView'
import SpaceMainView from '@/views/myspace/SpaceMainView'
import NotFound from '@/views/error/NotFound'
import UserAccountLoginView from '@/views/user/account/UserAccountLoginView'
import UserAccountRegisterView from '@/views/user/account/UserAccountRegisterView'
import UserAccountAcWingWebReceiveCodeView from '@/views/user/account/UserAccountAcWingWebReceiveCodeView'
import PersonalInfoView from '@/views/user/PersonalInfoView'
import UserAccountQQReceiveCodeView from '@/views/user/account/UserAccountQQReceiveCodeView'
import store from '@/store'

const routes = [
    {
        path: '/',
        name: 'home',
        redirect: '/record/',
        meta: {
            requestAuth: true,
            description: '首页',
            isRoot: true,
        }
    },
    {
        path: '/pk/:game/',
        name: 'pk_index',
        component: PkIndexView,
        meta: {
            requestAuth: true,
            description: '对战界面',
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
            description: '回放界面',
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
        path: '/fresh_news/',
        name: 'fresh_news_index',
        component: FreshNewsView,
        meta: {
            requestAuth: true,
            description: '新鲜事',
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
        path: '/myspace/:userId/',
        name: 'myspace_index',
        component: SpaceMainView,
        meta: {
            requestAuth: true,
            description: '我的空间',
            isRoot: false,
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
        path: "/player/acwing/web/receive_code/",
        name: 'player_acwing_web_receive_code',
        component: UserAccountAcWingWebReceiveCodeView,
        meta: {
            requestAuth: false,
            description: '',
            isRoot: true,
        }
    },
    {
        path: '/user/personal_info',
        name: 'personal_info',
        component: PersonalInfoView,
        meta: {
            requestAuth: true,
            description: '个人信息',
            isRoot: true,
        }
    },
    {
        path: "/player/qq/receive_code/",
        name: 'player_qq_receive_code',
        component: UserAccountQQReceiveCodeView,
        meta: {
            requestAuth: false,
            description: '',
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

router.beforeEach((to) => {
    if(to.meta.isRoot) store.commit("updateBackPage", "");
})

export default router
