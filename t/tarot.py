
from langchain_core.documents import Document
from dotenv import load_dotenv,find_dotenv
import os 
from langchain_openai import ChatOpenAI
from langchain_community.embeddings import BaichuanTextEmbeddings
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
import time
from langchain.chains import create_history_aware_retriever,create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
import random

store = {}
def get_session_history(session_id:str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

documents = [
    Document(
        id='1',
        title='体育教练',
        page_content="体育教练是教体育的",
        category='人物',
        subcategory='人物称谓',
        initial='T'
    ),
    Document(
        id='2',
        title='贵人',
        page_content="贵人是帮助你的人",
        category='人物',
        subcategory='人物称谓',
        initial='G'
    ),
    Document(
        id='3',
        title='贵族',
        page_content="贵族是社会地位高的人",
        category='人物',
        subcategory='人物称谓',
        initial='G'
    ),
    Document(
        id='4',
        title='缺席的人',
        page_content="缺席的人是没来的人",
        category='人物',
        subcategory='人物称谓',
        initial='Q'
    ),
]

_ = load_dotenv(find_dotenv())

embeddings = BaichuanTextEmbeddings(baichuan_api_key=os.environ["BAICHUAN_API_KEY"])
#向量库
vectorstore = Chroma.from_documents(
    documents,
    embedding=embeddings,
)

retriever = vectorstore.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 1},
) # select top result

llm = ChatOpenAI(
    base_url="http://api.baichuan-ai.com/v1",
    api_key=os.environ["BAICHUAN_API_KEY"],
    model="Baichuan4",
)

# httpx
contextualize_q_system_prompt = (
    "根据聊天记录及用户最新的问题"
    "该问题可能涉及聊天记录中的上下文信息，重新构思一个独立的问题，"
    "使其能够在不参考聊天历史的情况下被理解。"
    "不要直接回答问题，而是在需要时对其进行重新表述，否则直接按原样返回问题。"
)

contextualize_q_prompt = ChatPromptTemplate.from_messages([
    ("system",contextualize_q_system_prompt),
    MessagesPlaceholder("chat_history"),
    ("human","{input}")
])
history_aware_retriever = create_history_aware_retriever(llm,retriever,contextualize_q_prompt)

### 回答问题 ###
qa_prompt = ChatPromptTemplate.from_messages([
    ("system",'''仅使用提供的上下文来回答这个问题。
            上下文语境:
            {context}
            
            如果我说：“开始测试”，你应该说：“请在1至78里选一个数字。”
                我接下来会输入一个数字，如果这个数字不在1至78的范围里，你应该说：“你输入的数字不在1至78的范围里，应该再输入一次。”
                直到我输入一个在1至78范围内的数字。你才要做接下来的事情：
                你在1至78里随机抽一个数字并从文档里找到这个id对应的page_content。
                你的回答应该以如下语句开始：“这个编号对应的内容是：”
                '''),
    MessagesPlaceholder("chat_history"),
    ("human","{input}")
])
question_answer_chain = create_stuff_documents_chain(llm,qa_prompt)
chat_chain = create_retrieval_chain(history_aware_retriever,question_answer_chain)


# prompt = ChatPromptTemplate.from_messages(
#     [
#         ("system",'''仅使用提供的上下文来回答这个问题。
#                     上下文语境:
#                     {context}
                    
#                     如果我说：“开始测试”，你应该说：“请在1至78里选一个数字。”
#                      我接下来会输入一个数字，如果这个数字不在1至78的范围里，你应该说：“你输入的数字不在1至78的范围里，应该再输入一次。”
#                      直到我输入一个在1至78范围内的数字。你才要做接下来的事情：
#                      你在1至78里随机抽一个数字并输出。
#                      你应该直接输出数字，而不要说别的话。'''),
#         MessagesPlaceholder(variable_name="history"),
#         ("human", "{question}")
#     ]
# )

# chat_chain = {"context": retriever, "question": RunnablePassthrough()} | prompt | llm

chain = RunnableWithMessageHistory(
    chat_chain,
    get_session_history,
    input_messages_key="input",
    history_messages_key="chat_history"
    
)

config = {
    "configurable":{
        "session_id":time.time(),
    }
}




""" response = chain.invoke( {"input":"告诉我关于贵族的事。"},config=config)

print(response)  """


