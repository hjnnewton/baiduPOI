#-*- coding:utf-8 -*-
import requests
import json
regions = open('region.txt')
searches = open('test.txt')
try:
    list_of_regions = []
    list_of_kw = []
    for line in regions.readlines():
        line = line.strip('\n')
        list_of_regions.append(line)
    for line in searches.readlines():
        line = line.strip('\n')
        list_of_kw.append(line)
    results = []
    resultFile = open('testRe.txt', 'w')
    try:
        for region in list_of_regions:
            print(region, list.index(list_of_regions, region))
            for search in list_of_kw:
                url = 'http://api.map.baidu.com/place/v2/suggestion?query=' + search + '&region=' + region + '&city_limit=true&output=json&ak=4zbsyOHMfdK5BDnhnkthr53Z'
                r = requests.get(url)
                jo = json.loads(r.text)
                for result in jo['result']:
                    if(list.index(jo['result'], result) == 0):
                        continue
                    name = result['name']
                    if(len(name) <= 6):
                        resultFile.write(name + "\n")
        #resultFile.writelines(results)
    finally:
        resultFile.close()
finally:
    regions.close()
    searches.close()
