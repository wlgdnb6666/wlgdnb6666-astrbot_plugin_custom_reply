from astrbot.api.all import *

class CustomReplyPlugin(Star):
    def __init__(self, context: Context, config: dict):
        super().__init__(context)
        self.config = config
        # 初始化回复字典
        self.reply_map = self.config.get("replies", {"1": "2"})

    # 不使用装饰器，直接重写这个底层方法
    async def handle_event(self, event: AstrMessageEvent):
        # 1. 基础检查：确保是消息事件
        if not isinstance(event, AstrMessageEvent):
            return

        # 2. 获取用户发送的纯文本
        message = event.message_obj.message_str.strip()

        # 3. 匹配回复
        if message in self.reply_map:
            # 停止事件传播，彻底拦截 LLM 的回复
            event.stop_event()
            
            # 获取对应的回复内容并返回
            reply_content = self.reply_map[message]
            yield event.plain_result(reply_content)

    # 监听配置变动
    async def on_config_loaded(self):
        self.reply_map = self.config.get("replies", {"1": "2"})
