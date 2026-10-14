import os
from typing import TypedDict

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, START, END

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash",
    api_key=os.environ["GOOGLE_API_KEY"]
)

class State(TypedDict):
    question: str
    category: str
    answer: str

def classify_question(state: State):
    print("1. 질문 분류 시작")

    prompt = f"""
    다음 고객 문의를 분류해주세요.
    
    분류 기준:
    - 배송, 주문, 택배 관련 문의: delivery
    - 상품 정보, 색상, 가격 관련 문의: product

    반드시 delivery 또는 product 중 하나만 출력하세요.
    
    고객 문의: {state["question"]}
    """

    response = llm.invoke(prompt)

    print("응답 타입", type(response.content))
    print("응답 내용", response.content)

    category = response.text.strip()

    print("Gemini 분류 결과: ", category)

    return {"category": category}

def handle_delivery(state: State):
    print("2. 배송 문의 처리")

    return {
        "answer": "배송 문의입니다. 주문번호를 알려주시면 배송 상태를 확인하겠습니다."
    }

def handle_product(state: State):
    print("2. 상품 문의 처리")

    return {
        "answer": "상품 문의입니다. 어떤 상품이 궁금하신가요?"
    }

def select_route(state: State):
    if state["category"] == "delivery":
        return "handle_delivery"
    return "handle_product"

builder = StateGraph(State)

builder.add_node("classify_question", classify_question)
builder.add_node("handle_delivery", handle_delivery)
builder.add_node("handle_product", handle_product)

builder.add_edge(START, "classify_question")

builder.add_conditional_edges(
    "classify_question",
    select_route
)

builder.add_edge("handle_delivery", END)
builder.add_edge("handle_product", END)

graph = builder.compile()

result = graph.invoke({
    "question": "주문한 상품은 언제 배송되나요?",
    "category": "",
    "answer": ""
})

print("최종 결과: ", result)


