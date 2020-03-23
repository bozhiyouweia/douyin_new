#coding =utf-8
import os
from pymongo import MongoClient

import re
# import trsData
import datetime

#获取当时时间
def get_date():
    date = datetime.datetime.now()
    strDate = date.strftime("%Y-%m-%d")
    return strDate

class douyin_mongo:

    # 日志函数
    # def WriteLog(self,message):
    #     fileName = os.path.join(os.getcwd(), "log.txt")
    #     message = "\n" + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "：" + message
    #     with open(fileName, 'a') as f:
    #         f.write(message)
    # def __init__(self, connstr='mongodb://127.0.0.1:27017/', mongodbName='douyin_%s'%(get_date())):
    #     client = MongoClient(connstr)
    #     self.db = client[mongodbName]
                                                    #douyin_2020-02-18 #douyin_2020-02-27   # 'douyin_2020-02-18' #douyin_0121-0220
    def __init__(self, connstr='mongodb://127.0.0.1:27017/', mongodbName='douyin_2020-02-end'):
        client = MongoClient(connstr)
        self.db = client[mongodbName]

    def save_douyin_urls(self,strDate,id,accountname,accountid,accountplatform,thirdpartyplatformname,medianame):
        #count = self.db.douyinid.find({'id': id, 'date': strDate,'accountid':accountid,"accountname":accountname,"medianame":medianame}).count()

        count = self.db.douyinid.find({ 'date': strDate,'accountid':accountid}).count()
        if count == 0:
            self.db.douyinid.insert({'id': id, 'date': strDate,'accountid':accountid,
            "accountname":accountname,"medianame":medianame,"accountplatform":accountplatform,"thirdpartyplatformname":thirdpartyplatformname,'isdown':0,'isget':0})
        else:
            with open("%s_chongfu.txt"%(get_date()),"a",encoding="utf-8") as f:
                data = "抖音id重复 %s"%(accountid) + "\n"
                f.write(data)
    #存入每天的vdeo_url
    def save_video_url(self,id,video_url,publish_time,video_id,reptile_time):
        count = self.db.video_url.find({'video_id': video_id, 'publish_time': publish_time}).count()
        if count == 0:
            self.db.video_url.insert({'id':id, 'video_url': video_url, 'publish_time': publish_time,
                                     "video_id": video_id, "reptile_time": reptile_time})


    #获取抖音原始数据的数量
    def get_douyin_count(self,strDate):
        id_count = self.db.douyinid.count({"date": strDate})
        return id_count
    #已经请求的数量
    def get_user_count(self):
        user_count = self.db.user_data.count({"isget": 1})
        return user_count

    #获取content数量
    def get_content_count(self,strDate):
        content_count = self.db.content_data.count({"reptile_date": strDate})
        return content_count




    #获取user库里的账号数据
    def get_user_data(self,strDate):
        where = {"reptile_date": strDate,"isdata":1}
        rows = self.db.user_data.find(where, {"id": 1, "nickname": 1, "douyin_id": 1, "douyin_unique_id": 1,
                         "verify": 1, "signature": 1, "total_favorited": 1,
                         "following_count": 1, "followers_count": 1,
                         "aweme_count": 1,
                         "dongtai_count": 1, "like_count": 1, "reptile_time": 1,
                         "reptile_date": 1,"isdata":1,"share_url":1})
        return rows

    def get_content_data(self,strDate):
        where = {"reptile_date": strDate}
        rows = self.db.content_data.find(where, {"id":1,"nickname":1,"desc":1,"aweme_id":1,"create_time":1,
                                              "signature":1,"comment_count":1,"digg_count":1,"share_url":1,
                                              "download_count":1,"play_count":1,"share_count":1,"duration":1,
                                              "reptile_time":1,"reptile_date":1})
        return rows



    #获取库里的抖音id   isget:0
    def get_douyin_id(self,strDate):
        where = {"isget":0,"date":strDate}
        rows = self.db.douyinid.find(where,{"accountid":1,"id":1})
        return rows


        # 获取库里的抖音id   isget:0
        # 已经请求的数量

    def get_douyinid_down(self,strDate):
        user_count = self.db.douyinid.count({"isdown": 1,"date":strDate})
        return user_count

    def get_douyinid_notdown(self, strDate):
        where = {"isdown": 0, "date": strDate}
        rows = self.db.douyinid.find(where, {"accountid": 1,"accountname":1, "id": 1,"_id":0})
        return rows

    #更新id 只要获取了就标识
    def updateid(self,douyin_id):
        mdict = {'isget': 1}

        self.db.douyinid.update({"accountid": douyin_id}, {"$set": mdict})




    def updateurl(self,nickname,douyin_id,douyin_unique_id,reptile_date):
        mdict = {'isdown': 1}
        count1 = self.db.douyinid.find({"accountid":douyin_id,"date":reptile_date}).count()
        count2 = self.db.douyinid.find({"accountid": douyin_unique_id,"date":reptile_date}).count()
        count3 = self.db.douyinid.find({"accountname": nickname,"date":reptile_date}).count()
        if count1:
            self.db.douyinid.update({"accountid":douyin_id,"date":reptile_date},{"$set":mdict})
        elif count2:
            self.db.douyinid.update({"accountid": douyin_unique_id,"date":reptile_date}, {"$set": mdict})
        elif count3:
            self.db.douyinid.update({"accountname": nickname,"date":reptile_date}, {"$set": mdict})
        # else:
        #     #当数据库的数据总数和链接总数一致时再推出
        #
        #     message = "%s 可能不是目标数据 抖音id 有误" % (nickname)
        #     message = "\n" + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "：" + message
        #     with open("error.txt", "a", encoding="utf-8") as f:
        #         data = message
        #         f.write(data)
        #






    def save_userData(self, nickname,douyin_id,douyin_unique_id,verify,signature,
                total_favorited,following_count,followers_count,aweme_count,dongtai_count,
                like_count,reptile_time,reptile_date,share_url):
        count = self.db.user_data.find({"nickname":nickname,"douyin_id":douyin_id,"douyin_unique_id":douyin_unique_id,"reptile_date":reptile_date}).count()
        if count == 0:


            # """
            #   where = {"isdown":0,"date":strDate}
            #   rows = self.db.douyinid.find(where,{"accountid":1,"id":1})
            #   return rows

    #         """
    #           rows_o = []
    # rows_t = []
    # for row in rows_one:
    #     rows_o.append(row)
    # for row in rows_two:
    #     rows_t.append(row)
    # if len(rows_o)>0:
    #     print("11")
    #     for row in rows_o:
    #         print(row)
    #     return 1
    # elif len(rows_t)>0:
    #     print("22")
    #     for row in rows_t:
    #         print(row)
    #     return 1


            # """
            # # """
            #技术
            where_one = {"accountid": douyin_id,"date":reptile_date}
            rows_one = self.db.douyinid.find(where_one,{"id": 1})
            where_two = {"accountid":douyin_unique_id,"date":reptile_date}
            rows_two = self.db.douyinid.find(where_two,{"id":1})
            where_three = {"accountname": nickname,"date":reptile_date}
            rows_three = self.db.douyinid.find(where_three, {"id": 1})
            rows_o = []
            rows_t = []
            rows_th = []
            for row in rows_one:
                rows_o.append(row)
            for row in rows_two:
                rows_t.append(row)
            for row in rows_three:
                rows_th.append(row)

            if len(rows_o) > 0:
                for row in rows_o:
                    id = row["id"]
                    self.db.user_data.insert(
                        {"id": id, "nickname": nickname, "douyin_id": douyin_id, "douyin_unique_id": douyin_unique_id,
                         "verify": verify, "signature": signature, "total_favorited": total_favorited,
                         "following_count": following_count, "followers_count": followers_count,
                         "aweme_count": aweme_count,
                         "dongtai_count": dongtai_count, "like_count": like_count, "reptile_time": reptile_time,
                         "reptile_date": reptile_date,"isdata":1,"share_url":share_url})
                return 1
            elif len(rows_t) > 0:
                for row in rows_t:
                    id = row["id"]
                    self.db.user_data.insert(
                        {"id": id, "nickname": nickname, "douyin_id": douyin_id, "douyin_unique_id": douyin_unique_id,
                         "verify": verify, "signature": signature, "total_favorited": total_favorited,
                         "following_count": following_count, "followers_count": followers_count,
                         "aweme_count": aweme_count,
                         "dongtai_count": dongtai_count, "like_count": like_count, "reptile_time": reptile_time,
                         "reptile_date": reptile_date,"isdata":1,"share_url":share_url})
                return 1



            elif len(rows_th) > 0:
                for row in rows_th:
                    id = row["id"]
                    self.db.user_data.insert(
                        {"id": id, "nickname": nickname, "douyin_id": douyin_id, "douyin_unique_id": douyin_unique_id,
                         "verify": verify, "signature": signature, "total_favorited": total_favorited,
                         "following_count": following_count, "followers_count": followers_count,
                         "aweme_count": aweme_count,
                         "dongtai_count": dongtai_count, "like_count": like_count, "reptile_time": reptile_time,
                         "reptile_date": reptile_date, "isdata": 1,"share_url":share_url})
                return 1
            else:
                self.db.user_data.insert(
                    {"id": 0, "nickname": nickname, "douyin_id": douyin_id, "douyin_unique_id": douyin_unique_id,
                     "verify": verify, "signature": signature, "total_favorited": total_favorited,
                     "following_count": following_count, "followers_count": followers_count,
                     "aweme_count": aweme_count,
                     "dongtai_count": dongtai_count, "like_count": like_count, "reptile_time": reptile_time,
                     "reptile_date": reptile_date, "isdata": 0,"share_url":share_url})

    def save_noexist_userData(self, id,nickname, douyin_id, douyin_unique_id, verify, signature,
                      total_favorited, following_count, followers_count, aweme_count, dongtai_count,
                      like_count, reptile_time, reptile_date,share_url):
        count = self.db.user_data.find(
            {"nickname": nickname, "douyin_id": douyin_id, "douyin_unique_id": douyin_unique_id,
             "reptile_date": reptile_date}).count()
        if count == 0:
            self.db.user_data.insert(
                {"id": id, "nickname": nickname, "douyin_id": douyin_id, "douyin_unique_id": douyin_unique_id,
                 "verify": verify, "signature": signature, "total_favorited": total_favorited,
                 "following_count": following_count, "followers_count": followers_count,
                 "aweme_count": aweme_count,
                 "dongtai_count": dongtai_count, "like_count": like_count, "reptile_time": reptile_time,
                 "reptile_date": reptile_date, "isdata": 1,"share_url":share_url})










    def sava_Content(self,nickname,desc,aweme_id,create_time,signature,comment_count,digg_count,
                  download_count,play_count,share_count,duration,share_url,reptile_time,reptile_date):#,short_id
        count = self.db.content_data.find(
            {"nickname": nickname, "aweme_id": aweme_id,"reptile_date": reptile_date}).count()
        if count == 0:
            where = {"accountname": nickname,"date":reptile_date}
            # where_one = {"accountid": short_id, "date": reptile_date}
            rows = self.db.douyinid.find(where,{"id": 1})
            # rows_one  = self.db.douyinid.find(where_one, {"id": 1})

            ro = []
            for o in rows:
                ro.append(o)

            # r_list = []
            # for r in rows_one:
            #     r_list.append(r)

            if len(ro):
                for row in ro:
                    id = row["id"]

                    self.db.content_data.insert({"id":id,"nickname":nickname,"desc":desc,"aweme_id":aweme_id,"create_time":create_time,
                                              "signature":signature,"comment_count":comment_count,"digg_count":digg_count,
                                              "download_count":download_count,"play_count":play_count,"share_count":share_count,"duration":duration,
                                              "share_url":share_url,"reptile_time":reptile_time,"reptile_date":reptile_date})

            # elif len(r_list):
            #     for row in r_list:
            #         id = row["id"]
            #
            #         self.db.content_data.insert(
            #             {"id": id, "nickname": nickname, "desc": desc, "aweme_id": aweme_id, "create_time": create_time,
            #              "signature": signature, "comment_count": comment_count, "digg_count": digg_count,
            #              "download_count": download_count, "play_count": play_count, "share_count": share_count,
            #              "duration": duration,
            #              "share_url": share_url, "reptile_time": reptile_time, "reptile_date": reptile_date})


            else:
                self.db.content_data.insert(
                    {"id": 0, "nickname": nickname, "desc": desc, "aweme_id": aweme_id, "create_time": create_time,
                     "signature": signature, "comment_count": comment_count, "digg_count": digg_count,
                     "download_count": download_count, "play_count": play_count, "share_count": share_count,
                     "duration": duration,
                     "share_url": share_url, "reptile_time": reptile_time, "reptile_date": reptile_date}
                )



    def sava_video_Content(self, nickname, desc, aweme_id, create_time, signature, comment_count, digg_count,
                     download_count, play_count, share_count, duration, share_url, reptile_time, reptile_date):
        count = self.db.video_content_data.find(
            {"nickname": nickname, "aweme_id": aweme_id, "reptile_date": reptile_date}).count()
        if count == 0:
            where = {"accountname": nickname, "date": reptile_date}
            rows = self.db.douyinid.find(where, {"id": 1})
            if rows:
                for row in rows:
                    id = row["id"]

                    self.db.video_content_data.insert(
                        {"id": id, "nickname": nickname, "desc": desc, "aweme_id": aweme_id, "create_time": create_time,
                         "signature": signature, "comment_count": comment_count, "digg_count": digg_count,
                         "download_count": download_count, "play_count": play_count, "share_count": share_count,
                         "duration": duration,
                         "share_url": share_url, "reptile_time": reptile_time, "reptile_date": reptile_date}
                        )

    def sava_video_seven_Content(self, nickname, desc, aweme_id, create_time, signature, comment_count, digg_count,
                     download_count, play_count, share_count, duration, share_url, reptile_time, reptile_date):
        count = self.db.detail_data.find(
            {"nickname": nickname, "aweme_id": aweme_id, "reptile_date": reptile_date}).count()
        if count == 0:
            where = {"accountname": nickname, "date": reptile_date}
            rows = self.db.douyinid.find(where, {"id": 1})
            if rows:
                for row in rows:
                    id = row["id"]

                    self.db.detail_data.insert(
                        {"id": id, "nickname": nickname, "desc": desc, "aweme_id": aweme_id, "create_time": create_time,
                         "signature": signature, "comment_count": comment_count, "digg_count": digg_count,
                         "download_count": download_count, "play_count": play_count, "share_count": share_count,
                         "duration": duration,
                         "share_url": share_url, "reptile_time": reptile_time, "reptile_date": reptile_date}
                        )





    def getDate(self,beforeOfDay):
        today = datetime.datetime.now()
        # 计算偏移量
        offset = datetime.timedelta(days=-beforeOfDay)
        # 获取想要的日期的时间
        re_date = (today + offset).strftime('%Y-%m-%d')  # %Y-%m-%d %H:%M:%S

        return re_date

    def get_qimai_Urls(self, strDate, iosOrAndroid):
        where = {'isdown': 0, "date": strDate}
        if iosOrAndroid:
            where["iosOrAndroid"] = iosOrAndroid

        rows = self.db.qimaiurl08.find(where,
                                       {'_id': 0, 'category': 1, 'evalue_object': 1, 'id': 1, "netname": 1, "neturl": 1,
                                        'iosOrAndroid': 1, 'IsFailure': 1, 'RemarkInfo': 1})
        return rows


    def getAndroidData(self,strDate):
        rows = self.db.android08.find({"date": strDate},{'_id':0,'id': 1, 'netname': 1, 'link':1,'app_market': 1,
                                     'add_down_count': 1, 'total_down_count': 1,'ModifiedName':1,'IsFailure':1,'RemarkInfoInfo':1})
        return rows

    def getIOSData(self,strDate):
        rows = self.db.ios08.find({"date": strDate}, {'_id': 0, 'id': 1, 'netname': 1, 'link': 1,
                                                        'total_down_count': 1,  'ModifiedName': 1,'IsFailure':1,'RemarkInfo':1
                                                    })
        return rows

















