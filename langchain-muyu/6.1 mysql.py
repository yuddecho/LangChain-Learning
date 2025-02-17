# https://hub.docker.com/_/mysql
# docker pull mysql:latest
# docker run --name mysql -p 3306:3306 -e MYSQL_ROOT_PASSWORD=root -d mysql:latest
# docker run --name mysql -p 3306:3306 -v c:\Users\ydduo\Desktop\zhiyaoyuanchuang\dev-summary\python\zhipuai\sql:/var/lib/mysql -e MYSQL_ROOT_PASSWORD=root -d mysql:latest

# pip install pymysql

import pymysql

def create_and_populate_mysql():
    # 连接到MySQL服务器（未指定数据库）
    conn_mysql = pymysql.connect(
        host='localhost',         # 这里替换成你自己的 MySQL 主机地址
        user='root',              # 这里替换成你自己的用户名
        password='root',          # 这里替换成你自己的密码
        charset='utf8mb4'         # 字符集
    )
    cursor_mysql = conn_mysql.cursor()

    # 创建数据库 education_db（如果不存在）
    cursor_mysql.execute("CREATE DATABASE IF NOT EXISTS education_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")

    # 切换到 education_db 数据库
    cursor_mysql.execute('USE education_db;')

    # 创建课程信息表
    create_courses_table_query = '''
    CREATE TABLE IF NOT EXISTS courses (
        course_id VARCHAR(20),                  -- 课程ID
        course_name VARCHAR(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,  -- 课程名称
        course_category VARCHAR(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,  -- 课程类别
        chapter_number INT,                      -- 章节编号
        chapter_name VARCHAR(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,  -- 章节名称
        duration INT,                            -- 课程时长（小时）
        keywords VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,   -- 关键词
        PRIMARY KEY (course_id, chapter_number)   -- 组合主键（课程ID + 章节编号）
    );
    '''
    cursor_mysql.execute(create_courses_table_query)

    # 插入示例数据
    insert_data_query = '''
    INSERT INTO courses (course_id, course_name, course_category, chapter_number, chapter_name, duration, keywords)
    VALUES
    ('ML001', '机器学习基础', '机器学习', 1, '机器学习简介', 4, '监督学习,无监督学习'),
    ('ML001', '机器学习基础', '机器学习', 2, '线性回归', 6, '回归分析,模型训练'),
    ('DL001', '深度学习概论', '深度学习', 1, '神经网络基础', 5, '神经网络,激活函数'),
    ('DL001', '深度学习概论', '深度学习', 2, '卷积神经网络', 6, 'CNN,图像识别'),
    ('LM001', '大模型智能体开发', '大模型智能体开发', 1, '智能体基础', 5, 'Agent,FunctionCalling'),
    ('LM001', '大模型智能体开发', '大模型智能体开发', 2, '本地知识库问答', 7, 'RAG,VectorStore'),
    ('MLP001', '大模型原理', '大模型原理', 1, '大模型概念', 4, '大模型,计算资源'),
    ('MLP001', '大模型原理', '大模型原理', 2, '大规模训练', 6, '分布式训练,并行计算'),
    ('CI001', '因果推断导论', '因果推断', 1, '因果关系与相关性', 5, '因果推断,回归分析'),
    ('CI001', '因果推断导论', '因果推断', 2, '随机化实验设计', 5, '实验设计,干预实验');
    '''
    try:
        cursor_mysql.execute(insert_data_query)
        conn_mysql.commit()  # 提交事务
        print("数据插入成功！")
    except pymysql.MySQLError as e:
        print(f"插入数据时出错：{e}")
        conn_mysql.rollback()  # 回滚事务

    # 提交更改并关闭连接
    conn_mysql.close()

def query_by_keyword(keyword):
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

# 调用函数创建数据库并插入数据
# create_and_populate_mysql()

print(query_by_keyword("Agent"))
