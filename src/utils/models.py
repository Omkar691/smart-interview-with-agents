from langchain_groq import ChatGroq
from langchain.chat_models import init_chat_model

from dotenv import load_dotenv

load_dotenv()



llm=ChatGroq(model="openai/gpt-oss-120b",
             temperature=0)



