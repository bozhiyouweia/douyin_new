import json
import time
import re

import douyin_mongo
db = douyin_mongo.douyin_mongo()

def write_date(publish_dates):

    with open(r"c:\Users\wenxin\Nox_share\Other\anjian11.txt","w",encoding="utf-8") as f:
        f.write(publish_dates)



#发布时间 时间戳转换
def publish_time(timeStamp):
    timeArray = time.localtime(timeStamp)
    date_time = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    return date_time

#当前时间戳转换
def reptile_t():
    now = int(time.time())  # 1533952277
    timeArray = time.localtime(now)
    otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    return otherStyleTime


def reptile_d():
    now = int(time.time())  # 1533952277
    timeArray = time.localtime(now)
    otherStyleTime = time.strftime("%Y-%m-%d", timeArray)
    return otherStyleTime

def write_error(message):
    with open("mitmdu_error.txt","a",encoding="utf-8") as f:
        f.write(message)

def write_user(message):
    with open("userurl.txt", "a", encoding="utf-8") as f:
        f.write(message)

def write_content(message):
    with open("contenturl.txt", "a", encoding="utf-8") as f:
        f.write(message)
#必须的格式
def response(flow):
    #通过抓包软件获取请求的接口
    # url1 = "https://aweme.snssdk.com/aweme/v1/user/?sec_user_id="  #账号信息链接
    # url2 = "https://aweme.snssdk.com/aweme/v1/aweme/post/?max_cursor=0&sec_user_id=" #前二十条信息链接
    #https://aweme-hl.snssdk.com/aweme/v1/user/?sec_user_id  新账号
    #https://aweme-hl.snssdk.com/aweme/v1/forward/list/?user_id
    # https://aweme-hl.snssdk.com/aweme/v1/forward/list/?user_id
    #                https://aweme-hl.snssdk.com/aweme/v1/user/?user_id=
    try:
        url_list = ["https://aweme-hl.snssdk.com/aweme/v1/user/?sec_user_id",
                    "https://aweme-eagle-hl.snssdk.com/aweme/v1/user/?sec_user_id=",
                    "https://aweme-hl.snssdk.com/aweme/v1/forward/list/?user_id"
                    ]
        # for i,url in enumerate(url_list):
        #     if i == 0:

        if "/aweme/v1/user/" in flow.request.url:

            #数据的解析
            #flow.request.url.startswith(url_list[0]) or flow.request.url.startswith(url_list[1])
            print("有有有有有有有有有有有有有有有有有有有有有有有有有有有有有有有有有有有有有有有有有有有有")
            print(flow.response.text)
            data = json.loads(flow.response.text)
            nickname = data["user"]["nickname"]#分享id
            douyin_id = data["user"]["short_id"]#抖音号  short_id 或unique_id
            douyin_unique_id = data["user"]["unique_id"]
            verify = data["user"]["enterprise_verify_reason"]
            signature = data["user"]["signature"]
            total_favorited = data["user"]["total_favorited"] #获赞数
            following_count = data["user"]["following_count"]  # 关注数
            followers_count = data["user"]["mplatform_followers_count"]  # 粉丝数
            aweme_count = data["user"]["aweme_count"]  # 作品数
            dongtai_count = data["user"]["dongtai_count"]  # 动态数
            like_count = data["user"]["favoriting_count"]  # 喜欢数
            uid = data["user"]["uid"]
            share_url = data["user"]["share_info"]["share_url"]
            reptile_time = reptile_t()
            reptile_date = reptile_d()
            # print("账号信息:",douyin_info)
            #nickname,douyin_id,douyin_unique_id,verify,signature,
            # total_favorited,following_count,followers_count,aweme_count,dongtai_count,
            # like_count,reptile_time,reptile_date
            print("***************************************************")
            print(nickname,douyin_id,douyin_unique_id,verify,signature,
                total_favorited,following_count,followers_count,aweme_count,dongtai_count,
                like_count,reptile_time,reptile_date,share_url)
            message = {
                "nickname":nickname,
                "userurl":flow.request.url,
                "douyin_id":douyin_id,
                "douyin_unique_id": douyin_unique_id,
                "uid": uid

            }
            #获取账号链接
            # message = str(message) + "\n"
            # write_user(message)

            # n = [nickname, douyin_id, douyin_unique_id, verify, signature,
            # total_favorited, following_count, followers_count, aweme_count, dongtai_count,
            # like_count, reptile_time, reptile_date]
            # with open("ww.txt","a",encoding="utf-8") as f:
            #     data = str(n) + "\n"
            #     f.write(data)
            #save_userData


            if nickname:
                result = db.save_userData(nickname,douyin_id,douyin_unique_id,verify,signature,
                    total_favorited,following_count,followers_count,aweme_count,dongtai_count,
                    like_count,reptile_time,reptile_date,share_url)
                if result:
                    db.updateurl(nickname,douyin_id,douyin_unique_id,reptile_date)



        elif flow.request.url.startswith(url_list[2]):
            # 数据的解析
            # with open("production.txt", "a", encoding="utf-8") as f:
            #获取动态链接
            # message = str(flow.request.url) + "\n"
            # write_content(message)
            #获取时间
            print("1111111111111111111111111111111111111111111111111111111111111111111")
            print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
            print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
            print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
            print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
            Dongtai_List = json.loads(flow.response.text)["dongtai_list"]
            pattern = re.compile('(.*-.*-.*) ')
            publish_times = publish_time(Dongtai_List[-1]["aweme"]["create_time"])
            publish_dates = pattern.findall(publish_times)[0]
            print(publish_dates)
            write_date(publish_dates)



            for user in Dongtai_List:
                nickname = user["aweme"]["author"]["nickname"]  # 昵称
                desc = user["aweme"]["desc"]  # 描述
                aweme_id = user["aweme"]["aweme_id"]
                create_time = publish_time(user["aweme"]["create_time"])
                try:
                    signature = (user["aweme"]["author"]["signature"]).replace("🧡","").replace("�","").replace("�","")  # 官方描述
                except Exception as e:
                    signature = ""
                print("signature$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$🥰")
                print(signature)
                comment_count = user["aweme"]["statistics"]["comment_count"]  # 评论数
                digg_count = user["aweme"]["statistics"]["digg_count"]  # 点赞数
                download_count = user["aweme"]["statistics"]["download_count"]  # 下载数
                play_count = user["aweme"]["statistics"]["play_count"]  # 不知
                share_count = user["aweme"]["statistics"]["share_count"]  # 分享数
                share_url = user["aweme"]["share_info"]["share_url"]
                # 时长
                try:
                    duration = user["aweme"]["music"]["duration"]
                except Exception as e:
                    duration = 0

                reptile_time = reptile_t()
                reptile_date = reptile_d()
                print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
                print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
                print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
                print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
                print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
                print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
                print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")

                # print(nickname,desc,aweme_id,create_time,signature,comment_count,digg_count,
                #       download_count,play_count,share_count,duration,share_url,reptile_time,reptile_date)
                if nickname:
                    db.sava_Content(nickname,desc,aweme_id,create_time,signature,comment_count,digg_count,
                      download_count,play_count,share_count,duration,share_url,reptile_time,reptile_date)


    except Exception as e:
        message = str(reptile_t()) + "出现错误" + str(e) + "\n"
        write_error(message)

