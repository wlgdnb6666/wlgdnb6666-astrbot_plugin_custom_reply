from astrbot.api.all import *

class CustomReplyPlugin(Star):
    def __init__(self, context: Context): # 去掉了 config 参数
        super().__init__(context)
        # 在 v4.13.1 中，通过 self.context.config 获取配置
        self.reply_map = self.context.config.get("replies", {"1": "2"})

    # 底层监听方法
    async def handle_event(self, event: AstrMessageEvent):
        # 确保是消息事件
        if not isinstance(event, AstrMessageEvent):
            return

        # 获取用户消息并去除空格
        message = event.message_obj.message_str.strip()

        # 匹配回复字典
        if message in self.reply_map:
            # 停止事件传播，拦截 LLM
            event.stop_event()
            
            # 发送结果
            reply_content = self.reply_map[message]
            yield event.plain_result(reply_content)

    # 兼容配置更新逻辑
    async def on_config_loaded(self):
        self.reply_map = self.context.config.get("replies", {"1": "2"})
