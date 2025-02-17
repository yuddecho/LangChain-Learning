"""
https://kq4b3vgg5b.feishu.cn/wiki/NaUDwDa6QiRfOCkRP9pcmUydnYb

使用 LangGraph 构建图

"""
from typing import Annotated
from langgraph.graph import StateGraph
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages

class State(TypedDict):
    messages: Annotated[list, add_messages]

#  LangGraph 中的 StateGraph类，这个类允许我们创建图，其节点通过读取和写入共享状态进行通信。 StateGraph 类由开发者定义的 State 对象进行参数化，该对象表示图中的节点将通过其进行通信的共享数据结构。
graph_builder = StateGraph(State)

# LLM 
from langchain_openai import ChatOpenAI

model = ChatOpenAI(
    temperature=0.95,
    model="glm-4",
    openai_api_key="9a523c8b1e8145bcb9755a876611b372.mEg9L0BVnBsAHytk11",
    openai_api_base="https://open.bigmodel.cn/api/paas/v4/"
)

# 对话节点
def chatbot(state: State):
    # print(state)
    return {"messages": [model.invoke(state["messages"])]}

# 定义图
# 添加节点并编译图。同样，我们先看普通边。如果直接想从节点A到节点B，可以直接使用add_edge方法。注意：LangGraph有两个特殊的节点：START和END。START表示将用户输入发送到图的节点。使用该节点的主要目的是确定应该首先调用哪些节点。END节点是代表终端节点的特殊节点。当想要指示哪些边完成后没有任何操作时，将使用该节点。因此，一个完整的图就可以使用如下代码进行定义：
from langgraph.graph import START, END

# 添加自定义节点
graph_builder.add_node("chatbot", chatbot)

# 构建边
graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)

# 当通过 builder.compile() 方法编译图后，编译后的 graph 对象提供了 invoke 方法，该方法用于启动图的执行。我们可以通过 invoke 方法传递一个初始状态，这个状态将作为图执行的起始输入
# 编译图
graph = graph_builder.compile()

# 可视化图
from langchain_core.runnables.graph import MermaidDrawMethod

# # 使用 Mermaid.Ink API 渲染 PNG 图像
png_data = graph.get_graph().draw_mermaid_png(draw_method=MermaidDrawMethod.API)

# # 保存为文件
with open("graph.png", "wb") as f:
    f.write(png_data)

# 测试
input_message = {"messages": ["你好，请你介绍一下你自己"]}

result = graph.invoke(input_message)
# print(result)
print(result["messages"][-1].content)

# 构建一个交互机器人
def stream_graph_updates(user_input: str):  
    for event in graph.stream({"messages": [("user", user_input)]}):
        for value in event.values():
            print("模型回复:", value["messages"][-1].content)


while True:
    try:
        user_input = input("用户提问: ")
        if user_input.lower() in ["退出"]:
            print("下次再见！")
            break

        stream_graph_updates(user_input)
    except:
        break