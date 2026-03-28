from astrbot.api.all import *
from astrbot.api.event import filter, AstrMessageEvent 
import astrbot.api.message_components as Comp
import json
import os

class CustomReplyPlugin(Star):
    def priority(self) -> int:
        return -1

    def get_local_config(self):
        config_path = os.path.join(os.path.dirname(__file__), "config.json")
        try:
            if os.path.exists(config_path):
                with open(config_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            pass
        return {}

    @filter.event_message_type(filter.EventMessageType.ALL)
    async def on_all_message(self, event: AstrMessageEvent):
        # 1. 获取消息并转为小写（实现大小写不敏感匹配）
        message = event.message_str.strip()
        if not message or message.startswith('/'):
            return

        # 2. 获取配置
        local_data = self.get_local_config()
        replies = local_data.get("replies", {})
        
        if not replies:
            config = getattr(self, "config", getattr(self.context, "config", {}))
            replies = config.get("replies", {})

        # 3. 强制保底
        if not replies:
            replies = {"你好": "你也好呀！"}

        # 4. 模糊匹配逻辑
        matched_content = None
        for key, value in replies.items():
            # 判断逻辑：如果【触发词】在【用户消息】中
            # 例如：触发词是 "你好"，用户说 "嗨你好呀"，则匹配成功
            trigger_word = str(key).strip()
            if trigger_word and trigger_word in message:
                matched_content = value
                break
        
        # 5. 回复
        if matched_content:
            event.stop_event() # 拦截消息，不传给大模型
            chain = [Comp.Plain(str(matched_content))]
            yield event.chain_result(chain)

    async def on_config_loaded(self):
        pass
