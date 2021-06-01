from nonebot import on_command, CommandSession
from nonebot import on_natural_language, NLPSession, IntentCommand
from nonebot.helpers import context_id, render_expression
from typing import Optional
# import aiohttp
from aiocqhttp.message import escape

import urllib
import requests
import json
import base64
import hashlib
import time
import random
import re

#  https://ai.qq.com/  获取AppId和AppKey
app_id=""
app_key=""



@on_command('qqbot')
async def qqbot(session:CommandSession):
    # 获取可选参数，这里如果没有 message 参数，命令不会被中断，message 变量会是 None
    message = session.state.get('message')
    # 通过封装的函数获取机器人的回复
    reply = await nlp_textchat(session, message)
    if reply:
        # 如果调用机器人成功，得到了回复，则转义之后发送给用户
        # 转义会把消息中的某些特殊字符做转换，以避免 酷Q 将它们理解为 CQ 码
        await session.send(escape(reply))
    else:
        # 如果调用失败，或者它返回的内容我们目前处理不了，发送无法获取回复时的「表达」
        # 这里的 render_expression() 函数会将一个「表达」渲染成一个字符串消息
        await session.send(render_expression(EXPR_DONT_UNDERSTAND))

@on_natural_language
async def _(session: NLPSession):
    # 以置信度 60.0 返回 qqbot 命令
    # 确保任何消息都在且仅在其它自然语言处理器无法理解的时候使用 qqbot 命令
    return IntentCommand(60.0, 'qqbot', args={'message': session.msg_text})

async def genSignString(parser):
    """
    @description  : 获取签名
    ---------
    @param  :
    -------
    @Returns  :
    -------
    """
    
    uri_str = ''
    for key in sorted(parser.keys()):
        if key == 'app_key':
            continue
        uri_str += "%s=%s&" % (key, urllib.parse.quote(str(parser[key]).encode('utf-8'), safe = ''))
    sign_str = uri_str + 'app_key=' + parser['app_key']

    hash_md5 = hashlib.md5(sign_str.encode('utf-8'))
    return hash_md5.hexdigest().upper()


async def nlp_textchat(session: CommandSession, text: str) -> Optional[str]:
    """
    @description  : 腾讯智能闲聊
    ---------
    @param  :
    -------
    @Returns  :
    -------
    """
    data={}
    timett=int(time.time())
    if not text:
        return None
    data["app_id"] = app_id
    data["app_key"] = app_key
    data["session"] = str(session.event.user_id)
    data["question"] = re.sub('\s+', '', text).strip()
    data["time_stamp"] = timett
    data["nonce_str"] = ''.join(random.sample('zyxwvutsrqponmlkjihgfedcba0123456789',32))
    sign_str=await genSignString(data)
    data['sign']=sign_str
    
    r=requests.post('https://api.ai.qq.com/fcgi-bin/nlp/nlp_textchat',data=data)
    str_=json.loads(r.text)
    
    if str_['ret'] == 0:
        return str_['data']['answer']
    else:
        print(str_['msg'])
        return '呃。。你说了啥？'
