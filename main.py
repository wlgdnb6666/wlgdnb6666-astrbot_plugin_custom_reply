from astrbot.api.all import *

class CustomReplyPlugin(Star):
    # 使用 *args 和 **kwargs 接收所有可能的初始化参数，彻底解决版本差异
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 在 v4.13.x 中，配置通常存储在 self.context.config 或 self.config
        # 我们做一个安全的兼容处理
        config_obj = getattr(self, "config", getattr(self.context, "config", {}))
        self.reply_map = config_obj.get("replies", {"1": "2"})

    # 底层事件监听
    async def handle_event(self, event: AstrMessageEvent):
        # 确认是消息事件
        if not isinstance(event, AstrMessageEvent):
            return

        # 获取并清洗用户消息
        message = event.message_obj.message_str.strip()

        # 匹配回复字典
        if message in self.reply_map:
            # 停止事件传播，拦截 LLM 和其他插件
            event.stop_event()
            
            # 发送回复内容
            reply_content = self.reply_map[message]
            yield event.plain_result(reply_content)

    # 兼容配置实时更新
    async def on_config_loaded(self):
        config_obj = getattr(self, "config", getattr(self.context, "config", {}))
        self.reply_map = config_obj.get("replies", {"1": "2"})
