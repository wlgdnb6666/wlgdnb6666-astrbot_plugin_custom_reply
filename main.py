from astrbot.api.all import *

class CustomReplyPlugin(Star):
    # 显式写出两个参数，满足 v4.13.1 的实例化需求
    def __init__(self, context: Context, config: dict):
        super().__init__(context)
        self.config = config
        # 初始化回复表
        self.reply_map = self.config.get("replies", {"1": "2"})

    # 使用 handle_event 确保最高兼容性
    async def handle_event(self, event: AstrMessageEvent):
        # 确认是消息事件
        if not isinstance(event, AstrMessageEvent):
            return

        # 获取消息文本
        message = event.message_obj.message_str.strip()

        # 匹配回复字典
        if message in self.reply_map:
            # 停止事件传播，拦截 LLM
            event.stop_event()
            
            # 发送结果
            reply_content = self.reply_map[message]
            yield event.plain_result(reply_content)

    # 监听配置加载
    async def on_config_loaded(self):
        self.reply_map = self.config.get("replies", {"1": "2"})
