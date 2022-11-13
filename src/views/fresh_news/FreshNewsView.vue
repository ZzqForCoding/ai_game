<template>
    <el-row style="margin-top: 40px;">
        <el-col :span="5" :offset="2">
            <!-- 个人信息 -->
            <el-card class="profile-card" shadow="always">
                <div class="background">
                </div>
                <div class="content">
                    <el-row>
                        <el-col :span="6" :offset="9">
                            <div class="photo">
                                <img :src="$store.state.user.photo" alt="" class="" style="user-select: none;">
                            </div>
                        </el-col>
                    </el-row>
                    <el-row>
                        <el-col :span="20" :offset="2">
                            <div class="username">
                                {{ $store.state.user.username }}
                            </div>

                            <div class="profession">
                                Web Developer at Webestica
                            </div>

                            <div class="description">
                                I'd love to change the world, but they won’t give me the source code.
                            </div>

                            <div class="friend-num-container">
                                <div>
                                    <h6 class="num">256</h6>
                                    <small class="text">Post</small>
                                </div>
                                <div class="vertical-divider"></div>
                                <div>
                                    <h6 class="num">2.5K</h6>
                                    <small class="text">Followers</small>
                                </div>
                                <div class="vertical-divider"></div>
                                <div>
                                    <h6 class="num">365</h6>
                                    <small class="text">Following</small>
                                </div>
                            </div>

                            <div class="horizontal-divider"></div>
                        </el-col>
                    </el-row>
                </div>
            </el-card>
        </el-col>
        <el-col :span="14" :offset="1">
            <el-card class="post-card">
                <div class="post-a-fresh-news">
                    <div class="avatar-container">
                        <el-avatar :src="$store.state.user.photo" />
                    </div>

                    <el-input
                        v-model="input_fresh_news"
                        :rows="4"
                        class="input-fresh-news"
                        resize="none"
                        type="textarea"
                        placeholder="Share your thoughts..."
                    />
                </div>
                <el-divider style="margin-top: 5px; margin-bottom: 0px;" />
                <div class="post-container">
                    <div class="post-container-right">
                        <el-button type="primary" size="small" @click="postFreshNews(input_fresh_news)">发送</el-button>
                    </div>
                </div>
            </el-card>


            <el-card class="box-card" style="margin-top: 20px;" v-for="item in freshNews" :key="item.id">
                <div class="post-message-container">
                    <el-avatar :src="item.photo" />
                    <div class="post-message">
                        <h6>{{ item.username }}</h6>
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
                    <div>
                        <svg t="1664632040191" class="icon" viewBox="0 0 1024 1024" version="1.1"
                            xmlns="http://www.w3.org/2000/svg" p-id="4832" width="25" height="25">
                            <path
                                d="M71.9 909.8c-2.2 8.4-12.5 5.9-11.9-2.9 13.1-187 71.1-284.1 128.1-352.8C274.7 449.9 469.8 352.7 604 341.3c10.6-0.9 18.9-11.7 18.9-24.8V157.9c0-21.7 21.1-32.9 34.1-18.2l299.5 339.5c9 10.2 8.6 27.6-0.8 37.2L662 817.6c-13.2 13.5-33.3 2-33.3-19V604.3c0-12.9-8.1-23.7-18.6-24.7-85.7-8.5-287.5 10.3-369.1 70.2-34.8 25.4-129.8 112.4-169.1 260z"
                                p-id="4833"></path>
                        </svg>
                        <span>转发（3）</span>
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
                        <el-avatar size="small" :src="child.photo" />
                    </div>
                    <div class="right">
                        <div class="info">
                            <h6>{{ child.username }}</h6>
                            <span class="time">{{ child.since }}</span>
                            <span v-if="child.reply !== item.username" class="reply">回复 <a>{{ child.reply }}</a>
                                的评论</span>
                            <a class="post-comment-right-reply" @click="openComment(item.id + '-' + child.id)">回复</a>
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
        </el-col>
    </el-row>
