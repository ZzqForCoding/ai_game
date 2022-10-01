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
                <div class="el-divider el-divider--horizontal m-0" role="separator" style="--el-border-style:solid; margin-top: 5px; margin-bottom: 5px; margin-right: 7px;"></div>

                <div class="post-container">
                    <div class="post-container-right">
                        <el-button type="primary" size="small" @click="postFreshNews">发送</el-button>
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
                <div class="post-content">
                    {{ item.content }}
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
        let freshNews = ref([]);

        const getFreshNews = () => {
            $.ajax({
                url: "https://aigame.zzqahm.top/backend/playervoice/freshnews/getlist/",
                type: "get",
                success(resp) {
                    freshNews.value = resp.freshNews;
                }
            });
        }

        getFreshNews();

        const postFreshNews = () => {
            $.ajax({
                url: "https://aigame.zzqahm.top/backend/playervoice/freshnews/post/",
                headers: {
                    "Authorization": "Bearer " + store.state.user.access,
                },
                type: "post",
                data: {
                    content: input_fresh_news.value,
                },
                success() {
                    ElMessage({
                        showClose: true,
                        message: '动态发布成功',
                        type: 'success',
                    });
                    freshNews.value.unshift({
                        photo: store.state.user.photo,
                        username: store.state.user.username,
                        since: "刚刚",
                        id: freshNews.value.length == 0 ? 1 : freshNews.value[freshNews.value.length - 1].id + 1,
                        content: input_fresh_news.value,
                    });
                    input_fresh_news.value = "";
                }
            });
        }

        return {
            input_fresh_news,
            freshNews,
            postFreshNews,
        }
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
.post-a-fresh-news /deep/.el-textarea__inner {
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

.el-card /deep/  .el-card__body  {
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

.profile-card .photo > img {
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