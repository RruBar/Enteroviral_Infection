import json
import urllib.request as httplib
import os,sys
import pandas as pd
import matplotlib.pyplot as plt


"""將會印出作業系統名稱，並解決matplotlib的中文字和負號(-)問題"""
if sys.platform.startswith("linux"):  # could be "linux", "linux2", "linux3", ...
    print("linux")              # linux
elif sys.platform == "darwin":  # MAC OS X
    print("MAC OS")
    plt.rcParams['font.sans-serif'] = 'Arial Unicode MS'
    # //注意這裡用的不是'SimHei'
    plt.rcParams['axes.unicode_minus'] = False
elif sys.platform == "win32":   # Windows (either 32-bit or 64-bit)
    plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']
    plt.rcParams['axes.unicode_minus'] = False  # 步驟二（解決座標軸負數的負號顯示問題）

if not os.path.exists("急診傳染病監測統計-腸病毒.json"):
    URL="https://od.cdc.gov.tw/eic/RODS_EnteroviralInfection.json"
    header={
         'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36"
    }
    req = httplib.Request(url=URL,data=None,
                               headers=header)
    response=httplib.urlopen(req)
    if response.code==200:
        contents=response.read()
        contents=contents.decode("utf-8")
    with open("急診傳染病監測統計-腸病毒.json", mode="w+", encoding="utf-8") as file:
        file.write(contents)
else:
    with open("急診傳染病監測統計-腸病毒.json", mode="r+", encoding="utf-8") as file:
        contents=file.read()

data=json.loads(contents)
year = ['2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014',
        '2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022']
week = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13',
        '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26',
        '27', '28', '29', '30', '31', '32', '33', '34', '35', '36', '37', '38', '39',
        '40', '41', '42', '43', '44', '45', '46', '47', '48', '49', '50', '51', '52','53']

data_filter_by_year_week_case_numbers = {}
for i in year:
    data_filter_by_year_week_case_numbers[i]={}
    for j in week:
        if j not in data_filter_by_year_week_case_numbers[i]:
            data_filter_by_year_week_case_numbers[i][j] = 0
for case in data:
    data_filter_by_year_week_case_numbers[case['年']][case['週']] += int(case['腸病毒急診就診人次'])

data_filter_by_year_week_case_numbers_2007to2014={
    i: j for (i, j) in data_filter_by_year_week_case_numbers.items() if int(i)<2015
}
data_filter_by_year_week_case_numbers_2015to2022={
    i: j for (i, j) in data_filter_by_year_week_case_numbers.items() if int(i)>2014
}
color_label = ['bo-', 'go-', 'ro-', 'co-',
               'mo-', 'yo-', 'ko-', 'b*-']
color_count = 0

plot1=plt.subplot(2,1,1)
for single_year in data_filter_by_year_week_case_numbers_2007to2014.items():
    # print(single_year)
    # ('2022', {'01': 23, '02': 37, '03': 28, '04': 27,
    week_data = list(single_year[1].items())
    # print(list(week_data))
    x=[]
    y=[]
    for i in range(len(week_data)):
        x.append(i+1)
        y.append(week_data[i][1])
    plt.plot(x, y,color_label[color_count],label=single_year[0])
    color_count += 1
plt.title("2007至2014腸病毒急診就診人次(各週為單位)")
plt.xlabel("週")
plt.ylabel("就診人次")
# ax = plt.axes()
# ax.set_facecolor("grey")
plt.legend()

color_count=0
plot1=plt.subplot(2,1,2)
for single_year in data_filter_by_year_week_case_numbers_2015to2022.items():
    week_data = list(single_year[1].items())
    # print(list(week_data))
    x=[]
    y=[]
    for i in range(len(week_data)):
        x.append(i+1)
        y.append(week_data[i][1])
    plt.plot(x, y,color_label[color_count],label=single_year[0])
    color_count += 1
plt.ylim(0,2500)
plt.xlabel("週")
plt.ylabel("就診人次")
plt.title("2015至2022腸病毒急診就診人次(各週為單位)")
plt.legend()

plt.tight_layout()
plt.show()


# print(data_filter_by_year_week_case_numbers)

# for i in data:
#     new_data={
#             '週' : i["週"],
#             '縣市' : i["縣市"],
#             '年齡別' : i["年齡別"],
#             '腸病毒急診就診人次' : i["腸病毒急診就診人次"]
#         }
#     data_filter_by_year_week_case_numbers[i['年']].append(new_data)
#
# data2007=data_filter_by_year['2007']
# data2007.sort()
# print(len(data2007))
"""
demo
{"2007": [  {"週": "35", "縣市": "嘉義市", "年齡別": "4-6", "腸病毒急診就診人次": "2"},
            {"週": "05", "縣市": "桃園市", "年齡別": "0", "腸病毒急診就診人次": "1"},
            {"週": "05", "縣市": "台北市", "年齡別": "4-6", "腸病毒急診就診人次": "2"},
            {"週": "22", "縣市": "彰化縣", "年齡別": "0", "腸病毒急診就診人次": "10"},
"""


# for i in data2007:
#     if i['週'] not in week_2007:
#         week_2007.append(i['週'])
#     week_2007.sort()


# # 將整理黨檔案寫入json
# with open("急診傳染病監測統計-腸病毒_data_filter_by_year.json",mode="w",encoding="utf-8") as jsonfile:
#     json.dump(data_filter_by_year, jsonfile, ensure_ascii=False)



# print(data_filter_by_year)
