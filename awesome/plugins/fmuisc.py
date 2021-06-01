from nonebot import on_command, CommandSession, MessageSegment

from requests import get


@on_command('test', aliases=('点歌'), only_to_me=False)
async def fmusic(session: CommandSession):
    music = session.get('music', prompt='你想听什么歌呢？')
    songid = await search(music)
    m = MessageSegment.music("qq", songid)
    await session.send(str(m))

# fmusic.args_parser 装饰器将函数声明为 weather 命令的参数解析器
# 命令解析器用于将用户输入的参数解析成命令真正需要的数据


@fmusic.args_parser
async def _(session: CommandSession):
    # 去掉消息首尾的空白符
    stripped_arg = session.current_arg_text.strip()
    if session.is_first_run:
        # 该命令第一次运行（第一次进入命令会话）
        if stripped_arg:
            # 第一次运行参数不为空，意味着用户直接将城市名跟在命令名后面，作为参数传入
            # 例如用户可能发送了：天气 南京
            session.state['music'] = stripped_arg
        return

    if not stripped_arg:
        # 用户没有发送有效的城市名称（而是发送了空白字符），则提示重新输入
        # 这里 session.pause() 将会发送消息并暂停当前会话（该行后面的代码不会被运行）
        session.pause('')

    # 如果当前正在向用户询问更多信息（例如本例中的要查询的城市），且用户输入有效，则放入会话状态
    session.state[session.current_key] = stripped_arg


async def callback(lists):
    print(lists)
    return lists


async def search(name: str) -> str:
    r = get(
        f'https://c.y.qq.com/soso/fcgi-bin/client_search_cp?aggr=1&cr=1&flag_qc=0&p=1&n=30&w={name}').text
    jsons = await eval(r)
    return jsons["data"]["song"]["list"][0]['songid']
