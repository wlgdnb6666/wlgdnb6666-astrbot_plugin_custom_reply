from astrbot.api.all import *

class CustomReplyPlugin(Star):
    # 给 config 设为 None 作为默认值，这样无论传 1 个还是 2 个参数都不会报错
    def __init__(self, context: Context, config: dict = None):
        super().__init__(context)
        
        # 兼容性获取配置：如果传入了 config 就用，没有就去 context 里找
        if config is not None:
            self.config = config
        else:
            self.config = getattr(self.context, "config", {})
            
        # 初始化回复映射
        self.reply_map = self.config.get("replies", {"1": "2"})

    # 使用 handle_event 确保最高级别的事件拦截
    async def handle_event(self, event: AstrMessageEvent):
        # 确认是消息事件
        if not isinstance(event, AstrMessageEvent):
            return

        # 获取消息纯文本
        message = event.message_obj.message_str.strip()

        # 检查是否匹配自定义回复字典
        if message in self.reply_map:
            # 停止事件传播：这会拦截 LLM 大模型和其他插件的回复
            event.stop_event()
            
            # 获取对应的回复内容
            reply_content = self.reply_map[message]
            
            # 发送结果
            yield event.plain_result(reply_content)

    # 监听配置加载，支持 WebUI 热重载
    async def on_config_loaded(self):
        self.reply_map = self.config.get("replies", {"1": "2"})
