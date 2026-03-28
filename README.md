# AstrBot 插件：自定义拦截回复 (Custom Reply)

这是一个为 [AstrBot](https://github.com/Soulter/AstrBot) 编写的自定义回复插件。

## 功能特性
- 精确匹配用户发送的关键字。
- 匹配成功后，自动回复预设内容。
- **拦截机制**：一旦触发自定义回复，会自动停止事件传播，**阻止 LLM（大模型）和其他插件继续响应**。

## 配置方法
安装插件后，请在 AstrBot 的 WebUI 插件管理界面中找到本插件的配置项，或者直接修改 `config.json` 文件中的 `replies` 字典：
```json
{
  "replies": {
    "1": "2",
    "触发词1": "回复词2",
  }
}

