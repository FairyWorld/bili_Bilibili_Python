import random
import time
from Method import *


class Daily(User):
    def __init__(self):
        super().__init__()

    def receive_message(self, data_get):  # 接受get_requests返回的数据,并筛选处理
        if data_get['code'] == 0:
            self.logger.info("-------->"+data_get['data']['uname']+"<--------")
            self.logger.info(
                data_get['data']['uname'] + " 当前经验值为：" + str(data_get['data']['level_info']['current_exp']))
            self.logger.info(data_get['data']['uname'] + " 当前硬币数为：" + str(data_get['data']['money']))
        elif data_get['code'] == -101:
            self.logger.info(data_get['message'] + "请检查cookie")
        elif data_get['code'] == -111:
            self.logger.info(data_get['message'] + "请检查csrf")
        else:
            self.logger.info(data_get['message'])

    def cope_dynamic(self, dynamic):  # 接收动态数据，筛选视频bv和title
        title = []
        bv = []
        if dynamic['code'] == 0:
            for i in range(len(dynamic['data']['items'])):
                if dynamic['data']['items'][i]['basic']['comment_type'] == 1:
                    title.append(dynamic['data']['items'][i]['modules']['module_dynamic']['major']['archive']['title'])
                    bv.append(dynamic['data']['items'][i]['modules']['module_dynamic']['major']['archive']['bvid'])
            return title, bv
        elif dynamic['code'] == -101:
            self.logger.info(dynamic['message'] + "请检查cookie")
        else:
            self.logger.info(dynamic['message'])

    def start_drop_coin(self, title, bv, csrf):  # 开始投币
        final_bv = list(set(bv))
        final_title = list(set(title))
        for i in range(len(final_bv)):
            if len(final_bv) >= 5:
                self.logger.info("视频标题：" + final_title[i] + "，视频bv：" + final_bv[i])
                data = self.drop_coin(final_bv[i], csrf)  # 打赏视频
                self.cope_drop_coin(data)
            else:
                self.logger.info("视频标题：" + final_title[i] + "，视频bv：" + final_bv[i])
                data = self.drop_coin(final_bv[i], csrf)  # 打赏视频
                self.cope_drop_coin(data)
                if i == len(final_bv) - 1:
                    self.logger.info("已经投币"+str(len(final_bv))+"个视频，不足5次跳转推荐视频投币")
                    for j in range(5 - len(final_bv)):
                        recommend_data = self.recommend(final_bv[0])  # 推荐视频
                        title_re, bv_re = self.cope_recommend(recommend_data)
                        self.logger.info("视频标题：" + title_re[j] + "，视频bv：" + bv_re[j])
                        data = self.drop_coin(bv_re, csrf)  # 打赏视频
                        self.cope_drop_coin(data)
            if i == 4:
                self.logger.info("视频数量到5,到此结束")
                break
            time.sleep(random.randint(3, 5))

    def cope_drop_coin(self, data):  # 接收打赏返回数据，处理数据
        if data['code'] == 0:
            self.logger.info("投币成功 ௹ ✓")
        elif data['code'] == -101:
            self.logger.info(data['message'] + "请检查cookie")
        elif data['code'] == -111:
            self.logger.info(data['message'] + "请检查csrf")
        elif data['code'] == -104:
            self.logger.info(data['message'] + "硬币不足")
        else:
            self.logger.info(data['message'])

    def cope_share(self, data):  # 接收分享返回数据，处理数据
        if data['code'] == 0:
            self.logger.info("分享成功 ௹ ✓")
        elif data['code'] == -101:
            self.logger.info(data['message'] + "请检查cookie")
        elif data['code'] == -111:
            self.logger.info(data['message'] + "请检查csrf")
        else:
            self.logger.info(data['message'])

    def cope_recommend(self, data):  # 接收推荐返回数据，处理数据
        title = []
        bv = []
        if data['code'] == 0:
            for i in range(len(data['data'])):
                title.append(data['data'][i]['title'])
                bv.append(data['data'][i]['bvid'])
                if i == 4:
                    break
            return title, bv
        elif data['code'] == -101:
            self.logger.info(data['message'] + "请检查cookie")
        elif data['code'] == -111:
            self.logger.info(data['message'] + "请检查csrf")
        else:
            self.logger.info(data['message'])

    def decorate(self):
        self.logger.info("开始每日登录经验+5,一天只能加一次 ☆*: .｡. o(≧▽≦)o .｡.:*☆")
        self.logger.info("开始投币，每次投币5个硬币")
        self.logger.info("开始分享，每次分享1个视频")
        self.logger.info("一天只需要运行一次，请勿重复运行，以免硬币流失")

    def run_daily(self):
        self.decorate()
        for i in range(len(self.a)):
            self.headers['Cookie'] = self.a[i]  # 获取cookies设置到headers中
            data = self.get_requests(self.url)  # 获取用户信息,返回数据
            self.receive_message(data)  # 接收用户信息，处理数据，输出来给我们看
            dynamic = self.consult_dynamic(self.url2)  # 获取动态信息
            title, bv = self.cope_dynamic(dynamic)  # 处理动态信息
            self.start_drop_coin(title, bv, self.csrf[i])  # 投币函数,输出视频标题和bv信息
            share_dynamic = self.share_dynamic(bv[0], title[0], self.csrf[i])  # 分享动态，只分享第一个视频
            self.cope_share(share_dynamic)  # 输出分享返回数据
            data = self.get_requests(self.url)  # 获取用户信息,返回数据
            self.receive_message(data)
            self.logger.info("================分割线====================")
            if i == len(self.a) - 1:
                break
            time.sleep(5)


if __name__ == '__main__':
    daily = Daily()
    daily.run_daily()