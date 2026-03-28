from astrbot.api.all import *

class CustomReplyPlugin(Star):
    def __init__(self, context: Context, config: dict):
        super().__init__(context)
        self.config = config
        # 初始化回复表，默认 1 -> 2
        self.reply_map = self.config.get("replies", {"1": "2"})

    # 在 v4.13.x 版本中，最稳妥的监听器装饰器
    @event_message()
    async def handle_custom_reply(self, event: AstrMessageEvent):
        '''
        监听消息并匹配自定义回复
        '''
        # 获取消息文本内容并去除首尾空格
        message = event.message_obj.message_str.strip()

        # 检查是否命中关键字
        if message in self.reply_map:
            # 停止事件传播，彻底拦截 LLM 的回复
            event.stop_event()
            
            # 获取对应的回复内容
            reply_content = self.reply_map[message]
            
            # 发送结果
            yield event.plain_result(reply_content)

    # 监听配置加载
    @on_config_loaded()
    async def on_config_updated(self, event: AstrMessageEvent):
        self.reply_map = self.config.get("replies", {"1": "2"})
