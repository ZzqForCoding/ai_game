<template>
    <el-card class="post-card" v-if="showPostComment">
        <div class="post-a-fresh-news">
            <div class="avatar-container">
                <el-avatar :src="$store.state.user.photo" />
            </div>

            <el-input v-model="input_fresh_news" :rows="4" class="input-fresh-news" resize="none" type="textarea"
                placeholder="Share your thoughts..." />
        </div>
        <el-divider style="margin-top: 5px; margin-bottom: 0px;" />
        <div class="post-container">
            <div class="post-container-right">
                <el-button type="primary" size="small" @click="postFreshNews(input_fresh_news)">发送</el-button>
            </div>
        </div>
    </el-card>
    <ul v-if="freshNews.length > 0" v-infinite-scroll="load" :infinite-scroll-disabled="isOver"
        style="margin: 0; padding: 0; list-style: none;">
        <li style="margin-top: 20px;" v-for="item in freshNews" :key="item.id">
            <el-card class="box-card" style="position: relative;">
                <span class="forward-desp" v-if="item.forwarded_id !== -1">
                    转发于
                    <span @click="enterPlayerSpace(item.forwarded_userId)"> {{ item.forwarded_username }} </span>
                    的动态
                </span>
                <el-button type="danger" text style="float: right; margin: 30px 20px 0 0;"
                    v-if="item.userId === $store.state.user.id" @click="openDeleteDialog(item)">
                    删除
                </el-button>
                <div class="post-message-container">
                    <el-avatar class="info-scale" :src="item.photo" @click="enterPlayerSpace(item.userId)" />
                    <div class="post-message">
                        <h6 class="info-scale" @click="enterPlayerSpace(item.userId)">{{ item.username }}</h6>
                        <span>{{ item.since }}</span>
                    </div>
                </div>
                <pre class="post-content">{{ item.content }}</pre>
                <el-divider style="margin-top: 5px; margin-bottom: 0px;" />
                <div class="post-tools">
                    <div @click="clickLikeFreshNews(item)">
                        <svg t="1664632066049" class="icon" viewBox="0 0 1024 1024" version="1.1"
                            xmlns="http://www.w3.org/2000/svg" p-id="6641" width="25" height="25">
                            <path
                                d="M513.5 921.6c-38.3 0-87.4-26.1-121.9-48-48.2-30.6-99.4-73.2-144.3-120-67.2-70-179.9-212.1-179.9-376.3 0-66 26.3-134.2 72.2-187.2 23.3-26.9 50.1-48.2 79.7-63.3 32.1-16.4 66-24.8 100.6-24.8 73.4 0 143.3 31.8 191.6 87.1 0.2 0.2 0.6 0.7 1.5 0.7s1.3-0.5 1.5-0.7c48.4-55.4 118.2-87.1 191.6-87.1 34.7 0 68.5 8.4 100.5 24.9 29.6 15.3 56.4 36.8 79.6 64 45.6 53.5 71.7 123.1 71.7 191 0 161.7-112.2 302.7-179.1 372.3-44.7 46.6-95.8 89-143.7 119.5-34.4 21.8-83.4 47.9-121.6 47.9zM319.9 158c-50.6 0-99.6 24.4-138 68.8-18 20.8-32.9 45.4-43 71.2-10.2 26-15.6 53.5-15.6 79.3 0 56.9 16.3 117.1 48.3 178.9 27.8 53.7 67.9 108.6 116 158.6 41.8 43.6 89.4 83.2 133.9 111.5 45.6 29 77.4 39.3 91.9 39.3s46.2-10.3 91.6-39.2c44.3-28.1 91.6-67.6 133.4-111 47.8-49.8 87.7-104.2 115.4-157.3 31.9-61.1 48-120.4 48-176.2 0-54.8-21.3-111.2-58.3-154.7-38-44.6-86.8-69.2-137.5-69.2-57.3 0-111.7 24.8-149.5 68-11 12.6-26.9 19.8-43.6 19.8s-32.6-7.2-43.6-19.8c-37.6-43.2-92.1-68-149.4-68z"
                                fill="" p-id="6642"></path>
                        </svg>
                        <!-- <svg t="1664632066049" class="icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="6641" width="25" height="25"><path d="M513.5 921.6c-38.3 0-87.4-26.1-121.9-48-48.2-30.6-99.4-73.2-144.3-120-67.2-70-179.9-212.1-179.9-376.3 0-66 26.3-134.2 72.2-187.2 23.3-26.9 50.1-48.2 79.7-63.3 32.1-16.4 66-24.8 100.6-24.8 73.4 0 143.3 31.8 191.6 87.1 0.2 0.2 0.6 0.7 1.5 0.7s1.3-0.5 1.5-0.7c48.4-55.4 118.2-87.1 191.6-87.1 34.7 0 68.5 8.4 100.5 24.9 29.6 15.3 56.4 36.8 79.6 64 45.6 53.5 71.7 123.1 71.7 191 0 161.7-112.2 302.7-179.1 372.3-44.7 46.6-95.8 89-143.7 119.5-34.4 21.8-83.4 47.9-121.6 47.9zM319.9 158c-50.6 0-99.6 24.4-138 68.8-18 20.8-32.9 45.4-43 71.2-10.2 26-15.6 53.5-15.6 79.3 0 56.9 16.3 117.1 48.3 178.9 27.8 53.7 67.9 108.6 116 158.6 41.8 43.6 89.4 83.2 133.9 111.5 45.6 29 77.4 39.3 91.9 39.3s46.2-10.3 91.6-39.2c44.3-28.1 91.6-67.6 133.4-111 47.8-49.8 87.7-104.2 115.4-157.3 31.9-61.1 48-120.4 48-176.2 0-54.8-21.3-111.2-58.3-154.7-38-44.6-86.8-69.2-137.5-69.2-57.3 0-111.7 24.8-149.5 68-11 12.6-26.9 19.8-43.6 19.8s-32.6-7.2-43.6-19.8c-37.6-43.2-92.1-68-149.4-68z" fill="#d81e06" p-id="6642"></path></svg> -->
                        <span v-if="!item.is_like">点赞</span>
                        <span v-else>取消点赞</span>
                        <span v-if="item.likes !== 0">({{ item.likes }})</span>
                    </div>
                    <div @click="openComment(item.id)">
                        <svg t="1664631879270" class="icon" viewBox="0 0 1024 1024" version="1.1"
                            xmlns="http://www.w3.org/2000/svg" p-id="2557" width="25" height="25">
                            <path
                                d="M622.56056 464.834794c0 27.928073 22.73684 50.64854 50.664913 50.64854 27.956725 0 50.693566-22.720468 50.693566-50.64854 0-27.928073-22.73684-50.66389-50.693566-50.66389C645.2974 414.171927 622.56056 436.907745 622.56056 464.834794"
                                p-id="2558"></path>
                            <path
                                d="M931.254178 211.459063c0-40.637536-33.05893-73.698512-73.728188-73.698512L166.471964 137.76055c-40.637536 0-73.727165 33.059953-73.727165 73.698512l0 506.796488c0 40.637536 33.088606 73.696466 73.727165 73.696466l251.16846 0 94.343715 94.28641 94.315062-94.28641 251.226788 0c40.669258 0 73.728188-33.05893 73.728188-73.696466l0-82.560344-0.089028-1.282203L931.254178 211.459063zM875.96699 695.220928c0 22.88522-18.558681 41.444924-41.443901 41.444924L579.446623 736.665853l-67.462484 67.490114-67.430762-67.490114L189.506587 736.665853c-22.88522 0-41.4746-18.559705-41.4746-41.444924L148.031986 234.493685c0-22.88522 18.58938-41.488927 41.4746-41.488927l645.01548 0c22.88522 0 41.443901 18.603707 41.443901 41.488927l0 396.579247 0 36.161594L875.965967 695.220928z"
                                p-id="2559"></path>
                            <path
                                d="M461.321272 464.834794c0 27.928073 22.735817 50.64854 50.662867 50.64854 27.929096 0 50.66389-22.720468 50.66389-50.64854 0-27.928073-22.734794-50.66389-50.66389-50.66389C484.057089 414.171927 461.321272 436.907745 461.321272 464.834794"
                                p-id="2560"></path>
                            <path
                                d="M300.083008 464.834794c0 27.928073 22.735817 50.64854 50.66389 50.64854 27.927049 0 50.662867-22.720468 50.662867-50.64854 0-27.928073-22.735817-50.66389-50.662867-50.66389C322.817802 414.171927 300.083008 436.907745 300.083008 464.834794"
                                p-id="2561"></path>
                        </svg>
                        <span>评论</span>
                    </div>
                    <div @click="openForwardDialog(item)">
                        <svg t="1664632040191" class="icon" viewBox="0 0 1024 1024" version="1.1"
                            xmlns="http://www.w3.org/2000/svg" p-id="4832" width="25" height="25">
                            <path
                                d="M71.9 909.8c-2.2 8.4-12.5 5.9-11.9-2.9 13.1-187 71.1-284.1 128.1-352.8C274.7 449.9 469.8 352.7 604 341.3c10.6-0.9 18.9-11.7 18.9-24.8V157.9c0-21.7 21.1-32.9 34.1-18.2l299.5 339.5c9 10.2 8.6 27.6-0.8 37.2L662 817.6c-13.2 13.5-33.3 2-33.3-19V604.3c0-12.9-8.1-23.7-18.6-24.7-85.7-8.5-287.5 10.3-369.1 70.2-34.8 25.4-129.8 112.4-169.1 260z"
                                p-id="4833"></path>
                        </svg>
                        <span>
                            转发
                            <span v-if="item.forward_count !== 0">({{ item.forward_count }})</span>
                        </span>
                    </div>
                </div>
                <el-divider style="margin-top: 0px; margin-bottom: 5px;" />
                <div class="post-comment" v-if="openCommentId === item.id">
                    <textarea :class="'post-comment-input' + item.id" placeholder="Please input" v-model="input_comment"
                        cols="40" rows="2" maxlength="3000" required title="回复"></textarea>
                    <el-button class="btn" text @click="postFreshNews(input_comment, item.id)" size="small">
                        提交评论
                    </el-button>
                </div>
                <div v-for="child in item.children" :key="child.id" class="post-comments">
                    <div class="avatar">
                        <el-avatar size="small" :src="child.photo" class="info-scale"
                            @click="enterPlayerSpace(child.userId)" />
                    </div>
                    <div class="right">
                        <div class="info">
                            <h6 class="info-scale" @click="enterPlayerSpace(child.userId)">{{ child.username }}</h6>
                            <span class="time">{{ child.since }}</span>
                            <span v-if="child.reply !== item.username" class="reply">回复 <a class="info-scale" @click="enterPlayerSpace(child.reply_id)">{{ child.reply }}</a>
                                的评论</span>
                            <a class="post-comment-right-reply" @click="openComment(item.id + '-' + child.id)">回复</a>
                            <a class="post-comment-right-del" v-if="child.userId === $store.state.user.id" @click="openDeleteDialog(child)">删除</a>
                        </div>
                        <div class="content">
                            {{ child.content }}
                        </div>
                        <div class="post-reply-comment" v-if="openCommentId === item.id + '-' + child.id">
                            <textarea :class="'post-comment-input' + item.id + '-' + child.id"
                                placeholder="Please input" v-model="input_comment" cols="90" rows="2" maxlength="3000"
                                required title="回复"></textarea>
                            <el-button class="btn" text @click="postFreshNews(input_comment, child.id)" size="small">
                                提交评论
                            </el-button>
                        </div>
                    </div>
                </div>
            </el-card>
        </li>
    </ul>
    <div v-else-if="freshNews.length == 0 && !loading">
        <el-card class="box-card" style="margin-top: 20px;">
            <template #header>
                <div class="card-header">
                    <span>快发布发布你的动态叭!</span>
                </div>
            </template>
        </el-card>
    </div>
    <el-dialog v-model="showDeleteDialog" title="删除动态" width="30%">
        <span v-if="curOpeItem">
            确认删除内容为
            <span class="content-ellipsis"> {{ curOpeItem.content }} </span>
            的动态吗?
        </span>
        <template #footer>
            <span class="dialog-footer">
                <el-button type="primary" @click="removeFreshNews(curOpeItem.id, curOpeItem.forwarded_id)">确认删除
                </el-button>
                <el-button @click="cancelDeleteBot">取消</el-button>
            </span>
        </template>
    </el-dialog>
    <el-dialog v-model="showForwardDialog" title="转发动态" width="30%">
        <span v-if="curOpeItem">
            确认转发内容为
            <span class="content-ellipsis"> {{ curOpeItem.content }} </span>
            的动态吗?
        </span>
        <template #footer>
            <span class="dialog-footer">
                <el-button type="primary" @click="forwardFreshNews(curOpeItem)">确认转发</el-button>
                <el-button @click="cancelForwardBot">取消</el-button>
            </span>
        </template>
    </el-dialog>
    <p v-if="loading" class="desp">加载中...</p>
    <p v-if="isOver" class="desp">到底啦!</p>
