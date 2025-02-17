"""
https://kq4b3vgg5b.feishu.cn/wiki/NaUDwDa6QiRfOCkRP9pcmUydnYb

使用 LangGraph 构建图 和 ToolNode 构建节点

Tool Calling Agent（工具调用代理）是LangGraph支持的一种AI Agent代理架构。这个代理架构是在Router Agent的基础上，大模型可以自主选择并使用多种工具来完成某个条件分支中的任务。 当我们希望代理与外部系统交互时，工具就非常有用。外部系统（例如API）通常需要特定的输入模式，而不是自然语言。例如，当我们绑定 API 作为工具时，我们赋予大模型对所需输入模式的感知，大模型就能根据用户的自然语言输入选择调用工具，并将返回符合该工具架构的输出。

经过ToolNode工具后，其返回的是一个LangChain Runnable对象，会将图形状态（带有消息列表）作为输入并输出状态更新以及工具调用的结果，通过这种设计去适配LangGraph中其他的功能组件。比如我们LangGraph预构建的更高级AI Agent架构 - ReAct，两者搭配起来可以开箱即用，同时通过ToolNode构建的工具对象也能与任何StateGraph一起使用。由此，对于ToolNode的使用，有三个必要的点需要满足，即：
1. 状态必须包含消息列表。
2. 最后一条消息必须是AIMessage。
3. AIMessage必须填充tool_calls。

LangGraph ToolNode 源码：https://langchain-ai.github.io/langgraph/reference/prebuilt/#langgraph.prebuilt.tool_node.ToolNode

# 通过 函数注释 让大模型知道什么时候来调用工具
"""
from langchain_core.tools import tool
from langgraph.prebuilt import ToolNode

# 添加注解，定义Tool
@tool
def get_weather(location):
    """Call to get the current weather."""
    if location.lower() in ["beijing"]:
        return "北京的温度是16度，天气晴朗。"
    elif location.lower() in ["shanghai"]:
        return "上海的温度是20度，部分多云。"
    else:
        return "不好意思，并未查询到具体的天气信息。"
    
tools = [get_weather]
tool_node = ToolNode(tools)
print(tool_node)

# 测试
from langchain_core.messages import AIMessage

message_with_single_tool_call = AIMessage(
    content="",
    tool_calls=[
        {
            "name": "get_weather",
            "args": {"location": "beijing"},
            "id": "tool_call_id_2",
            "type": "tool_call",
        },
        {
            "name": "get_weather",
            "args": {"location": "shanghai"},
            "id": "tool_call_id_2",
            "type": "tool_call",
        },
        {
            "name": "get_weather",
            "args": {"location": "kk"},
            "id": "tool_call_id_2",
            "type": "tool_call",
        }
    ],
)

result = tool_node.invoke({"messages": [message_with_single_tool_call]})

for res in result["messages"]:
    print(res.content)
    
# print(result["messages"][-1].content)
