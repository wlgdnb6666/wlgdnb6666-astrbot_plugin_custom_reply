from astrbot.api.all import *

class CustomReplyPlugin(Star):
    # 彻底不写 __init__，由父类 Star 自动处理，避开重载时的参数校验 Bug
    
    def priority(self) -> int:
        return -1 # 保持最高优先级，确保拦截 LLM

    @event_filter.on_recv_message()
    async def handle_custom_reply(self, event: AstrMessageEvent):
        # 1. 动态获取配置（兼容重载后的上下文）
        config_obj = getattr(self, "config", getattr(self.context, "config", {}))
        reply_map = config_obj.get("replies", {"1": "2"})

        # 2. 获取消息原文并清洗
        message = event.message_obj.message_str.strip()

        # 3. 排除指令形式（以 / 开头的跳过）
        if message.startswith('/'):
            return

        # 4. 匹配关键字
        if message in reply_map:
            # 停止事件传播，拦截后续插件（包括 LLM）
            event.stop_event()
            
            # 获取回复内容并 yield 发送
            reply_content = reply_map[message]
            yield event.plain_result(reply_content)

    async def on_config_loaded(self):
        """
        WebUI 配置保存后的回调
        """
        pass # 逻辑已在 handle_custom_reply 中动态处理
