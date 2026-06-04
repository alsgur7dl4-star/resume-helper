# day4_self1_resume_agents.py
"""Day 4 self1: 자소서 분석 Agent와 Triage 라우팅 첫 골격.

오늘 범위:
- analyze_agent 1개 (ResumeAnalysis 5필드 + 6대 결함 점검)
- triage_agent 1개 (분석 요청만 analyze_agent로 handoff)
- 라우팅 테스트 2개 (분석 요청 / 범위 밖 요청)
- Runner.run() 실행 로그에서 last_agent 확인

첨삭 Agent, 최종본 Agent, Guardrails는 day4-self2 범위입니다.
API 키 원문과 자소서 개인정보는 코드와 로그에 출력하지 않습니다.
"""

import os
import asyncio

from dotenv import load_dotenv

from agents import Agent, Runner

load_dotenv()


def check_env() -> None:
    """OPENAI_API_KEY 존재 여부만 확인한다. 키 원문은 출력하지 않는다."""
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        print("OPENAI_API_KEY 로딩 확인")
    else:
        print("OPENAI_API_KEY를 .env에 먼저 넣어주세요")


analyze_agent = Agent(
    name="ResumeAnalyzeAgent",
    handoff_description=(
        "자소서 분석 요청을 맡아요. "
        "ResumeAnalysis 5필드로 정리하고 6대 결함 탐지 후 결함 태그를 남겨요."
    ),
    instructions="""
당신은 자소서를 분석하는 Specialist입니다.

분석 기준(ResumeAnalysis 5필드):
- 성장: 성장 과정에서 직무와 연결되는 단서를 확인해요.
- 동기: 지원 동기에서 회사 또는 직무와 연결되는 이유를 확인해요.
- 포부: 입사 후 포부와 향후 기여 방향을 확인해요.
- 경험: 직무 관련 경험, 역할, 행동, 결과 단서를 확인해요.
- 성공실패: 성공 또는 실패 경험과 거기서 배운 점을 확인해요.

결함 점검(6대 결함):
- 추상적 표현: 구체성 없이 두루뭉술한 표현을 결함 태그로 남겨요.
- 수치 부재: 정량 근거나 수치가 빠진 부분을 결함 태그로 남겨요.
- 복붙 흔적: 회사·직무와 무관하게 재사용된 듯한 문장을 결함 태그로 남겨요.
- 직무 불일치: 지원 직무와 어긋나는 경험이나 주장을 결함 태그로 남겨요.
- NCS 미반영: 직무 NCS 키워드가 반영되지 않은 부분을 결함 태그로 남겨요.
- 블라인드 위반: 실명, 학교명, 주소, 연락처 같은 개인정보 노출을 결함 태그로 남겨요.

출력은 짧은 분석 요약과 결함 태그 중심으로 작성해요.
첨삭 문장 전체 재작성과 최종본 작성은 다음 시간 범위이므로 하지 않아요.
""",
)


triage_agent = Agent(
    name="ResumeTriageAgent",
    instructions="""
당신은 자소서 도우미의 접수 담당입니다.

규칙:
- 사용자가 자소서 분석, ResumeAnalysis, 결함 탐지를 요청하면 분석 Agent로 넘겨요.
- 오늘 범위 밖의 첨삭, 최종본, Guardrails 요청은 다음 시간에 다룬다고 짧게 안내해요.
- 날씨, 잡담, 일반 검색처럼 자소서와 관련 없는 요청은 범위 밖이라고 안내해요.
- 직접 긴 분석을 작성하지 말고 적합한 Specialist를 선택해요.
""",
    handoffs=[analyze_agent],
)


TEST_CASES = [
    {
        "label": "분석 요청",
        "input": """
아래 자소서를 ResumeAnalysis 5필드 기준으로 분석해줘.
저는 팀 프로젝트에서 로그인 API 오류를 정리했고,
재발 방지를 위해 오류 메시지와 테스트 케이스를 문서화했습니다.
""",
    },
    {
        "label": "범위 밖 요청",
        "input": "오늘 서울 날씨 알려주고 점심 메뉴도 추천해줘.",
    },
]


async def run_case(label: str, user_input: str) -> None:
    """Triage를 실행하고 라벨, 마지막 Agent 이름, 짧은 출력만 확인한다."""
    print(f"\n--- {label} ---")

    result = await Runner.run(triage_agent, input=user_input)

    print("last_agent:", result.last_agent.name)
    print("output:", str(result.final_output)[:200])


async def main() -> None:
    """TEST_CASES를 순회하며 라우팅 결과를 확인한다."""
    for case in TEST_CASES:
        await run_case(case["label"], case["input"])


if __name__ == "__main__":
    check_env()
    asyncio.run(main())
