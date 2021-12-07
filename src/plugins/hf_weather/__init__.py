'''
Author: GM
Date: 2021-11-23 18:28:50
LastEditors: GM
LastEditTime: 2021-12-06 21:24:18
Description: file content
'''
# import nonebot
from nonebot import get_driver
from nonebot import on_command
from .config import Config
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
from httpx import get
import json

global_config = get_driver().config
config = Config(**global_config.dict())


weather=on_command("天气")

@weather.handle()
async def weather_command(bot: Bot, event: Event, state: T_State):
    args = str(event.get_message()).strip()  # 首次发送命令时跟随的参数，例：/天气 上海，则args为上海
    if args:
        state["city"]=args

@weather.got("city")
async def handle_music(bot: Bot, event: Event, state: T_State):
    city=state["city"]
    weather_report = await get_weather(city)
    if weather_report != f"没有找到{city}":
        await weather.finish(weather_report)
    await weather.finish("水木说了：别瞎几把搜！")

async def get_weather(city: str) -> str:
    citycode = await get_city_id(city)
    if citycode != f"没有找到{city}":
        wea = await get_hefeng(citycode, city)
        return wea
    return citycode


async def get_city_id(city: str) -> str:
    r = get(f"https://geoapi.qweather.com/v2/city/lookup?location={city}&key={global_config.weaterapi}")
    json_str = json.loads(r.text)
    if json_str["code"] != '200':
        return f"没有找到{city}"
    return json_str["location"][0]['id']


async def get_hefeng(city, citystr) -> str:
    r = get(f"https://devapi.qweather.com/v7/weather/now?location={city}&key={global_config.weaterapi}")
    json_str = json.loads(r.text)
    if json_str["code"] == '200':
        # jstr["now"]["temp"]         # 实况温度，默认单位：摄氏度
        # jstr["now"]["feelsLike"]    # 实况体感温度，默认单位：摄氏度
        # jstr["now"]["text"]         # 阴晴雨雪等天气状态的描述
        # jstr["now"]["windDir"]      # 实况风向
        # jstr["now"]["windScale"]    # 实况风力等级
        # jstr["now"]["humidity"]     # 实况相对湿度，百分比数值
        # jstr["now"]["precip"]       # 实况降水量，默认单位：毫米
        # jstr["now"]["pressure"]     # 实况大气压强，默认单位：百帕
        # jstr["now"]["vis"]          # 实况能见度，默认单位：公里
        # jstr["now"]["cloud"]        # 实况云量，百分比数值
        # jstr["now"]["dew"]          # 实况露点温度
        return f"{citystr}当前温度："+json_str["now"]["temp"]+"℃\n天气状况:"+json_str["now"]["text"] 
    return f"{citystr}天气查询失败"