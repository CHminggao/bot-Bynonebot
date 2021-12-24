'''
Author: GM
Date: 2021-12-06 21:17:54
LastEditors: GM
LastEditTime: 2021-12-24 09:51:14
Description: file content
'''
# import nonebot
import json
from typing import Optional
from nonebot.rule import to_me
from nonebot import get_driver, on_message
from nonebot.adapters import Bot, Event
from nonebot.typing import T_State
from tencentcloud.common import credential
from tencentcloud.common.exception.tencent_cloud_sdk_exception import \
    TencentCloudSDKException
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.nlp.v20190408 import models, nlp_client


from .config import Config

global_config = get_driver().config
config = Config(**global_config.dict())

tencent=on_message(priority=5,rule=to_me())
@tencent.handle()
async def nlp_message(bot: Bot, event: Event, state: T_State):
    args = str(event.get_message()).strip()  # 消息
    reback = await nlp_textchat(args)
    await tencent.finish(reback)


async def nlp_textchat(text: str) -> Optional[str]:
    """
    @description  : 腾讯智能闲聊
    ---------
    @param  :
    -------
    @Returns  :
    -------
    """
    try: 
        
        cred = credential.Credential(global_config.tencentcloudkey1, global_config.tencentcloudkey2) 
        httpProfile = HttpProfile()
        httpProfile.endpoint = "nlp.tencentcloudapi.com"
        
        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        client = nlp_client.NlpClient(cred, "ap-guangzhou", clientProfile) 
        
        req = models.ChatBotRequest()
        params = {
        	"Query": text
        }
        req.from_json_string(json.dumps(params))
        
        resp = client.ChatBot(req) 
        return resp.Reply
        
    except TencentCloudSDKException as err: 
        print(err) 
        return '哦淦！？'
