import csv
import pandas as pd

# 拼接不同文件内的公会信息
def add_walk_data():
    rows = {}
    for i in range(1,5):
        with open('clan'+str(i)+'.csv', 'r', encoding="utf8") as f:
            reader = csv.reader(f)
            for row in reader:
                rows[int(row[1])] = ['"%s"'%row[0], row[1], '"%s"'%row[2], row[3], row[4], row[5], row[6], row[7]]
    with open('clan_full.csv','w', newline='', encoding="utf8") as csvfile:
        writer  = csv.writer(csvfile)
        for row in sorted(rows):
             writer.writerow(rows[row])

#按需求筛选clan_full文件内公会
def filter_clan(num: int):
    """
    根据输入的数字执行不同的指令
    1:筛选上次会战有排名的公会，并按排名顺序排列
    2:
    3:
    4:
    """
    filter_data = {}
    if num == 1:
        with open('clan_full.csv','r', encoding="utf8") as csvfile:
            lines = csv.reader(csvfile)
            for line in lines:
                if line[6] != 0:
                    filter_data[int(line[6])] = line
        savepath = 'clan_withrank.csv'
    with open(savepath,'w', newline='', encoding="utf8") as csvfile:
        writer  = csv.writer(csvfile)
        for row in sorted(filter_data):
             writer.writerow(filter_data[row])
    return 0


if __name__ == "__main__":
    filter_clan(1)