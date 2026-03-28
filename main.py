from astrbot.api.all import *

class CustomReplyPlugin(Star):
    # 强制给类定义一个默认 config，防止实例化时报错缺失参数
    config: dict = {}

    # 这里不写 __init__，让它直接去撞父类的逻辑
    
    async def on_load(self):
        """
        插件载入时的生命周期钩子
        """
        # 兼容性获取配置
        self.config_data = getattr(self, "config", getattr(self.context, "config", {}))
        # 如果还是拿不到，就从 context 里直接掏
        if not self.config_data:
            self.config_data = self.context.config
            
        self.reply_map = self.config_data.get("replies", {"1": "2"})

    async def handle_event(self, event: AstrMessageEvent):
        """
        底层事件监听
        """
        if not isinstance(event, AstrMessageEvent):
            return

        # 获取消息纯文本
        message = event.message_obj.message_str.strip()

        # 初始化检查
        if not hasattr(self, 'reply_map'):
            await self.on_load()

        # 匹配回复字典
        if message in self.reply_map:
            # 停止事件传播，拦截 LLM
            event.stop_event()
            
            # 发送结果
            reply_content = self.reply_map[message]
            yield event.plain_result(reply_content)

    async def on_config_loaded(self):
        """
        配置更新钩子
        """
        await self.on_load()
