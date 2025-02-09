from astrbot.api.all import *
from astrbot.api.event import CommandResult, AstrMessageEvent
from bilibili_api import user, Credential, video, bangumi
from astrbot.api.message_components import Image, Plain
from astrbot.api.event.filter import command, regex, llm_tool
from bilibili_api.bangumi import IndexFilter as IF
from .constant import category_mapping
from .dynamics import parse_last_dynamic
import asyncio
import logging
import re
import os
import json

DEFAULT_CFG = {
    "bili_sub_list": {}  # sub_user -> [{"uid": "uid", "last": "last_dynamic_id"}]
}
DATA_PATH = "data/astrbot_plugin_bilibili.json"
BV = r"(?:\?.*)?(?:https?:\/\/)?(?:www\.)?bilibili\.com\/video\/(BV[\w\d]+)\/?(?:\?.*)?"
logger = logging.getLogger("astrbot")


@register("astrbot_plugin_bilibili", "Soulter", "", "", "")
class Main(Star):
    def __init__(self, context: Context, config: dict) -> None:
        super().__init__(context)
        
        self.cfg = config
        self.credential = None
        if not self.cfg["sessdata"]:
            logger.error("请设置 bilibili sessdata")
        else:
            self.credential = Credential(self.cfg["sessdata"])
        self.context = context

        if not os.path.exists(DATA_PATH):
            with open(DATA_PATH, "w", encoding="utf-8-sig") as f:
                f.write(json.dumps(DEFAULT_CFG, ensure_ascii=False, indent=4))
        with open(DATA_PATH, "r", encoding="utf-8-sig") as f:
            self.data = json.load(f)

        self.context.register_task(self.dynamic_listener(), "bilibili动态监听")

    @regex(BV)
    async def get_video_info(self, message: AstrMessageEvent):
        if len(message.message_str) == 12:
            bvid = message.message_str
        else:
            match_ = re.search(BV, message.message_str, re.IGNORECASE)
            if not match_:
                return
            bvid = "BV" + match_.group(1)[2:]

        v = video.Video(bvid=bvid)
        info = await v.get_info()
        online = await v.get_online()
        ret = f"""Billibili 视频信息：
标题: {info['title']}
UP主: {info['owner']['name']}
播放量: {info['stat']['view']}
点赞: {info['stat']['like']}
投币: {info['stat']['coin']}
总共 {online['total']} 人正在观看"""
        ls = [Plain(ret), Image.fromURL(info["pic"])]

        result = CommandResult()
        result.chain = ls
        result.use_t2i(False)
        return result

    async def save_cfg(self):
        with open(DATA_PATH, "w", encoding="utf-8") as f:
            f.write(json.dumps(self.data, ensure_ascii=False, indent=2))
    
    @command("订阅动态")
    async def dynamic_sub(self, message: AstrMessageEvent, uid: str):
        '''添加 bilibili 动态监控'''
        sub_user = message.unified_msg_origin
        if uid.isdigit():
            if sub_user:
                if sub_user in self.data["bili_sub_list"]:
                    self.data["bili_sub_list"][sub_user].append(
                        {"uid": int(uid), "last": ""}
                    )
                else:
                    self.data["bili_sub_list"][sub_user] = [
                        {"uid": int(uid), "last": ""}
                    ]
                await self.save_cfg()
                return CommandResult().message("添加成功")
            else:
                return CommandResult().message("用户信息缺失")
        
    @command("订阅列表")
    async def sub_list(self, message: AstrMessageEvent):
        '''查看 bilibili 动态监控列表'''
        sub_user = message.unified_msg_origin
        ret = """订阅列表：\n"""
        if sub_user in self.data["bili_sub_list"]:
            for idx, uid_sub_data in enumerate(
                self.data["bili_sub_list"][sub_user]
            ):
                ret += f"{idx+1}. {uid_sub_data['uid']}\n"
            return CommandResult().message(ret)
        else:
            return CommandResult().message("无订阅")
        
    @command("订阅删除")
    async def sub_del(self, message: AstrMessageEvent, uid: str):
        '''删除 bilibili 动态监控'''
        sub_user = message.unified_msg_origin
        if sub_user in self.data["bili_sub_list"]:
            if len(uid) < 1:
                return CommandResult().message("参数数量不足。订阅动态 b站id")

            uid = int(uid)

            for idx, uid_sub_data in enumerate(
                self.data["bili_sub_list"][sub_user]
            ):
                if uid_sub_data["uid"] == uid:
                    del self.data["bili_sub_list"][sub_user][idx]
                    await self.save_cfg()
                    return CommandResult().message("删除成功")
            return CommandResult().message("未找到指定的订阅")
        else:
            return CommandResult().message("不存在")
    
    async def dynamic_listener(self):
        while True:
            await asyncio.sleep(60*20)
            if self.credential is None:
                logger.warning("bilibili sessdata 未设置，无法获取动态")
                continue
            for sub_usr in self.data["bili_sub_list"]:
                for idx, uid_sub_data in enumerate(self.data["bili_sub_list"][sub_usr]):
                    try:
                        usr = user.User(uid_sub_data["uid"], credential=self.credential)
                        dyn = await usr.get_dynamics_new()
                        if dyn:
                            ret, dyn_id = await parse_last_dynamic(dyn, uid_sub_data)
                            if not ret:
                                continue
                            await self.context.send_message(sub_usr, ret)
                            self.data["bili_sub_list"][sub_usr][idx]["last"] = dyn_id
                            await self.save_cfg()
                    except Exception as e:
                        raise e

    @llm_tool("get_bangumi")
    async def get_bangumi(self, message: AstrMessageEvent, style: str = "ALL", season: str = "ALL", start_year: int = None, end_year: int = None):
        """当用户希望推荐番剧时调用。根据用户的描述获取前 5 条推荐的动漫番剧。

        Args:
            style(string): 番剧的风格。默认为全部。可选值有：原创, 漫画改, 小说改, 游戏改, 特摄, 布袋戏, 热血, 穿越, 奇幻, 战斗, 搞笑, 日常, 科幻, 萌系, 治愈, 校园, 儿童, 泡面, 恋爱, 少女, 魔法, 冒险, 历史, 架空, 机战, 神魔, 声控, 运动, 励志, 音乐, 推理, 社团, 智斗, 催泪, 美食, 偶像, 乙女, 职场
            season(string): 番剧的季度。默认为全部。可选值有：WINTER, SPRING, SUMMER, AUTUMN。其也分别代表一月番、四月番、七月番、十月番
            start_year(number): 起始年份。默认为空，即不限制年份。
            end_year(number): 结束年份。默认为空，即不限制年份。
        """
        
        if style in category_mapping:
            style = getattr(IF.Style.Anime, category_mapping[style], IF.Style.Anime.ALL)
        else:
            style = IF.Style.Anime.ALL
        
        if season in ["WINTER", "SPRING", "SUMMER", "AUTUMN"]:
            season = getattr(IF.Season, season, IF.Season.ALL)
        else:
            season = IF.Season.ALL
        
        filters = bangumi.IndexFilterMeta.Anime(
            area=IF.Area.JAPAN,
            year=IF.make_time_filter(start=start_year, end=end_year, include_end=True),
            season=season,
            style=style,
        )
        index = await bangumi.get_index_info(
            filters=filters, order=IF.Order.SCORE, sort=IF.Sort.DESC, pn=1, ps=5
        )
        
        result = "推荐的番剧:\n"
        for item in index['list']:
            result += f"标题: {item['title']}\n"
            result += f"副标题: {item['subTitle']}\n"
            result += f"评分: {item['score']}\n"
            result += f"集数: {item['index_show']}\n"
            result += f"链接: {item['link']}\n"
            result += "\n"
        result += "请分点，贴心地回答。不要输出 markdown 格式。"
        return result