from langchain_openai import ChatOpenAI
import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts import MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
import time

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

""" # 星座和对应超链接的映射
constellation_links = {
    "双鱼座": "https://example.com/pisces",
    "巨蟹座": "https://example.com/cancer",
    "白羊座": "https://example.com/aries",
    "金牛座": "https://example.com/taurus",
    "双子座": "https://example.com/gemini",
    "狮子座": "https://example.com/leo",
    "处女座": "https://example.com/virgo",
    "天秤座": "https://example.com/libra",
    "天蝎座": "https://example.com/scorpio",
    "射手座": "https://example.com/sagittarius",
    "摩羯座": "https://example.com/capricorn",
    "水瓶座": "https://example.com/aquarius"
} """
prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system",'''你应该根据询问的星座给出一个简单的介绍。'''),
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

""" def extract_constellation(question):
    # 简单的字符串匹配方法来识别星座名
    for constellation in constellation_links.keys():
        if constellation in question:
            return constellation
    return None

def get_constellation_info(question):
    constellation_name = extract_constellation(question)
    if not constellation_name:
        return "无法识别问题中的星座名。"
    
    link = constellation_links.get(constellation_name, "https://example.com/default")
    # 将星座名和链接插入到问题中
    question_with_link = question.replace(constellation_name, f"{constellation_name} [这里]({link})")
    response = chain.invoke({"question": question_with_link})
    return response """

# 示例使用
""" question = "巨蟹座是什么意思？"  # 可以根据需要替换
response = get_constellation_info(question)
print(response) """