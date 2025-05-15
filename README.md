# astrbot_plugin_bilibili

Bilibili 插件

> [!Note]
> 需要 curl_cffi 版本在 0.8.1b9。使用 pip install curl_cffi~=0.8.1b9 安装

- 消息识别 BV 号返回视频信息
- 订阅 UP 动态：支持 `直播` `图文动态` `视频动态` 的订阅
   - 指令：
      - `订阅动态 <b站id> <string>` - <string>可以为多个以空格分隔的字符串若为forward(转发动态),lottery(互动抽奖)，video(视频发布)则过滤对应类型的动态，否则视作正则表达式过滤。例如：`/订阅动态 123456 lottery 关注`表示订阅123456的动态，同时过滤转发动态和含"关注"的动态。此指令亦用于更新已订阅对象的过滤条件。
      - `订阅列表`
      - `订阅删除 <b站id>`。
      - `全局删除 <sid>` - 管理员指令。删除对应 SID 的会话的所有订阅。使用 /sid 指令可以查看会话的 SID。对于 aiocqhttp 用户，可以直接输入 QQ 群号或者 QQ 号来删除
      - `全局列表` - 管理员指令。查看所有订阅过的会话。
   - 订阅列表轮询时间是 `5` 分钟检查一轮。可以进插件配置修改。
- 推荐番剧。
   - 试着对 LLM 说 `推荐一些催泪的番剧，2016年之后的`。
   - 支持类别、番剧起始年份、番剧结束年份、番剧季度（一月番等）
   - 需要支持函数调用的 LLM。如 gpt-4o-mini
- 识别转发时的qq小程序并返回视频直链 
- 后续还会增加更多功能！！
 
![image](https://github.com/user-attachments/assets/972b2b99-b801-45cf-a882-6d841c9e8137)


## 使用
需要在面板配置 sessdata。

<img width="1453" alt="image" src="https://github.com/user-attachments/assets/d5342767-8e5c-4222-81da-f1cdb4b30c95">

获取 sessdata 参见 https://nemo2011.github.io/bilibili-api/#/get-credential

## 适用平台/适配器
- aiocqhttp
- nakuru

## 安装方式
```
plugin i https://github.com/Soulter/astrbot_plugin_bilibili
```
