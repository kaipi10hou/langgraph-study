from typing import TypedDict
from langgraph.graph import StateGraph, START, END


# 1. 그래프가 들고 다닐 데이터
class State(TypedDict):
    message: str


# 2. 첫 번째 작업
def hello(state: State):
    print("hello 실행:", state)

    return {
        "message": "안녕하세요"
    }


# 3. 두 번째 작업
def add_name(state: State):
    print("add_name 실행:", state)

    return {
        "message": state["message"] + " Isaac!"
    }


# 4. 그래프 만들기
builder = StateGraph(State)

builder.add_node("hello", hello)
builder.add_node("add_name", add_name)


# 5. 실행 순서 연결
builder.add_edge(START, "hello")
builder.add_edge("hello", "add_name")
builder.add_edge("add_name", END)


# 6. 실행 가능한 그래프로 만들기
graph = builder.compile()


# 7. 실행
result = graph.invoke({
    "message": ""
})

print("최종 결과:", result)