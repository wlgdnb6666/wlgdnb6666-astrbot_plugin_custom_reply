from astrbot.api.all import *

@register("custom_reply", "青禾遇海", "自定义精确匹配回复并拦截 LLM 的插件", "1.0.1", "https://github.com/wlgdnb6666/wlgdnb6666-astrbot_plugin_custom_reply")
class CustomReplyPlugin(Star):
    def __init__(self, context: Context, config: dict):
        super().__init__(context)
        self.config = config
        # 从配置中读取回复映射
        self.reply_map = self.config.get("replies", {"1": "2"})

    # 关键点：将 filter 修改为 event_filter
    @event_filter.on_recv_message()
    async def on_message(self, event: AstrMessageEvent):
        # 获取用户消息并去除空格
        user_text = event.message_obj.message_str.strip()
        
        # 检查是否匹配自定义回复
        if user_text in self.reply_map:
            # 停止事件传播：这会拦截 LLM 和其他插件的响应
            event.stop_event()
            
            # 获取对应的回复内容
            reply_text = self.reply_map[user_text]
            
            # 发送结果
            yield event.plain_result(reply_text)
