from langchain_community.utilities import SQLDatabase

db = SQLDatabase.from_uri("sqlite:///zb_dream.db")
#db = SQLDatabase.from_uri("mysql+pymysql://root:040428@localhost:3306/test")
#print(db.dialect)
#print(db.get_usable_table_names())
#print(db.run("select * from zb_dream limit 10;"))

import os
from dotenv import find_dotenv,load_dotenv

_ = load_dotenv(find_dotenv())
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    base_url="http://api.baichuan-ai.com/v1",
    api_key=os.environ["BAICHUAN_API_KEY"],
    model="Baichuan4",
)
from operator import itemgetter

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool
from langchain_core.runnables import RunnablePassthrough
from langchain.chains import create_sql_query_chain
import time
answer_prompt = PromptTemplate.from_template(
    """给出以下用户问题、相应的 SQL 查询和 SQL 结果，回答用户问题。
    你要根据我连接的数据库zb_dream中的zb_dream这张表回答问题。
    你需要使用中文回答问题。
    你连接数据库和回答问题的速度要非常快。
    你只需要回答数据库中的查询结果，而不要自己编造一些答案。
    如果我的问题里有多个梦境意象，而这些意象有时候不是单纯的并列关系，你需要从一段完整的话中提炼出这些意象，
    接着，你需要把这些意象拆分开来，分别在数据库中找到对应的title，
    查找title所对应的message信息。
    比如，“梦见舅舅在当司机”这句话里有“舅舅”和“司机”两个意象，你需要对它们分别解释。
    对于其余场景，请参考上述例子举一反三。
    你不仅要对“舅舅”“司机”这些词语敏感，你也要对别的词语敏感。
    你要对查询结果的语法进行检查，使回答内容流畅易懂。

Question: {question}
SQL Query: {query}
SQL Result: {result}
Answer: """
)

execute_query = QuerySQLDataBaseTool(db=db)
write_query = create_sql_query_chain(llm,db)



chain = (
    RunnablePassthrough.assign(query=lambda x: write_query.invoke(x).split("\n")[0]).assign(
        result=itemgetter("query") | execute_query
    )
    | answer_prompt
    | llm
    | StrOutputParser()
)

# start = time.time()
print(write_query.invoke({"question": "梦见律师代表什么?"}))
# end = time.time()
# print("db duration=======>",(end-start)/1000)

print(chain.invoke({"question": "梦见律师代表什么?"}))
