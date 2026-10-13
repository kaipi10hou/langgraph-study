from typing import TypedDict
from langgraph.graph import StateGraph, START, END


# 1. 그래프가 들고 다닐 데이터
class State(TypedDict):
	language: str
	message: str

# 언어 확인
def check_language(state: State):
	print("check_language 실행:", state)
	return {}

# 한국어 처리
def korean(state: State):
	print("korean 실행:", state)

	return {
		"message": "안녕하세요 Isaac"
	}

# 영어 처리
def english(state: State):
	print("english 실행: ", state)

	return {
		"message": "Hello Isaac"
	}

def select_language(state: State):
	if state["language"] == "ko":
		return "korean"

	return "english"


# 그래프 만들기
builder = StateGraph(State)

builder.add_node("check_language", check_language)
builder.add_node("korean", korean)
builder.add_node("english", english)


# 5. 실행 순서 연결
builder.add_edge(START, "check_language")

builder.add_conditional_edges(
	"check_language",
	select_language
)


builder.add_edge("korean", END)
builder.add_edge("english", END)


# 6. 실행 가능한 그래프로 만들기
graph = builder.compile()


# 7. 실행
result = graph.invoke({
    "language": "ko",
	"message": ""
})

print("최종 결과:", result)