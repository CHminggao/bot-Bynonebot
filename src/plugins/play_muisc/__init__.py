'''
Author: GM
Date: 2021-11-23 17:24:45
LastEditors: GM
LastEditTime: 2021-11-24 18:06:33
Description: file content
'''
# import nonebot
from httpx import get
from nonebot.adapters.cqhttp.message import MessageSegment
from nonebot import get_driver
from nonebot import on_command
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
from .config import Config

global_config = get_driver().config
config = Config(**global_config.dict())

play_music=on_command("点歌")

@play_music.handle()
async def music_command(bot: Bot, event: Event, state: T_State):
    args = str(event.get_message()).strip()  # 首次发送命令时跟随的参数，例：/天气 上海，则args为上海
    if args:
        state["music-name"]=args
        
@play_music.got("music-name")
async def handle_music(bot: Bot, event: Event, state: T_State):
    music=state["music-name"]
    if music:
        songid = await search(music)
        if songid==0:
            await play_music.finish()
        else:
            m = MessageSegment.music("qq",songid)
            await play_music.finish(m)

async def search(name: str) -> str:
    r = get(
        f'https://c.y.qq.com/soso/fcgi-bin/client_search_cp?aggr=1&cr=1&flag_qc=0&p=1&n=30&w={name}').text
    jsons = await eval(r)
    try:
        return jsons["data"]["song"]["list"][0]['songid']
    except :
        return 0
    

async def callback(lists):
    return lists

