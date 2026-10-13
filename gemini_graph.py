import os
from typing import TypedDict

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, START, END

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-3.8-flash",
    api_key=os.environ["GOOGLE_API_KEY"]
)

class State(TypedDict):
    question: str
    answer: str


def ask_llm(state: State):
    print("ask_llm 실행: ", state)

    response = llm.invoke(state["question"])

    return {"answer": response.content}

builder = StateGraph(State)

builder.add_node("ask_llm", ask_llm)

builder.add_edge(START, "ask_llm")
builder.add_edge("ask_llm", END)

graph = builder.compile()

result = graph.invoke({
    "question": "LangGraph와 LangChain의 차이를 한 문장으로 설명해줘.",
    "answer": ""
})

print("최종결과: ", result)

