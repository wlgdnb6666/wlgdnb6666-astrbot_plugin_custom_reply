from astrbot.api.all import *

class CustomReplyPlugin(Star):
    def __init__(self, context: Context, config: dict):
        super().__init__(context)
        self.config = config
        # 初始化回复映射，优先从 WebUI 配置读取
        self.reply_map = self.config.get("replies", {"1": "2"})

    @event_filter.on_recv_message()
    async def handle_custom_reply(self, event: AstrMessageEvent):
        '''
        监听消息并匹配自定义回复
        '''
        # 获取消息纯文本并去除首尾空格
        message = event.message_obj.message_str.strip()

        # 检查是否命中关键字
        if message in self.reply_map:
            # 关键：停止事件传播，拦截 LLM 和其他插件
            event.stop_event()
            
            # 获取对应的回复内容
            reply_content = self.reply_map[message]
            
            # 返回结果
            yield event.plain_result(reply_content)

    @event_filter.on_config_loaded()
    async def on_config_updated(self, event: AstrMessageEvent):
        '''
        当在 WebUI 修改配置后，实时更新插件内的回复映射
        '''
        self.reply_map = self.config.get("replies", {"1": "2"})
