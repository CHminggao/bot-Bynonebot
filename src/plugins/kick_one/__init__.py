'''
Author: GM
Date: 2021-11-24 18:13:50
LastEditors: GM
LastEditTime: 2021-11-24 18:38:57
Description: file content
'''
# import nonebot
from nonebot import get_driver
from nonebot import on_command
from nonebot.permission import SUPERUSER
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
from nonebot.rule import to_me
from .config import Config

global_config = get_driver().config
config = Config(**global_config.dict())

kick_one=on_command("踢出群主")

@kick_one.handle()
async def kick_handle(bot: Bot, event: Event, state: T_State):
    args = str(event.get_message()).strip()
    # await bot.call_api("set_group_kick",group_id=711498146,user_id=3423065435)
    # all_list = await bot.call_api("get_group_member_list",group_id=event.group_id)
    await kick_one.finish("踢出群主失败，请重试")