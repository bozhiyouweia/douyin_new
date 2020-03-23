#按时更新id   开启mitmdump监听   开启按键 入库    全部数据入库 上传
import douyin_mongo
import datetime
import requests
import json
import time
import re
db = douyin_mongo.douyin_mongo()

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

def write_json(data):
    with open(r"E:\douyin_day\{0}抖音数据.txt".format(reptile_d()),"w",encoding="utf-8") as f:
        f.write(data)
def down_txt(data):
    with open("down_txt.txt","a",encoding="utf-8") as f:
        data = str(reptile_t()) + "账户数据下载数量down:1" + ",%s"%data + "\n"
        f.write(data)

def down_error(data):
    with open("down_error.txt", "a", encoding="utf-8") as f:
        data = str(reptile_t()) + "账户数据没值" + ",%s" % data + "\n"
        f.write(data)

# 获取前1天或N天的日期，beforeOfDay=1：前1天；beforeOfDay=N：前N天
def getDate(beforeOfDay):
    today = datetime.datetime.now()
    # 计算偏移量
    offset = datetime.timedelta(days=-beforeOfDay)
    # 获取想要的日期的时间
    re_date = (today + offset).strftime('%Y-%m-%d')  # %Y-%m-%d %H:%M:%S

    return re_date
def reptile_d():
    now = int(time.time())  # 1533952277
    timeArray = time.localtime(now)
    otherStyleTime = time.strftime("%Y-%m-%d", timeArray)
    return otherStyleTime

def get_data():
    date = datetime.datetime.now()
    strDate = date.strftime("%Y-%m-%d")
    print("时间",strDate)

    url = "http://218.241.201.165:30001/Logic/AccountInfoForWeb.ashx?FromDate=%s&ToDate=%s&PlatformID=5&AuditStatus=5"%(strDate,strDate)
    try:
        response = requests.get(url).text
    except Exception as e:
        print(e)
        response = requests.get(url).text
    data_list = json.loads(response)["data"]
    i = 0
    for data in data_list:
        if data["ThirdPartyPlatformName"] == "抖音":
            print(data)
            id = str(data["ID"]).strip()
            accountname = str(data["AccountName"].strip())
            accountid = str(data["AccountID"].strip())
            accountplatform = str(data["AccountPlatform"].strip())
            thirdpartyplatformname = str(data["ThirdPartyPlatformName"].strip())
            medianame = str(data["MediaName"]).strip()

            if accountid:
                db.save_douyin_urls(strDate,id,accountname,accountid,accountplatform,thirdpartyplatformname,medianame)
            i += 1
    print(i)
#日志txt
def log_txt(message):
    with open("log_txt.txt","a",encoding="utf-8") as f:
        data = str(message) + "\n"
        f.write(data)

def log_error_txt(message):
    with open("log_error_txt.txt", "a", encoding="utf-8") as f:
        data = str(message) + "\n"
        f.write(data)
