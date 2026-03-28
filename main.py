from astrbot.api.all import *
from astrbot.api.event import filter as event_filter # 显式导入过滤器

@register("custom_reply", "青禾遇海", "自定义回复并拦截LLM", "1.0.2", "https://github.com/wlgdnb6666/wlgdnb6666-astrbot_plugin_custom_reply")
class CustomReplyPlugin(Star):
    def __init__(self, context: Context, config: dict):
        super().__init__(context)
        self.config = config
        # 如果配置里没写回复，默认给个 1 -> 2
        self.reply_map = self.config.get("replies", {"1": "2"})

    @event_filter.on_recv_message()
    async def on_message(self, event: AstrMessageEvent):
        # 获取消息文本
        user_text = event.message_obj.message_str.strip()
        
        if user_text in self.reply_map:
            # 停止事件，拦截 LLM
            event.stop_event()
            
            # 回复内容
            reply_text = self.reply_map[user_text]
            yield event.plain_result(reply_text)
