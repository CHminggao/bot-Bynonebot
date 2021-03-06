'''
Author: GM
Date: 2021-11-24 18:13:50
LastEditors: GM
LastEditTime: 2021-12-24 09:33:09
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

kick_one=on_command("踢出")

@kick_one.handle()
async def kick_handle(bot: Bot, event: GroupMessageEvent, state: T_State):
    args = str(event.get_message()).strip()
    if args:
        state["someone"]=args
    if await GROUP_ADMIN(bot, event) or await GROUP_OWNER(bot, event) or str(event.user_id) in list(global_config.superusers):
        print()
    else:
        await kick_one.finish("想啥呢，你只是普通人！")

@kick_one.got("someone",prompt="要踢出谁呢？")
async def _(bot: Bot, event: GroupMessageEvent, state: T_State):
    msg="0、退出\n"
    i=1
    list_user=[]
    if event.get_message()[0].type=='at':
        state['someone']=event.get_message()[0].data['qq']
    all_list = await bot.call_api("get_group_member_list",group_id=event.group_id)
    try:
        find=int(state['someone'])
    except ValueError:
        find=0
    for item in all_list:
        if state['someone'] in item["card"] or state['someone'] in item["nickname"]:
            if item["card"]:
                msg+=str(i)+"、"+ item["card"] +"  "+ str(item['user_id'])+'\n'
            else:
                msg+=str(i)+"、"+ item["nickname"] +"  "+ str(item['user_id'])+'\n'
            list_user.append(item['user_id'])
            i+=1
        elif find>0 and find==item["user_id"] :
            if item["card"]:
                msg+=str(i)+"、"+ item["card"] +"  "+ str(item['user_id'])+'\n'
            else:
                msg+=str(i)+"、"+ item["nickname"] +"  "+ str(item['user_id'])+'\n'
            list_user.append(item['user_id'])
            i+=1
    if i>10:
        await kick_one.finish("查询到人数过多请重新输入")
    elif i==1:
        await kick_one.finish("没有查询到请重新输入")
    else :
        state['somelist']=list_user
        await kick_one.send(msg)

@kick_one.got('yes')
async def y(bot:Bot,event:GroupMessageEvent,state:T_State):
    b = event.get_message()
    try:
        i=int(str(b))
        if i==0:
            await kick_one.finish('已退出')
        else:
            qq_num = state['somelist'][i-1]
    except IndexError :
        await kick_one.reject("请重新输入序号")
    except :
        await kick_one.finish('')
    else:
        try:
            await bot.call_api("set_group_kick",group_id=event.group_id,user_id=qq_num)
            await kick_one.finish("踢出完成")
        except ActionFailed:
            await kick_one.finish("权限不足")

