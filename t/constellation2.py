import httpx
import json
from langchain_openai import ChatOpenAI
import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts import MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
import time

def get_ali_api(star, needMonth=0, needWeek=0, needTomorrow=0, needYear=0):
    host = 'https://ali-star-lucky.showapi.com'
    path = '/star'
    appcode = '6685c9f6da73471dba8f2e0e6dc0f27c'
    
    # 动态构建查询字符串
    querys = f'needMonth={needMonth}&star={star}&needWeek={needWeek}&needTomorrow={needTomorrow}&needYear={needYear}'
    url = f'{host}{path}?{querys}'

    headers = {
        'Authorization': f'APPCODE {appcode}'
    }

    response = httpx.get(url, headers=headers, verify=False)
    print("Status code:", response.status_code)

    if response.status_code == 200:
        json_content = response.json()
        formatted_json = json.dumps(json_content, ensure_ascii=False, indent=4)
        return formatted_json
    else:
        return f"请求失败，状态码: {response.status_code}"

#print(get_ali_api())
from dotenv import load_dotenv,find_dotenv
_ = load_dotenv(find_dotenv())

store = {}
def get_session_history(session_id:str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

llm = ChatOpenAI(
    base_url="http://api.baichuan-ai.com/v1",
    api_key=os.environ["BAICHUAN_API_KEY"],
    model="Baichuan4",
)

prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system",'''如果我输入“开始运势测试”，你应该输出下面这段话：“请使用拼音给我你的星座，并且告诉我你要预测本年、本月、本周、明天中的哪些运势。”
         接下来，你要根据我给出的星座（star），以及是否需要预测本年（needYear）、本月（needMonth）、本周（needWeek）、明天（needTomorrow）
         来调用get_ali_api(star, needMonth=0, needWeek=0, needTomorrow=0, needYear=0)这个函数来获得答案，并把这个答案整合成一段通顺且完整的话。'''),
        MessagesPlaceholder(variable_name="history"),
        ("user", '''{question}''')
    ]
)
chat_chain = prompt_template | llm

chain = RunnableWithMessageHistory(
    chat_chain,
    get_session_history,
    input_messages_key="question",
    history_messages_key="history"
)

config = {
    "configurable":{
        "session_id":time.time(),
    }
}
""" response = chat_chain.invoke({"question":"baiyang"})
print(response) """