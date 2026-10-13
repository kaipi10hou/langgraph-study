import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-3.8-flash",
    api_key=os.environ["GOOGLE_API_KEY"]
)

response = llm.invoke("LangGraph가 무엇인지 한 문장으로 설명해줘.")

print(response.content)