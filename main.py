from astrbot.api.all import *

class CustomReplyPlugin(Star):
    def __init__(self, context: Context, config: dict = None):
        super().__init__(context)
        # 获取配置
        self.config_data = config if config else getattr(self.context, "config", {})
        self.reply_map = self.config_data.get("replies", {"1": "2"})

    # 提高优先级，确保在 LLM 之前拦截
    def priority(self) -> int:
        return -1

    @event_filter.on_recv_message()
    async def handle_custom_reply(self, event: AstrMessageEvent):
        # 1. 获取消息原文并去除前后空格
        message = event.message_obj.message_str.strip()

        # 2. 如果消息是以 / 开头的，直接跳过，不触发本插件逻辑
        if message.startswith('/'):
            return

        # 3. 匹配关键字（全匹配）
        if message in self.reply_map:
            # 停止事件，让 LLM 闭嘴
            event.stop_event()
            
            # 获取回复内容
            reply_content = self.reply_map[message]
            
            # 发送结果
            yield event.plain_result(reply_content)

    async def on_config_loaded(self):
        self.config_data = getattr(self, "config", getattr(self.context, "config", {}))
        self.reply_map = self.config_data.get("replies", {"1": "2"})
