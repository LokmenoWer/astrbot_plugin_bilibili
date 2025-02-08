# astrbot_plugin_bilibili

Bilibili 插件

- 消息识别 BV 号返回视频信息
- 订阅 UP 动态
   - 指令：订阅动态 <b站id>、订阅列表、订阅删除 <b站id>。
- 推荐番剧。
   - 试着对 LLM 说 `推荐一些催泪的番剧，2016年之后的`。
   - 支持类别、番剧起始年份、番剧结束年份、番剧季度（一月番等）
   - 需要支持函数调用的 LLM。如 gpt-4o-mini
 
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