#上传抖音账户数据
def push_user_data(strDate):
    # date = datetime.datetime.now()
    # strDate = date.strftime("%Y-%m-%d")
    # strDate = "2019-10-08"
    id_count = db.get_douyin_count(strDate)
    # id的总数
    dataCount = id_count
    print("id数量:",dataCount)
    rows = db.get_user_data(strDate)
    rows_list = []
    for row in rows:
        rows_list.append(row)
    #userdata 数据总数
    userdata_count = len(rows_list)
    print("用户数据数量",userdata_count)
    data_list = []
    for i in rows_list:
        print(i)
        AccountName = i["douyin_unique_id"] if i['douyin_id'] == "0" else i['douyin_id']
        PlatformName = "抖音"
        TPAccountName = i["nickname"]
        TPAccountUrl = i["share_url"] if "share_url" in i.keys() else ""
        TPAccountFollowersCount = i["followers_count"] #粉丝数
        TPAccountPlayCount = -2
        TPAccountLikeCount = i["total_favorited"]
        TPAccountPostCount = i["aweme_count"]  #作品数
        TPAccountRepostCount = -2
        TPAccountCommentCount = -2
        LastUpdateTime = strDate
        AuthenticationInfo = i["verify"] #认证信息
        IntroductionInfo = (i["signature"]).replace('"','') #简介
        CreateTime = strDate
        RemarkInfo = ""
        DataPeriodID = "1"
        IsFailure = "0"
        ID = i["id"]
        TPAccountFavorite = i["like_count"] #喜欢数
        TPAccountFollowing = i["following_count"] #关注数
        TPAccountAction = i["dongtai_count"]
        dict_data = {
            "AccountName":AccountName,
            "PlatformName":PlatformName,
            "TPAccountName" : TPAccountName,
            "TPAccountUrl" :  TPAccountUrl,
            "TPAccountFollowersCount" : TPAccountFollowersCount,  # 粉丝数
            "TPAccountPlayCount" :  TPAccountPlayCount,
            "TPAccountLikeCount" : TPAccountLikeCount,
            "TPAccountPostCount" : TPAccountPostCount,  # 作品数
            "TPAccountRepostCount" :  TPAccountRepostCount,
            "TPAccountCommentCount" : TPAccountCommentCount,
            "LastUpdateTime" : LastUpdateTime,
            "AuthenticationInfo" : AuthenticationInfo,  # 认证信息
            "IntroductionInfo" : IntroductionInfo,  # 简介
            "CreateTime" :  CreateTime,
            "RemarkInfo" :   RemarkInfo,
            "DataPeriodID" :  DataPeriodID,
            "IsFailure" : IsFailure,
            "ID":ID,
            "TPAccountFavorite" : TPAccountFavorite,  # 喜欢数
            "TPAccountFollowing" :  TPAccountFollowing,  # 关注数
            "TPAccountAction" : TPAccountAction
        }
        if dict_data not in data_list:
            data_list.append(dict_data)




    print("去重后",len(data_list))
    #上传接口
    serverUrl = "http://218.241.201.165:30001/Logic/MetaDataFromWeb.ashx"
    exceptionCount = 0
    data_json = json.dumps({'userid': 19, 'datatype': 5, 'dataCount': dataCount,
                                                   'exceptionCount': exceptionCount,'data':data_list}, ensure_ascii=False)
    headers = {'Content-type': 'application/json'}

    try:
        response = requests.post(serverUrl, json=data_json, headers=headers)
        print("************************************************************")
        print(response)
        print(response.text)
        dictinfo = json.loads(response.text)
        if dictinfo and dictinfo.get('code') == 0:
           print('上传成功%d条抖音账号数据,其中全部记录%d条，采集记录%d条，异常账号记录%d条' % (userdata_count,dataCount, userdata_count, exceptionCount))
           date_data = reptile_t()
           message = date_data + '上传成功%d条抖音账号数据,其中全部记录%d条，采集记录%d条，异常账号记录%d条' % (userdata_count,dataCount, userdata_count, exceptionCount)
           message1 = date_data + str(response.text)
           log_txt(message)
           log_txt(message1)


        else:
            print('上传抖音账号数据失败:%s' % response.text)
            date_data = reptile_t()
            message = date_data + '上传抖音账号数据失败:%s' % response.text
            log_txt(message)


    except Exception as ex:
        print(ex)
        date_data = reptile_t()
        message = date_data + "抖音账号数据" + str(ex)
        log_error_txt(message)
