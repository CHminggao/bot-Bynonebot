'''
Author: GM
Date: 2021-11-23 20:22:45
LastEditors: GM
LastEditTime: 2021-12-08 11:48:39
Description: file content
'''
# import nonebot
from nonebot import get_driver
import sqlite3
from .config import Config
from nonebot import on_command
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
from .data_source import data_source
from nonebot.permission import SUPERUSER

global_config = get_driver().config
config = Config(**global_config.dict())

tiangou=on_command("舔狗日记")
@tiangou.handle()
async def tiangou_command(bot: Bot, event: Event, state: T_State):
    args = str(event.get_message()).strip()  # 首次发送命令时跟随的参数，例：/天气 上海，则args为上海
    if args=="":
        content= await data_source.selectContent(config.db_file)
        await tiangou.finish(content)


tiangou_add=on_command("日记", permission=SUPERUSER)
@tiangou_add.handle()
async def tiangouadd_command(bot: Bot, event: Event, state: T_State):
    args = str(event.get_message()).strip()  # 首次发送命令时跟随的参数，例：/天气 上海，则args为上海
    if args:
        if args=="初始化":
            await data_source.create_table(config.db_file)
            await tiangou.finish("已初始化完成")
        elif args.split(' ')[0]=="新增":
            await data_source.insertContent(config.db_file,args.lstrip("新增 "))
            await tiangou.finish("已新增完成")
        elif args.split(' ')[0]=="清空":
            sta = await data_source.cleals_table(config.db_file)
            await tiangou.finish("已清空" if sta==True else "发生错误")