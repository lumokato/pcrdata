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
    2:筛选前500的公会中，人数超过15人的公会
    3:筛选前500未满员且任何人都可以加入的公会
    """
    filter_data = {}
    if num == 1:
        with open('clan_full.csv','r', encoding="utf8") as csvfile:
            lines = csv.reader(csvfile)
            for line in lines:
                if line[6] != '0':
                    filter_data[int(line[6])] = line
        savepath = 'clan_withrank.csv'
    elif num == 2:
        with open('clan_withrank.csv','r', encoding="utf8") as csvfile:
            lines = csv.reader(csvfile)
            for line in lines:
                if int(line[4]) > 14:
                    filter_data[int(line[6])] = line
        savepath = 'clan_top.csv'
    elif num == 3:
        with open('clan_top.csv','r', encoding="utf8") as csvfile:
            lines = csv.reader(csvfile)
            for line in lines:
                if int(line[3]) == 1 and int(line[4]) < 30:
                    filter_data[int(line[6])] = line
        savepath = 'clan_in.csv'
    with open(savepath,'w', newline='', encoding="utf8") as csvfile:
        writer  = csv.writer(csvfile)
        for row in sorted(filter_data):
             writer.writerow(filter_data[row])

#筛选top300中的新公会
def filter_top():
    clans_new = []
    clans = []
    with open('clan_top300.csv','r', encoding="utf8") as csvfile:
        lines = csv.reader(csvfile)
        for line in lines:
            clans_new.append(line[0])
    with open('clan_top.csv','r', encoding="utf8") as csvfile:
        lines = csv.reader(csvfile)
        for line in lines:
            clans.append(line[0])
    for clan in clans_new:
        if clan not in clans:
            with open("newclan.bak",'a', encoding="utf8") as f:
                f.write(clan + '\n')
                f.close()

#将top300的公会对应id写入新文件
def writein_top():
    dic = {}
    with open('clan_top.csv','r', encoding="utf8") as csvfile:
        lines = csv.reader(csvfile)
        for line in lines:
            dic[line[0]] = line[1]
    with open('clan_top300.csv','r', encoding="utf8") as csvfile:
        lines = csv.reader(csvfile)
        for line in lines:
            if line[0] in dic.keys():
                with open("clanid.csv",'a', encoding="utf8") as f:
                    f.write(line[0] + "," + dic[line[0]] + "\n")

if __name__ == "__main__":
    #filter_clan(3)
    writein_top()