#上传内容数据
def push_content_data(strDate):
    # date = datetime.datetime.now()
    # strDate = date.strftime("%Y-%m-%d")
    # strDate = "2019-10-08"
    content_count = db.get_content_count(strDate)
    # 作品的总数
    dataCount = content_count
    print("作品数量:", dataCount)
    rows = db.get_content_data(strDate)
    rows_list = []
    for row in rows:
        rows_list.append(row)
    # userdata 数据总数
    userdata_count = len(rows_list)
    print("作品数据数量", userdata_count)
    data_list = []
    for j,i in enumerate(rows_list):
        # print(i)
        ID = i["id"]
        if ID != 0:
            ArticleType = "视频"
            #做替换 a.replace('"','')
            i["desc"] = (i["desc"].replace("~", "")).replace('"','')
            Title = i["desc"]
            ReadNum = -2
            CommentNum = i["comment_count"]
            PlayNum = i["play_count"]
            LikeNum = i["digg_count"]
            ArticleCreateTime = i["create_time"]
            # 判断时间 发布时间是前一天的
            pattern = re.compile('(.*-.*-.*) ')
            yesterday_o = pattern.findall(ArticleCreateTime)[0]
            #只上传昨天的数据
            if yesterday_o == getDate(1):
                UpdateTime = strDate
                IsFailure = "0"
                RemarkInfo = ""
                ArticleText = ""
                ArticleUrl = i["share_url"]
                VoiceLength = i["duration"]
                Comments = ""
                ArticleID = i["aweme_id"]
                ShareNum = i["share_count"]
                DownLoadNum = i["download_count"]

                dict_data = {
                    "ID": ID,
                    "ArticleType": ArticleType,
                    "Title": Title,
                    "ReadNum":ReadNum,
                    "CommentNum": CommentNum,
                    "PlayNum": PlayNum,
                    "LikeNum": LikeNum,
                    "ArticleCreateTime": ArticleCreateTime,
                    "UpdateTime": UpdateTime,
                    "IsFailure":  IsFailure,
                    "RemarkInfo": RemarkInfo,
                    "ArticleText":  ArticleText,
                    "ArticleUrl": ArticleUrl,
                    "VoiceLength": VoiceLength,
                    "Comments": Comments,
                    "ArticleID": ArticleID,
                    "ShareNum": ShareNum,
                    "DownLoadNum":DownLoadNum
                 }
                print(dict_data)
                #存入每日视频的url
                video_url = dict_data["ArticleUrl"].strip("https://")
                db.save_video_url(dict_data["ID"],video_url,dict_data["ArticleCreateTime"],dict_data["ArticleID"],dict_data["UpdateTime"])
                data_list.append(dict_data)
                # if dict_data not in data_list:
                #     print(j, dict_data)
                #     data_list.append(dict_data)
    print(len(data_list))
    # 去重







    yesterday_count = len(data_list)
    print(yesterday_count)
    # 上传接口
    serverUrl = "http://218.241.201.165:30001/Logic/MetaDataFromWeb.ashx"
    exceptionCount = 0
    data_json = json.dumps({'userid': 19, 'datatype': 51, 'dataCount': dataCount,
                            'exceptionCount': exceptionCount, 'data': data_list}, ensure_ascii=False)
    write_json(data_json)
    headers = {'Content-type': 'application/json'}
    # print('上传成功%d条抖音作品数据,其中全部记录%d条，采集记录%d条，异常账号记录%d条' % (
    # dataCount,dataCount,dataCount,exceptionCount))

    try:
        response = requests.post(serverUrl, json=data_json, headers=headers)
        print(response)
        print(response.text)
        dictinfo = json.loads(response.text)
        if dictinfo and dictinfo.get('code') == 0:
            print('上传成功%d条抖音作品数据,其中全部记录%d条，采集记录%d条，异常账号记录%d条' % (
                yesterday_count, yesterday_count, yesterday_count, exceptionCount))
            date_data = reptile_t()
            message = date_data + '上传成功%d条抖音作品数据,其中全部记录%d条，采集记录%d条，异常账号记录%d条' % (
                yesterday_count, yesterday_count, yesterday_count, exceptionCount)
            message1 = date_data + str(response.text)
            log_txt(message)
            log_txt(message1)



        else:
            print('上传抖音作品数据失败:%s' % response.text)
            date_data = reptile_t()
            message = date_data + '上传抖音作品数据失败:%s' % response.text
            log_txt(message)


    except Exception as ex:
        print(ex)

        date_data = reptile_t()
        print(ex)
        message = date_data + "抖音内容数据" +str(ex)
        log_error_txt(message)




if __name__ == '__main__':

    while True:
        date = datetime.datetime.now()

        strDate = date.strftime("%Y-%m-%d")
        strtime = date.strftime("%Y-%m-%d %H:%M:%S")
        time.sleep(10)
        print(strtime + "正常循环")
        #00:07:30  "%H:%M:%S"
        if date.strftime("%H:%M") == "00:01":
            print("等待1分中")
            time.sleep(60)
            get_data()




        elif date.strftime("%H:%M") == "10:03": # %H:%M:%S
             # strDate = "2020-02-13"
            print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
            time.sleep(60)

            result = db.get_douyinid_down(strDate)
            time.sleep(60)
            if result > 600:
                print("***************************************")
                #将账户数据的数量写入                down_txt(str(result))

                print(result)

                rows = db.get_douyinid_notdown(strDate)
                list_rows = []
                for row in rows:
                    list_rows.append(row)
                print(len(list_rows))
                for i, row in enumerate(list_rows):
                    nickname = row["accountname"]
                    douyin_id = row["accountid"]
                    id = row["id"]
                    # reptile_time = reptile_t()
                    # reptile_date = reptile_d()
                    reptile_time = ""
                    reptile_date = strDate
                    print(row)
                # break

                #
                    message_one = id + " " + nickname + " " + douyin_id
                    down_error(message_one)
                    db.save_noexist_userData(id, nickname, douyin_id, "",  "",  "",
                                             -1,  -1,  -1,  -1,
                                             -1, -1, reptile_time, reptile_date,"")

                try:


                    try:
                        push_user_data(strDate)
                    except Exception as e:
                        push_user_data(strDate)
                    push_content_data(strDate)
                except Exception as e:
                    print(e)




























