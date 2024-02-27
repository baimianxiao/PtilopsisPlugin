# -*- encoding:utf-8 -*-
from GuDice import Plugin

from PtilopsisPlugin.sql import UserDataHandle, BlacklistHandle
from PtilopsisPlugin.util import get_json, write_json

import math
import time
import random
from os import getcwd
from os.path import join

main_dir = getcwd()  # 取根目录
data_dir = join(main_dir, "data", "PtilopsisPlugin")  # 数据路径
user_sqlite_path = join(data_dir, "user_data.db")  # 用户数据库路径
message_data = get_json(join(data_dir, "reply.json"))  # 自定义回复配置文件


# 插件实现
class PluginEvent(Plugin):
    def __init__(self):
        super().__init__()
        self.sql = None

    def init(self):
        self.sql = UserDataHandle(user_sqlite_path)

    def group_message(self, data, bot):
        if data.message == "签到" or data.message.startswith("/签到"):
            everyday_sign(data, bot, self.sql)
        elif (data.message == ".r" or data.message.startswith(".r")
              or data.message == "。r" or data.message.startswith("。r")
              or data.message == "/r" or data.message.startswith("/r")):
            everyday_sign(data, bot, self.sql)
        # elif (data.message == "方舟十连" or data.message == "寻访十次"
        #   or data.message == "寻访十连" or data.message.startswith("方舟十连")):
        # arknights_draw(data, bot)
        elif data.message == ".test" or data.message.startswith(".test"):
            bot.reply(
                f"————————————\n▼ ERROR!\n│ 未查询到用户资料 \n┣———————————\n▲ 请使用签到指令初始化!\n————————————")
        else:
            reply_message(data, bot)

    def private_message(self, data, bot):
        pass

    def group_poke(self, data, bot):
        bot.send_group_msg(data.group_id, random.choice(message_data['戳']))


def reply_message(data, bot):
    if data.message in message_data.keys():
        reply_message_data = message_data[data.message]
        reply_message_data = random.choice(reply_message_data)
        bot.reply(reply_message_data)


sign_version = "v2.1.0"


# 每日签到
def everyday_sign(data, bot, sql):
    user_id = data.user_id
    user_nick = data.user_nick
    user_data = sql.user_data_select(user_id)
    if user_data is None:
        sql.user_data_insert(user_nick, user_id, 1, 0, 12000, time.strftime("%Y-%m-%d", time.localtime()))
        bot.reply(
            f"————————————\n▼ 初始化成功！\n│ successfully!\n┣———————————\n▲ 获得初始合成玉：12000\n————————————")
        return True
    user_name = user_data[0][1]
    user_ex = user_data[0][3]
    user_hcy = user_data[0][5]
    user_time = user_data[0][6]
    if user_time == time.strftime("%Y-%m-%d", time.localtime()):
        bot.reply("今天已经签到了")
        return True
    hcy_add = random.randint(10, 24) * 100
    ex_add = random.randint(1, 20) * 10

    user_ex = int(user_ex) + int(ex_add)
    user_hcy = int(user_hcy) + int(hcy_add)
    level = math.floor(user_ex / 2000)
    sql.user_data_update(user_id, user_ex, level, user_hcy, time.strftime("%Y-%m-%d", time.localtime()))
    bot.reply(
        f"————————————\n▼ 签到成功！\n│ Sign in successfully!\n┣———————————\n│ Dr.{user_name}\n│ 获得合成玉：{hcy_add}"
        f"\n▲ 现有合成玉：{user_hcy}\n————————————")
    return True


def arknights_draw(data, bot, sql):
    user_id = data.user_id
    user_data = sql.user_data_select(user_id)
    if user_data is None:
        bot.reply(
            f"————————————\n▼ ERROR!\n│ 未查询到用户资料 \n┣———————————\n▲ 请使用签到指令初始化!\n————————————")
        return True
    user_ex = user_data[0][3]
    user_hcy = user_data[0][5]
    user_time = user_data[0][6]
    level = math.floor(user_ex / 2000)
    if user_hcy < 6000:
        bot.reply(f"————————————\n▼ ERROR!\n│ 合成玉不足 \n┣———————————\n▲ 现有合成玉：{user_hcy}\n————————————")
        return True
    hcy = 6000
    user_hcy = int(user_hcy) - int(hcy)
    sql.user_data_update(user_id, user_ex, level, user_hcy, user_time)
    bot.reply(
        f"[CQ:image,file=http://127.0.0.1:11451]")
    return True


def sign_ordering(data, bot, sql):
    hcy_list = sql.user_data_ordering()
    for i in range(10):
        print(i)
    reply = (f"1.{hcy_list[0][1]}{hcy_list[0][5]}\n2.{hcy_list[1][1]} "
             f"{hcy_list[1][5]}\n3.{hcy_list[2][1]} {hcy_list[2][5]}\n")
    bot.reply(reply)


# 更改用户名
def change_user_name(data, bot, sql):
    user_name = plugin_event.data.message.strip("/更改用户名").strip()
    if user_name != "":
        user_id = plugin_event.data.user_id
        user_data = sql.user_data_select(user_id)
        user_ex = user_data[0][3]
        user_hcy = user_data[0][5]
        user_time = user_data[0][6]
        level = math.floor(user_ex / 2000)
        sql.user_data_update(user_id, user_ex, level, user_hcy, user_time, user_name)
        plugin_event.reply("用户名已修改为" + user_name)
    else:
        plugin_event.reply("用户名不能为空！")
