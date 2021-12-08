'''
Author: GM
Date: 2021-12-08 18:15:22
LastEditors: GM
LastEditTime: 2021-12-08 18:35:35
Description: file content
'''
# import nonebot

from nonebot import get_driver, on_command
from nonebot.adapters import Bot, Event
from nonebot.adapters.cqhttp import GROUP_ADMIN, GROUP_OWNER, GroupMessageEvent
from nonebot.typing import T_State
from nonebot.exception import ActionFailed
from .config import Config

global_config = get_driver().config
config = Config(**global_config.dict())

group_ban=on_command("禁言")

@group_ban.handle()
async def _(bot: Bot, event: GroupMessageEvent, state: T_State):
    if await GROUP_ADMIN(bot, event) or await GROUP_OWNER(bot, event) or str(event.user_id) in list(global_config.superusers):
        print()
    else:
        await group_ban.finish("想啥呢，你只是普通人！")
    msg =list( event.get_message())
    length = len(msg)
    if length==0:
        state['soneone']=''
    elif length==1:
        if msg[0].type=='at':
            state['soneone']=msg[0].data['qq']
            print()
        else :
            state['soneone']=""
    elif length==2:
        if msg[0].type=='at' and msg[0].type=='text':
            qq_num=msg[0].data['qq']
            num=msg[1].data['text']
            await ____(qq_num,num,event.group_id,bot)
    print()

async def ____ (qq_num:int,num:str,group_id,bot:Bot):
    try:
        n=int(num)
    except ValueError:
        group_ban.finish("请输入正确时长")
    else:
        await bot.call_api('set_group_ban',group_id=group_id,user_id=qq_num,duration=n)