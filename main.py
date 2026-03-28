from astrbot.api.all import *

# 注册插件：请将 repo_url 替换为你自己的 GitHub 仓库地址
@register("custom_reply", "YourName", "自定义精确匹配回复并拦截 LLM 的插件", "1.0.0", "https://github.com/yourusername/astrbot_plugin_custom_reply")
class CustomReplyPlugin(Star):
    def __init__(self, context: Context, config: dict):
        super().__init__(context)
        self.config = config
        # 从 config.json 读取自定义回复映射，如果为空则提供一个默认示例
        self.reply_map = self.config.get("replies", {"1": "2"})

    @filter.on_message()
    async def on_message(self, event: AstrMessageEvent):
        # 获取用户发送的纯文本消息，并去除首尾空格
        user_text = event.message_obj.message_str.strip()
        
        # 检查用户发送的内容是否在我们的自定义回复字典中
        if user_text in self.reply_map:
            # 核心机制：停止事件传播，阻止 LLM 和其他优先级较低的插件处理此消息
            event.stop_event()
            
            # 获取对应的回复内容
            reply_text = self.reply_map[user_text]
            
            # 发送自定义回复
            yield event.plain_result(reply_text)