</template>

<script>
import $ from 'jquery';
import { ref } from 'vue';
import { useStore } from 'vuex';
import { ElMessage } from 'element-plus';

export default {
    name: 'FreshNewsView',
    setup() {
        const store = useStore();
        let input_fresh_news = ref('');
        let input_comment = ref('');
        let freshNews = ref([]);
        let openCommentId = ref(-1);

        const getFreshNews = () => {
            $.ajax({
                url: "https://aigame.zzqahm.top/backend/playervoice/freshnews/getlist/",
                type: "get",
                headers: {
                    "Authorization": "Bearer " + store.state.user.access,
                },
                success(resp) {
                    freshNews.value = resp.freshNews;
                },
                error() {
                    store.dispatch("logout");
                }
            });
        }

          getFreshNews();

        const postFreshNews = (msg, flag) => {
            if(msg.trim() === "") {
                ElMessage.error("please input your mood~");
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
                success() {
                     ElMessage({
                        showClose: true,
                       message: '动态发布成功',
                         type: 'success',
                    });
                    getFreshNews();
                    if(flag) {
                         input_comment.value = "";
                    } else {
                        input_fresh_news.value = "";
                     }
                     let element = document.getElementsByClassName('post-comment-input' + openCommentId.value)[0];
                    element.classList.remove('post-comment-input-animation');
                    openCommentId.value = -1;
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

        return {
            input_fresh_news,
            input_comment,
            freshNews,
            postFreshNews,
            openCommentId,
            openComment,
            clickLikeFreshNews,
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

.post-content {
    color: #676A79;
    font-size: 15px;
    padding: 0 15px 15px 15px;
}

.post-tools {
    display: flex;
    justify-content: center;
    align-items: center;
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

.post-comments .right .info .post-comment-right-reply {
    margin-left: 10px;
    color: #95a5a6;
    cursor: pointer;
    font-size: 13.125px;
}

.post-comments .right .info .post-comment-right-reply:hover {
    color: #337ab7;
    text-decoration: none;
}

.el-card:deep(.el-card__body) {
    padding: 0 0 !important;
}

.profile-card {
    border: none !important;
}

.profile-card .background {
    background-image: url('@/assets/images/01.jpg');
    background-position: center;
    background-size: cover;
    background-repeat: no-repeat;
    height: 50px;
}

.profile-card .photo>img {
    margin-top: -40px;
    border-radius: 10px 10px 0 0;
    border: 3px solid white;
    width: 100%;
    height: 100%;
}

.profile-card .username {
    text-align: center;
    font-size: 20px;
    font-weight: 700;
    height: 20px;
    line-height: 20px;
    margin-top: 18px;
    user-select: text;
}

.profile-card .profession {
    margin-top: 5px;
    color: #676A79;
    font-size: 12px;
    text-align: center;
}

.profile-card .description {
    color: #676A79;
    font-size: 13px;
    text-align: center;
    width: 90%;
    margin: 15px auto;
}

.profile-card .friend-num-container {
    display: flex;
    justify-content: space-between;
}

.profile-card .friend-num-container div:nth-child(1) {
    margin-left: 10px;
}

.profile-card .friend-num-container div:last-child {
    margin-right: 10px;
}

.profile-card .friend-num-container .num {
    text-align: center;
    height: 12px !important;
    line-height: 12px !important;
    margin-bottom: 0px;
}

.profile-card .friend-num-container .text {
    font-size: 8px;
    color: #676A79;
    user-select: none;
}

.profile-card .vertical-divider {
    height: 40px;
    border-left: 1px solid #CCCCCC;
    margin: 0 5px;
    padding: 8px 0;
}

.profile-card .horizontal-divider {
    width: 100%;
    border-top: 1px solid #CCCCCC;
    margin: 10px 0px;
    padding: 0 10px;
    margin-bottom: 15px;
}
</style>