</template>

<script>
import { ref, onMounted } from 'vue';
import { useStore } from 'vuex';
import $ from 'jquery';
import router from '@/router';
import { ElMessage } from 'element-plus';

export default {
    name: 'FreshNewsList',
    props: {
        freshNewsUrl: {
            type: String,
            required: true
        },
        showPostComment: {
            type: Boolean,
            required: true
        }
    },
    setup(props) {
        const store = useStore();
        let input_fresh_news = ref('');
        let input_comment = ref('');
        let freshNews = ref([]);
        let openCommentId = ref(-1);
        let page = ref(0);
        let loading = ref(false);
        let isOver = ref(false);
        let showDeleteDialog = ref(false);
        let curOpeItem = ref(null);
        let showForwardDialog = ref(false);

        onMounted(() => {
            load();
        });

        const getFreshNews = (cur) => {
            $.ajax({
                url: props.freshNewsUrl,
                type: "get",
                headers: {
                    "Authorization": "Bearer " + store.state.user.access,
                },
                data: {
                    page: cur,
                },
                success(resp) {
                    if(cur == 1) freshNews.value = resp.freshNews;
                    else freshNews.value = freshNews.value.concat(resp.freshNews);
                    if(cur >= resp.count / 4.0) {
                        isOver.value = true;
                    }
                    loading.value = false;
                    page.value = cur;
                },
                error() {
                    store.dispatch("logout");
                }
            });
        }

        const postFreshNews = (msg, flag) => {
            if(msg.trim() === "") {
                ElMessage.error("不能发布空动态！");
                return;
            }
            if(msg.length > 5000) {
                ElMessage.error("动态不能超过5000个字符！");
                return;
            }
            $.ajax({
                url: "https://aigame.zzqahm.top/backend/playervoice/freshnews/post/",
                headers: {
                    "Authorization": "Bearer " + store.state.user.access,
                },
                type: "post",
                data: {
                    content: msg,
                    parent_id: flag,
                 },
                success(resp) {
                    if(resp.result === 'success') {
                        ElMessage({
                            showClose: true,
                            message: '动态发布成功',
                            type: 'success',
                        });
                        load(1);
                        if(flag) {
                            input_comment.value = "";
                        } else {
                            input_fresh_news.value = "";
                        }
                        // 如果玩家发布动态且动态不是评论，则动态数 + 1
                        if(!flag) {
                            store.commit("updateUser", {
                                'id': store.state.user.id,
                                'username': store.state.user.username,
                                'photo': store.state.user.photo,
                                'is_login': store.state.user.is_login,
                                'job': store.state.user.job,
                                'desp': store.state.user.desp,
                                'botCnt': store.state.user.botCnt,
                                'recordCnt': store.state.user.recordCnt,
                                'freshNewsCnt': store.state.user.freshNewsCnt + 1,
                                'isSuperUser': store.state.user.isSuperUser,
                                'phone': store.state.user.phone,
                            });
                        }
                        let element = document.getElementsByClassName('post-comment-input' + openCommentId.value)[0];
                        element.classList.remove('post-comment-input-animation');
                        openCommentId.value = -1;
                    } else {
                        ElMessage.error(resp.result);
                    }


                },
                error() {
                    store.dispatch("logout");
                }
            });
        }
 
        const openComment = id => {
            input_comment.value = "";
            if(openCommentId.value !== -1) {
                let element = document.getElementsByClassName('post-comment-input' + openCommentId.value)[0];
                element.classList.remove('post-comment-input-animation');
            }
            if(openCommentId.value === id) {
                openCommentId.value = -1;
            }
            else {
                openCommentId.value = id;
                setTimeout(() => {
                    let element = document.getElementsByClassName('post-comment-input' + id)[0];
                    element.classList.add('post-comment-input-animation');
                }, 1);
            }
        };

        const clickLikeFreshNews = item => {
            if(item.is_like) {
                $.ajax({
                    url: "https://aigame.zzqahm.top/backend/playervoice/freshnews/dellike/",
                    headers: {
                        "Authorization": "Bearer " + store.state.user.access,
                    },
                    type: "post",
                    data: {
                        freshNewsId: item.id,
                    },
                    success() {
                        item.is_like = false;
                        item.likes -= 1;
                    },
                    error() {
                        store.dispatch("logout");
                    }
                });
            } else {
                $.ajax({
                    url: "https://aigame.zzqahm.top/backend/playervoice/freshnews/addlike/",
                    headers: {
                        "Authorization": "Bearer " + store.state.user.access,
                    },
                    type: "post",
                    data: {
                        freshNewsId: item.id,
                    },
                    success() {
                        item.is_like = true;
                         item.likes += 1;
                    },
                    error() {
                        store.dispatch("logout");
                    }
                });
            }
        }

        const load = (toPage) => {
            if(!loading.value && !isOver.value || toPage) {
                loading.value = true;
                if(toPage) {
                    getFreshNews(toPage);
                    isOver.value = false;
                }
                else getFreshNews(page.value + 1);
            }
        }

        const enterPlayerSpace = userId => {
            router.push({ 
                name: "myspace_index",
                params: {
                    userId
                }
            });
        }

        const removeFreshNews = (id, forwarded_id) => {
            showDeleteDialog.value = false;
            curOpeItem.value = null;
            $.ajax({
                url: "https://aigame.zzqahm.top/backend/playervoice/freshnews/remove/",
                headers: {
                    "Authorization": "Bearer " + store.state.user.access,
                },
                type: "post",
                data: {
                    freshNewsId: id,
                },
                success(resp) {
                    if(resp.result === 'success') {
                        for(let i = 0; i < freshNews.value.length; i++) {
                            if(freshNews.value[i].id === id) {
                                freshNews.value.splice(i, 1);
                                // 如果玩家删除动态且动态不是评论，则动态数 - 1
                                store.commit("updateUser", {
                                    'id': store.state.user.id,
                                    'username': store.state.user.username,
                                    'photo': store.state.user.photo,
                                    'is_login': store.state.user.is_login,
                                    'job': store.state.user.job,
                                    'desp': store.state.user.desp,
                                    'botCnt': store.state.user.botCnt,
                                    'recordCnt': store.state.user.recordCnt,
                                    'freshNewsCnt': store.state.user.freshNewsCnt - 1,
                                    'isSuperUser': store.state.user.isSuperUser,
                                    'phone': store.state.user.phone,
                                });
                                break;
                            }
                            if(freshNews.value[i].children && freshNews.value[i].children.length > 0) {
                                for(let j = 0; j < freshNews.value[i].children.length; j++) {
                                    if(freshNews.value[i].children[j].id === id) {
                                        freshNews.value[i].children.splice(j, 1);
                                        break;
                                    }
                                }
                            }
                        }
                        if(forwarded_id != -1) {
                            // 转发数 - 1
                            for(let i = 0; i < freshNews.value.length; i++) {
                                if(freshNews.value[i].id === forwarded_id) {
                                    freshNews.value[i].forward_count -= 1;
                                    break;
                                }
                            }
                        }
                        ElMessage({
                            message: '删除成功',
                            type: 'success',
                        });
                    } else {
                        ElMessage.error(resp.result);
                    }
                },
                error() {
                    store.dispatch("logout");
                }
            });
        }

        const openDeleteDialog = (item) => {
            curOpeItem.value = item;
            showDeleteDialog.value = true;
        }

        const cancelDeleteBot = () => {
            showDeleteDialog.value = false;
            curOpeItem.value = null;
        }

        const forwardFreshNews = (item) => {
            let forwarded_id = item.forwarded_id !== -1 ? item.forwarded_id : item.id;
            $.ajax({
                url: "https://aigame.zzqahm.top/backend/playervoice/freshnews/forward/",
                headers: {
                    "Authorization": "Bearer " + store.state.user.access,
                },
                type: "post",
                data: {
                    forwarded_id,
                },
                success(resp) {
                    if(resp.result === 'success') {
                        ElMessage({
                            message: '转发成功',
                            type: 'success',
                        });
                        load(1);
                        showForwardDialog.value = false;
                        curOpeItem.value = null;
                        store.commit("updateUser", {
                            'id': store.state.user.id,
                            'username': store.state.user.username,
                            'photo': store.state.user.photo,
                            'is_login': store.state.user.is_login,
                            'job': store.state.user.job,
                            'desp': store.state.user.desp,
                            'botCnt': store.state.user.botCnt,
                            'recordCnt': store.state.user.recordCnt,
                            'freshNewsCnt': store.state.user.freshNewsCnt + 1,
                            'isSuperUser': store.state.user.isSuperUser,
                            'phone': store.state.user.phone,
                        });
                    } else {
                        ElMessage.error(resp.result);
                    }
                },
                error() {
                    store.dispatch("logout");
                }
            });
        };

        const openForwardDialog = (item) => {
            curOpeItem.value = item;
            showForwardDialog.value = true;
        }

        const cancelForwardBot = () => {
            showForwardDialog.value = false;
            curOpeItem.value = null;
        }

        return {
            input_fresh_news,
            input_comment,
            freshNews,
            postFreshNews,
            openCommentId,
            openComment,
            clickLikeFreshNews,
            load,
            loading,
            isOver,
            enterPlayerSpace,
            removeFreshNews,
            curOpeItem,
            showDeleteDialog,
            openDeleteDialog,
            cancelDeleteBot,
            forwardFreshNews,
            showForwardDialog,
            openForwardDialog,
            cancelForwardBot,
        };
    }
}
</script>

