# -*- coding:utf-8 -*-
import json
import sys
import time
import requests
# Collect all possible places in china using BAIDU API


class BaiDuPOI(object):
    def __init__(self, itemy, loc):
        self.itemy = itemy
        self.loc = loc


    def baidu_search(self):
        api_key = baidu_api
        json_sel = []
        # 避免服务器连接次数过多过频而导致连接中断
        r = ''
        while r == '':
            try:
                r = requests.get('http://api.map.baidu.com/place/v2/search?query=' + self.itemy + '&bounds=' + self.loc +
                                '&page_size=20&page_num=0' + '&output=json&ak=' + api_key)
            except:
                print("Connection refused by the server..")
                print("Let me sleep for 5 seconds")
                print("ZZzzzz...")
                time.sleep(5)
                print("Was a nice sleep, now let me continue...")
                continue
        data = json.loads(r.text)
        # 解析Json结果，对可能的空键值条件
        if(data.get('total')):
            total = data["total"]
            for pages in range(0, int(total/20)+1):
                r = requests.get('http://api.map.baidu.com/place/v2/search?query=' + self.itemy + '&bounds=' + self.loc + \
                      '&page_size=20&page_num=' + str(pages) + '&output=json&ak=' + api_key)
                data = json.loads(r.text)
                if(data.get('results')):
                    for item in data['results']:
                        jname = item["name"].replace(',', '')
                        jlat = ''
                        jlng = ''
                        jadd = ''
                        if(item.get('location')):
                            jlat = item["location"]["lat"]
                            jlng = item["location"]["lng"]
                        if(item.get('address')):
                            jadd = item["address"].replace(',', '')
                        js_sel = jname + ',' + jadd + ',' + str(jlat) + ',' + str(jlng)
                        json_sel.append(js_sel)
        return json_sel


class LocaDiv(object):
    def __init__(self, loc_all):
        self.loc_all = loc_all

    # 定义函数，以0.05度为间隔，对纬度进行划分，返回一个列表
    def lat_all(self):
        lat_sw = float(self.loc_all.split(',')[0])
        lat_ne = float(self.loc_all.split(',')[2])
        lat_list = []
        for i in range(0, int((lat_ne - lat_sw + 0.0001) / 0.05)):
            lat_list.append(lat_sw + 0.05 * i)
        lat_list.append(lat_ne)
        return lat_list

    # 定义函数，以0.05度为间隔，对经度进行划分，返回一个列表
    def lng_all(self):
        lng_sw = float(self.loc_all.split(',')[1])
        lng_ne = float(self.loc_all.split(',')[3])
        lng_list = []
        for i in range(0, int((lng_ne - lng_sw + 0.0001) / 0.05)):
            lng_list.append(lng_sw + 0.05 * i)
        lng_list.append(lng_ne)
        return lng_list

    # 定义函数，将经纬度进行组合，返回一个列表
    def ls_com(self):
        l1 = self.lat_all()
        l2 = self.lng_all()
        ab_list = []
        for i in range(0, len(l1)):
            a = str(l1[i])
            for i2 in range(0, len(l2)):
                b = str(l2[i2])
                ab = a + ',' + b
                ab_list.append(ab)
        return ab_list

    # 定义函数，将对角线坐标进行组合，返回一个列表
    def ls_row(self):
        l1 = self.lat_all()
        l2 = self.lng_all()
        ls_com_v = self.ls_com()
        print(len(l1), len(l2))
        ls = []
        for n in range(0, len(l1) - 1):
            for i in range(0 + len(l2) * n, len(l2) + (len(l2)) * n - 1):
                a = ls_com_v[i]
                b = ls_com_v[i + len(l2) + 1]
                ab = a + ',' + b
                ls.append(ab)
        return ls


if __name__ == '__main__':
    baidu_api = '4zbsyOHMfdK5BDnhnkthr53Z'  # 这里填入你的百度API
    print("开始爬数据，请稍等...")
    start_time = time.time()
    loc = LocaDiv('23.5,100,45,120')
    # 120.552244,31.261114    120.760938,31.385985
    locs_to_use = loc.ls_row()
    tags = open('poitags.txt')
    list_of_tags = []
    for line in tags.readlines():
        line = line.strip('\n')
        list_of_tags.append(line)
    for loc_to_use in locs_to_use[5000:]:
        i = list.index(locs_to_use, loc_to_use)
        if i %1000 == 0:
            file_name = 'data/baidu_poi'+ str(int(i/1000)) + '.csv'
        print(str((list.index(locs_to_use, loc_to_use)+1)) + "of" +str(len(locs_to_use)) + "completed")
        print(loc_to_use + 'processing')
        for tag in list_of_tags:
            par = BaiDuPOI(str(tag), loc_to_use)  # 请修改这里的参数
            a = par.baidu_search()
            doc = open(file_name , 'a')
            for ax in a:
                print(ax)
                doc.write(ax)
                doc.write('\n')
            doc.close()
    end_time = time.time()
    print("数据爬取完毕，用时%.2f秒" % (end_time - start_time))