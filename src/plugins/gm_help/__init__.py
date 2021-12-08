'''
Author: GM
Date: 2021-11-24 17:14:41
LastEditors: GM
LastEditTime: 2021-12-08 17:37:00
Description: file content
'''
# import nonebot
from nonebot import get_driver
from nonebot import on_startswith
from .config import Config
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event

global_config = get_driver().config
config = Config(**global_config.dict())

gm_help=on_startswith("帮助")

@gm_help.handle()
async def help_handle(bot: Bot, event: Event, state: T_State):
    args = str(event.get_message()).lstrip("帮助 ")
    if args=="":
        await gm_help.finish("当前可使用命令：\n点歌\t舔狗日记\n天气\t踢出\n查看具体命令：帮助 点歌")
    elif args=='点歌':
        await gm_help.finish("点歌 歌名")
    elif args=="舔狗日记":
        await gm_help.finish("舔狗日记\n舔狗日记 新增 内容")
    elif args=="天气":
        await gm_help.finish("天气 城市名称")
    elif args=="踢出":
        await gm_help.finish("天气 群名片或昵称或qq号")