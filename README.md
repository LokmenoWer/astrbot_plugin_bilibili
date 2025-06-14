# astrbot_plugin_bilibili

这是一个为 [AstrBot](https://github.com/Soulter/AstrBot) 设计的多功能 Bilibili 插件。

## ✨ 功能特性

  - **Bilibili 视频解析**：自动识别消息中的 `BV` 号，并返回视频的详细信息。
  - **UP 主动态订阅**：
      - 支持订阅 `视频动态`、`图文动态` 和 `直播`。
      - 提供灵活的关键词和类型过滤。
      - 默认轮询时间为 `5` 分钟，可根据需要在插件配置中修改。
   - **推荐番剧**
      - 试着对 LLM 说 `推荐一些催泪的番剧，2016年之后的`。
      - 支持类别、番剧起始年份、番剧结束年份、番剧季度（一月番等）
      - 需要支持函数调用的 LLM。如 gpt-4o-mini
  - **QQ 小程序解析**：自动识别并解析 QQ 聊天中分享的 Bilibili 小程序，提取并返回直链。
  - 后续还会增加更多功能！！

![image](https://github.com/user-attachments/assets/972b2b99-b801-45cf-a882-6d841c9e8137)
## 🚀 安装

- 在插件市场下载
- 通过以下指令进行安装：

```shell
plugin i https://github.com/Soulter/astrbot_plugin_bilibili
```

## ⚙️ 配置

插件需要配置 `sessdata` 才能正常获取 Bilibili 数据。

参考 [此指南](https://nemo2011.github.io/bilibili-api/#/get-credential) 获取你的 `sessdata`。

<img width="1453" alt="image" src="https://github.com/user-attachments/assets/d5342767-8e5c-4222-81da-f1cdb4b30c95">

## 📖 使用说明

### 动态订阅指令

| 指令 | 参数 | 说明 | 别名 |
| :--- | :--- | :--- | :--- |
| **订阅动态** | `<B站UID> [过滤器...]` | 订阅指定 UP 主的动态。可以添加多个过滤器（以空格分隔）以排除不感兴趣的内容。 | `bili_sub` |
| **订阅列表** | (无) | 显示当前会话的所有订阅。 | `bili_sub_list` |
| **订阅删除** | `<B站UID>` | 删除当前会话中对指定 UP 主的订阅。 | `bili_sub_del` |
| **全局删除** | `<SID>` | **[管理员]** 删除指定 SID 会话的所有订阅。使用 `/sid` 指令可查看会话 SID。 | `bili_global_del` |
| **全局列表** | (无) | **[管理员]** 查看所有会话的订阅情况。 |

#### 过滤器说明

过滤器可以是以下几种类型：

  - `forward`：过滤掉转发动态。
  - `lottery`：过滤掉互动抽奖动态。
  - `video`：过滤掉视频发布动态。
  - **正则表达式**：任何不属于上述关键字的字符串都将被视为正则表达式，用于过滤动态文本内容。

**示例**：
`/订阅动态 123456 lottery 关注`
`/bili_sub 123456 lottery 关注`
这条指令会订阅 UID 为 `123456` 的 UP 主，但会过滤掉**抽奖动态**以及动态内容中包含“**关注**”二字的动态。

> **提示**：该指令也用于更新已订阅 UP 主的过滤条件。

## 适用平台/适配器

  - aiocqhttp
  - nakuru

## Contributors

1. [@Flartiny](https://github.com/Flartiny)
2. [@Soulter](https://github.com/Soulter)

## 更新日志

### v1.4.10

- 添加指令别名

### v1.4.9

- 现在使用订阅列表命令时显示UP主用户名
- 修复Image类名冲突导致的概率报错

### v1.4.8

- 修复裁剪图片导致的清晰度降低
- 支持添加自部署t2i接口提升图片质量
