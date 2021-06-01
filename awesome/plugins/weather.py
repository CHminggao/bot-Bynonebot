from nonebot import on_command, CommandSession


import requests
import json

# 天气接口请求token     https://dev.qweather.com/ 和风天气获取Key
key=''

# on_command 装饰器将函数声明为一个命令处理器
# 这里 weather 为命令的名字，同时允许使用别名「天气」「天气预报」「查天气」
@on_command('weather',aliases=('天气'),only_to_me=False)
async def weather(session:CommandSession):
    city = session.get('city',prompt='你想查询哪个城市的天气呢？')
    weather_report = await get_weather(city)
    await session.send(weather_report)

# weather.args_parser 装饰器将函数声明为 weather 命令的参数解析器
# 命令解析器用于将用户输入的参数解析成命令真正需要的数据
@weather.args_parser
async def _(session: CommandSession):
    # 去掉消息首尾的空白符
    stripped_arg = session.current_arg_text.strip()
    if session.is_first_run:
        # 该命令第一次运行（第一次进入命令会话）
        if stripped_arg:
            # 第一次运行参数不为空，意味着用户直接将城市名跟在命令名后面，作为参数传入
            # 例如用户可能发送了：天气 南京
            session.state['city'] = stripped_arg
        return

    if not stripped_arg:
        # 用户没有发送有效的城市名称（而是发送了空白字符），则提示重新输入
        # 这里 session.pause() 将会发送消息并暂停当前会话（该行后面的代码不会被运行）
        session.pause('')

    # 如果当前正在向用户询问更多信息（例如本例中的要查询的城市），且用户输入有效，则放入会话状态
    session.state[session.current_key] = stripped_arg

async def get_weather(city: str) -> str:
    citycode = await get_city_id(city)
    if citycode != f"没有找到{city}":
        wea = await get_hefeng(citycode, city)
        return wea
    return citycode


async def get_city_id(city: str) -> str:
    r = requests.get(f"https://geoapi.qweather.com/v2/city/lookup?location={city}&key={key}")
    jstr = json.loads(r.text)
    if jstr["code"] != '200':
        return f"没有找到{city}"
    return jstr["location"][0]['id']


async def get_hefeng(city, citystr) -> str:
    r = requests.get(f"https://devapi.qweather.com/v7/weather/now?location={city}&key={key}")
    jstr = json.loads(r.text)
    if jstr["code"] == '200':
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
        return f"{citystr}当前温度："+jstr["now"]["temp"]+"℃\n天气状况:"+jstr["now"]["text"] 
    return f"{citystr}天气查询失败"