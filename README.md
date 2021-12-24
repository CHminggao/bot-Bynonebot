
# gm-bot

## How to start

1. generate project using `nb create` .
2. writing your plugins under `src/plugins` folder.
3. run your bot using `nb run` .



需要添加 `.env.dev` :

```
HOST=127.0.0.1
PORT=18181

DEBUG=true #正式使用这项改为false

#天气
weaterapi=""  # 和风天气key

#智能闲聊
tencentcloudkey1="" #腾讯id
tencentcloudkey2="" #腾讯key

#舔狗日记 sqlite数据库绝对路径
db_file='C:/Users/Administrator/Desktop/qq_go/gm.db'
```



