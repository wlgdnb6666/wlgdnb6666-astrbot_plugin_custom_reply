from astrbot.api.all import *

# 显式从 api.event 导入 filter，并重命名为 event_filter 以匹配下方代码
from astrbot.api.event import filter as event_filter

class CustomReplyPlugin(Star):
    def __init__(self, context: Context, config: dict):
        super().__init__(context)
        self.config = config
        # 初始化回复映射，从 config.json 读取，没有则默认为 1 -> 2
        self.reply_map = self.config.get("replies", {"1": "2"})

    @event_filter.on_recv_message()
    async def handle_custom_reply(self, event: AstrMessageEvent):
        '''
        监听消息并匹配自定义回复
        '''
        # 获取消息纯文本
        message = event.message_obj.message_str.strip()

        # 匹配关键字
        if message in self.reply_map:
            # 停止事件传播，彻底拦截 LLM 的回复
            event.stop_event()
            
            # 获取对应的回复内容
            reply_content = self.reply_map[message]
            
            # 返回结果
            yield event.plain_result(reply_content)

    @event_filter.on_config_loaded()
    async def on_config_updated(self, event: AstrMessageEvent):
        '''
        当在 WebUI 修改配置并保存后，自动更新内存中的回复表
        '''
        self.reply_map = self.config.get("replies", {"1": "2"})
