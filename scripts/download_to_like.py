# download_to_like.py created by AkirTech（Akir_@Github） on 2024/08/01
# MIT Licensed
# This is used to turn your download list to a like list.
# 这个脚本用于将下载列表转换成一个“收藏”列表，以方便桌面版和手机版的同步。

import sqlite3 as sql
import os
import getpass
import json
import time
import colorama as co

def main(amount:int):
    usr = getpass.getuser()
    
    list_name = str(time.time_ns())[0:13]

    path = os.path.join(f"C:\\Users\\{usr}")
    path = os.path.join(path,"AppData\\Roaming\\lx-music-desktop\\LxDatas\\lx.data.db")

    # 以上几行用于定义工作列表，获取用户的lx music的本地数据库路径（鬼知道这三句为什么写一起要报错）
    conn = sql.connect(path)
    cur = conn.cursor()
    cur.execute("SELECT position FROM 'my_list' ORDER BY position DESC")
    now_pos:int = max(cur.fetchall()[0])
    new_pos = now_pos+1
    # 此处：看看现在用户有多少个列表，在此基础上加1
    print(new_pos)
    # Insert new working list
    # 向 my_list 表中注册我们的新表
    cur.execute("INSERT INTO my_list VALUES ('{}','{}',NULL,NULL,{},NULL)".format(f"userlist_{list_name}",f"Result_{list_name}",new_pos))
    conn.commit() # 不要忘记 commit
    for i in range(amount):
        try:
            # Get id name singer source interval
            # 处理获取来的数据
            cur.execute("SELECT musicInfo,filePath FROM download_list WHERE position = '{}'".format(i))
            data=cur.fetchall()[0]
            filePath=data[1]
            music_info = data[0]
            dic = json.loads(music_info)
            music_id = dic["id"]
            file_extension = os.path.splitext(filePath)[1]
            dic['meta']["ext"]=file_extension
            dic['meta']["filePath"]=filePath
            music_name = str(dic["name"].replace("'","''"))
            meta_info = json.dumps(dic["meta"])
            music_singer = dic["singer"]
            # music_source = dic["source"]
            music_source = 'local'
            music_interval = dic["interval"]

            # Insert into new my_list_music_info_order table
            # 向 my_list_music_info_order ， my_list_music_info 迁移刚刚从下载表获取的数据
            cur.execute(f"INSERT INTO my_list_music_info VALUES ('{music_id}','userlist_{list_name}','{music_name}','{music_singer}','{music_source}','{music_interval}','{meta_info}')")
            conn.commit()
            cur.execute(f"INSERT INTO my_list_music_info_order VALUES ('userlist_{list_name}','{music_id}','{i}')")
            conn.commit()
            print(f"Added {i} {music_name} to list")
        except:
            print(f"Failed to add {i}")
            pass
          # 结算CG
    print(co.Fore.CYAN+"Done"+co.Fore.RESET)
  
# 亲切问候用户
print(co.Fore.YELLOW+"This script will add the songs in download list to a new list in LX Music"+co.Fore.RESET)
print(co.Fore.YELLOW+"After done , check the list tab in LX Music and see the newly created list."+co.Fore.RESET)

# 控制台主循环
while True:

    amount = input(co.Fore.RED+"Enter amount: "+co.Fore.RESET)
    try:
        main(int(amount))
        print(co.Fore.BLUE+"If you want to do it again,enter the amount again below"+co.Fore.RESET)
    except Exception as e:
        print(co.Fore.RED+e+co.Fore.RESET)