<style scoped>
.avatar-container {
    width: 70px;
    display: flex;
    margin-top: 10px;
    justify-content: center;
}

.post-a-fresh-news {
    display: flex;
}

.post-a-fresh-news:deep(.el-textarea__inner) {
    background-color: #FFFFFF;
    box-shadow: 0 0 0 0;
}

.post-container {
    line-height: 35px;
    height: 35px;
}

.post-container-right {
    float: right;
    margin-right: 10px;
}

.post-message-container {
    display: flex;
    padding: 15px;
    width: 70%;
}

.post-message {
    margin-left: 10px;
}

.post-message h6 {
    font-size: 15px;
    margin: 0;
    display: inline-block;
    margin-right: 10px;
}

.post-message span::before {
    content: "•";
    color: inherit;
    padding-left: 2px;
    padding-right: 5px;
    opacity: 0.8;
}

.post-message span {
    color: #676A79;
    font-size: 13.125px;
}

.info-scale:hover {
    transform: scale(1.2);
    transition: 100ms;
    cursor: pointer;
}

.post-content {
    color: #676A79;
    font-size: 15px;
    padding: 0 15px 15px 15px;
}

.post-tools {
    display: flex;
    justify-content: center;
    align-items: center;
    user-select: none;
}

.post-tools div {
    border-radius: 6px;
    margin: 3px 6px;
    width: 32%;
    height: 35px;
    display: flex;
    justify-content: center;
    align-items: center;
}

