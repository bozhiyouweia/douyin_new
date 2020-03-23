# 数据到导出
#coding:utf-8
import os
import xlrd
import xlwt
import re
import douyin_mongo
db = douyin_mongo.douyin_mongo()
exportExcelPath = r"E:\pc_project\douyin_new"

def WriteSheetRow(sheet, rowValueList, rowIndex, isBold):
    i = 0
    style = xlwt.easyxf('font: bold 1')
    # style = xlwt.easyxf('font: bold 0, color red;')#红色字体
    style2 = xlwt.easyxf('pattern: pattern solid, fore_colour yellow; font: bold on;')  # 设置Excel单元格的背景色为黄色，字体为粗体
    for svalue in rowValueList:
        if isBold:
            sheet.write(rowIndex, i, svalue, style2)
        else:
            sheet.write(rowIndex, i, svalue)
        i = i + 1
def export(exportExcelPath):
    fileName = "抖音账号补采数据" + ".xls"
    fileName = os.path.join(exportExcelPath, fileName)
    result = False
    dict_id = {"央视国家记忆": "guojiajiyi", "CCTV4": "902971025", "CCTV中华医药": "1980133383", "CCTV中国缘": "cctvwgrzzg", "CCTV4《记住乡愁》": "cctvjzxc", "央视一套": "helloCCTV1", "央视新闻": "cctvnews", "央视社会与法": "1115087566", "警察特训营": "876728104", "CCTV法律讲堂": "cctv12fljt", "CCTV-12方方圆圆": "CCTV12_666", "CCTV热线12": "1058272902", "CCTV热话": "1838202415", "CCTV12融屏剧阵": "1535538212", "法讲生活": "cctvfljtlife", "道道侠": "1714686323", "央视夜线": "CCTV_YEXIAN"}

    if not os.path.exists(fileName):

        android_headList = ['title', 'video_id', 'publish_time','user_name','comment_count','download_count','like_count','share_count','video_duration','share_url','reptile_time']

        android_row_list = []
        strDate = "2020-02-27"
        rows = db.get_content_data(strDate)
        num_list_one = ["01", "02", "03","04"]
        num_list_two = ["01","02","03","04","05"]
        # data_dict = {
        #     "nickname": nickname,
        #     "desc": desc,
        #     "aweme_id": aweme_id,
        #     "create_time": create_time,
        #     "signature": signature,
        #     "comment_count": comment_count,
        #     "digg_count": digg_count,
        #     "download_count": download_count,
        #     "play_count": play_count,
        #     "share_count": share_count,
        #     "duration": duration,
        #     "reptile_time": reptile_time,
        #     "reptile_date": reptile_date
        # }
        for r in rows:

            col_list = []

            ab = r["create_time"]
            nm = re.compile('(.*)-(.*)-(.*) .*')
            num = nm.findall(ab)[0]
            print(num[0])
            print(num[1])
            print(num[2])

            # if num[0] == "2019" and num[1] == "11":
            #     if (num[2]) in num_list:

            if num[0] ==  "2020":
                if num[1] == "01" and int(num[2]) > 19:
                    col_list.append(r["desc"])
                    col_list.append(r["aweme_id"])
                    col_list.append(r["create_time"])
                    col_list.append(r["nickname"])





                    # col_list.append(strDate)'video_duration','share_url','tag','platform','reptile_time

                    col_list.append(r["comment_count"])
                    col_list.append(r["download_count"])
                    col_list.append(r["digg_count"])

                    col_list.append(r["share_count"])

                    col_list.append(r["duration"])
                    col_list.append(r["share_url"])
                    col_list.append(r["reptile_time"])



                    android_row_list.append(col_list)
                elif num[1] == "02" and int(num[2]) < 21:
                    col_list.append(r["desc"])
                    col_list.append(r["aweme_id"])
                    col_list.append(r["create_time"])
                    col_list.append(r["nickname"])

                    # col_list.append(strDate)'video_duration','share_url','tag','platform','reptile_time

                    col_list.append(r["comment_count"])
                    col_list.append(r["download_count"])
                    col_list.append(r["digg_count"])

                    col_list.append(r["share_count"])

                    col_list.append(r["duration"])
                    col_list.append(r["share_url"])
                    col_list.append(r["reptile_time"])



                    android_row_list.append(col_list)
        print(len(android_row_list))

        wbk = xlwt.Workbook()
        sheet1 = wbk.add_sheet('抖音数据', cell_overwrite_ok=True)

        rowIndex = 0
        WriteSheetRow(sheet1, android_headList, rowIndex, True)
        for lst in android_row_list:
            rowIndex += 1
            WriteSheetRow(sheet1, lst, rowIndex, False)
        wbk.save(fileName)
        result = True
        # return result

def export_user(exportExcelPath):
    fileName = "抖音账号补采账号数据" + ".xls"
    fileName = os.path.join(exportExcelPath, fileName)
    result = False
    dict_id = {"央视国家记忆": "guojiajiyi", "CCTV4": "902971025", "CCTV中华医药": "1980133383", "CCTV中国缘": "cctvwgrzzg", "CCTV4《记住乡愁》": "cctvjzxc", "央视一套": "helloCCTV1", "央视新闻": "cctvnews", "央视社会与法": "1115087566", "警察特训营": "876728104", "法律讲堂": "cctv12fljt", "CCTV-12方方圆圆": "CCTV12_666", "CCTV热线12": "1058272902", "CCTV热话": "1838202415", "CCTV12融屏剧阵": "1535538212", "法讲生活": "cctvfljtlife", "道道侠": "1714686323", "央视夜线": "CCTV_YEXIAN"}

    if not os.path.exists(fileName):
        """
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
        """

        android_headList = ['账号名称','认证', '简介','获赞数','关注数', '粉丝数', '作品数','喜欢数','爬取时间']

        android_row_list = []
        strDate = "2020-02-27"
        rows = db.get_user_data(strDate)
        # with open(r"E:\pc_project\douyin_guanjian_bu\guanjian_bu.txt","r",encoding="utf-8") as f:
        #     reads = f.readlines()
        for r in rows:
            # r = eval(i)





            col_list = []
        # ArticleCreateTime = r["create_time"]
        # pattern = re.compile('.*-(.*)-.* ')
        # yesterday_o = pattern.findall(ArticleCreateTime)[0]
        # print(yesterday_o)
        # if yesterday_o in ["07", "08", "09"]:
        #     print("来了", r)

            col_list.append(r["nickname"])
            #col_list.append(dict_id[r["nickname"]])
            col_list.append(r["verify"])
            col_list.append(r["signature"])

            # col_list.append(strDate)

            col_list.append(r["total_favorited"])
            col_list.append(r["following_count"])
            col_list.append(r["followers_count"])
            col_list.append(r["aweme_count"])

            col_list.append(r["like_count"])
            col_list.append(r["reptile_time"])


            android_row_list.append(col_list)
        print(len(android_row_list))

        wbk = xlwt.Workbook()
        sheet1 = wbk.add_sheet('抖音账号数据', cell_overwrite_ok=True)

        rowIndex = 0
        WriteSheetRow(sheet1, android_headList, rowIndex, True)
        for lst in android_row_list:
            rowIndex += 1
            WriteSheetRow(sheet1, lst, rowIndex, False)
        wbk.save(fileName)
        result = True
        return result
#生成作品数据excel
export(exportExcelPath)

#生成账号数据excel
# export_user(exportExcelPath)

