import pymysql
from langchain_core.tools import tool
from langgraph.prebuilt import ToolNode


@tool
def query_by_keyword(keyword):
    """Search course details in local database according to keywords"""
    # 连接 MySQL 数据库
    conn_mysql = pymysql.connect(
        host='localhost',
        user='root',
        password='root',
        database='education_db',
        charset='utf8mb4'
    )
    cursor_mysql = conn_mysql.cursor()

    # 使用 SQL 查询按关键字查找课程。'%'符号允许部分匹配。
    cursor_mysql.execute("SELECT * FROM courses WHERE LOWER(keywords) LIKE %s", ('%' + keyword.lower() + '%',))

    # 获取所有查询到的数据
    rows = cursor_mysql.fetchall()

    # 字段说明
    field_descriptions = {
        'course_id': '课程唯一标识符',
        'course_name': '课程名称',
        'course_category': '课程所属类别',
        'chapter_number': '章节的编号',
        'chapter_name': '章节名称',
        'duration': '课程时长（小时）',
        'keywords': '与课程相关的关键词'
    }

    # 关闭连接
    conn_mysql.close()

    # 返回数据和字段说明
    return {
        'data': rows,
        'field_descriptions': field_descriptions
    }

tools = [query_by_keyword]
tool_node = ToolNode(tools)

from langchain_openai import ChatOpenAI

model = ChatOpenAI(
    temperature=0.95,
    model="glm-4",
    openai_api_key="9a523c8b1e8145bcb9755a876611b372.mEg9L0BVnBsAHytk11",
    openai_api_base="https://open.bigmodel.cn/api/paas/v4/"
)

llm = model.bind_tools(tools)

from langgraph.prebuilt import create_react_agent

graph = create_react_agent(llm, tools=tools)

# 可视化图
from langchain_core.runnables.graph import MermaidDrawMethod

# # 使用 Mermaid.Ink API 渲染 PNG 图像
png_data = graph.get_graph().draw_mermaid_png(draw_method=MermaidDrawMethod.API)

# # 保存为文件
with open("graph2.png", "wb") as f:
    f.write(png_data)

finan_response = graph.invoke({"messages":["你好，请你介绍一下你自己"]})
print(finan_response["messages"][-1].content)

finan_response = graph.invoke({"messages":["课程中有没有Agent相关的内容"]})
print(finan_response["messages"][-1].content)

# 循环
def stream_graph_updates(user_input: str):
    # 初始化一个变量来累积输出
    accumulated_output = []

    for event in graph.stream({"messages": [("user", user_input)]}):
        for value in event.values():
            # 将模型回复的内容添加到累积输出中
            accumulated_output.append(value["messages"][-1].content)

    # 返回累积的输出
    return accumulated_output

while True:
    try:
        user_input = input("用户提问: ")
        if user_input.lower() in ["退出"]:
            print("下次再见！")
            break

        # 获取累积的输出
        updates = stream_graph_updates(user_input)

        # 打印最后一个输出
        if updates:
            print("模型回复:")
            print(updates[-1])
    except:
        break