.post-tools div span {
    font-size: 13.125px;
    color: #676A79;
    margin-left: 5px;
}

.post-tools div:hover {
    background-color: #EAECED;
    /* color: #0f6fec; */
    cursor: pointer;
}

.post-comment {
    margin: 10px 20px;
    height: auto;
}

.post-comment .btn {
    float: right;
    margin-bottom: 5px;
}

.post-comment textarea {
    transition: width 2s;
    transition-delay: .1s;
}

.post-comment-input-animation {
    width: 100%;
    padding: 5px 5px;
    border: 1px solid rgba(34, 36, 38, 0.15);
    resize: vertical;
    color: rgba(0, 0, 0, 0.87);
    box-shadow: 0 0 0 0 transparent inset;
    font-size: 1em;
    line-height: 1.2857;
    border-radius: 4px;
    white-space: pre-wrap;
    overflow-wrap: break-word;
}

.post-reply-comment {
    height: 60px;
    margin: 5px 20px 5px 0;
}

.post-reply-comment .btn {
    float: right;
}

.post-comments {
    display: flex;
    margin: 5px 0px 10px 30px;
}

.post-comments .right .info h6 {
    font-size: 15px;
    margin: 0;
    display: inline-block;
    margin-right: 10px;
}

.post-comments .right .info .time {
    color: #676A79;
    font-size: 13.125px;
}

.post-comments .right .info .time::before {
    content: "•";
    color: inherit;
    padding-left: 2px;
    padding-right: 5px;
    opacity: 0.8;
}

.post-comments .right .info .reply {
    margin-left: 10px;
    color: #95a5a6;
    cursor: pointer;
    font-size: 13.125px;
}

.post-comments .right .info .reply a {
    color: #337ab7;
    text-decoration: underline;
}

.post-comments .right {
    margin-left: 10px;
    width: 100%;
}

.post-comments .right .content {
    margin-top: 10px;
}

.post-comments .right .info .post-comment-right-reply, .post-comments .right .info .post-comment-right-del {
    margin-left: 10px;
    color: #95a5a6;
    cursor: pointer;
    font-size: 13.125px;
}

.post-comments .right .info .post-comment-right-reply:hover {
    color: #3366CC;
    text-decoration: none;
}

.post-comments .right .info .post-comment-right-del:hover {
    color: #FF0033;
    text-decoration: none;
}

.el-card:deep(.el-card__body) {
    padding: 0 0 !important;
}

.desp {
    color: #13ff03;
    text-align: center;
}

.forward-desp {
    font-size: 12px;
    position: absolute;
    right: 0;
    margin: 5px 10px 0 0;
}

.forward-desp span {
    font-weight: 600;
    right: 0;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    width: 40px;
    display: inline-block;
    position: relative;
    top: 3px;
    text-align: center;
}

.forward-desp span:hover {
    transform: scale(1.2);
    transition: 100ms;
    cursor: pointer;
}

.content-ellipsis {
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    width: 100px;
    display: inline-block;
    position: relative;
    top: 5px;
    text-align: center;
    font-weight: 600;
}
</style>