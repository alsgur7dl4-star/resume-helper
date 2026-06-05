# day5_self1_resume_pipeline.py
"""Day 5 self1: AI 1차 필터 점검과 /blind 로컬 점검 파이프라인.

오늘 범위:
- CHECK_ITEMS 3개 검증 항목
- check_resume_ai_filter: AI 1차 필터 역할의 자소서 점검 호출
- BLIND_RISK_WORDS 기반 로컬 /blind 점검 함수

API 키 원문, .env 내용, 자소서 개인정보는 코드와 로그에 출력하지 않습니다.
샘플 문장은 "샘플 지원자는..." 형태로 익명화합니다.
"""

import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()
MODEL_OPENAI = os.getenv("MODEL_OPENAI", "gpt-5.4-nano")


CHECK_ITEMS = [
    "STAR 구조 충족 여부",
    "정량 근거 포함 여부",
    "NCS 직무 키워드 밀도",
]


def check_resume_ai_filter(resume_text: str, check_items: list[str]) -> str:
    """AI 1차 필터 역할로 자소서를 점검하고 개선 권고를 반환한다.

    API 키는 코드에 직접 쓰지 않고 환경변수로 로딩한 client를 사용한다.
    """
    items_text = "\n".join(f"- {item}" for item in check_items)

    system_prompt = f"""당신은 채용 담당자에게 전달되기 전 자소서를 점검하는 AI 1차 필터 역할의 자소서 점검 도우미입니다.

아래 검증 항목을 기준으로 자소서를 점검합니다.
{items_text}

각 검증 항목별로 충족 여부를 간단히 정리하고,
마지막에 개선 권고를 1개 이상 제시합니다.
친절하지만 솔직하게, 한국어로 답변합니다.
"""

    completion = client.chat.completions.create(
        model=MODEL_OPENAI,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": resume_text},
        ],
        max_completion_tokens=700,
    )

    return completion.choices[0].message.content or ""


BLIND_RISK_WORDS = [
    "나이",
    "학교",
    "출신",
    "사진",
    "주소",
    "연락처",
    "전화번호",
    "주민등록",
    "가족",
    "부모",
]


def check_blind_risks(resume_text: str) -> list[str]:
    """자소서 본문에서 블라인드 채용 위험 단어 후보를 찾아 반환한다."""
    found: list[str] = []
    for word in BLIND_RISK_WORDS:
        if word in resume_text:
            found.append(word)
    return found


def format_blind_report(found: list[str]) -> str:
    """위험 단어 목록을 사람이 읽기 쉬운 보고 문자열로 변환한다."""
    if not found:
        return "블라인드 채용 위험 표현 후보가 발견되지 않았습니다."

    lines = ["블라인드 채용 위험 표현 후보:"]
    for word in found:
        lines.append(f"- {word}")
    return "\n".join(lines)


if __name__ == "__main__":
    sample_items = CHECK_ITEMS
    sample_text = (
        "샘플 지원자는 팀 프로젝트에서 로그인 기능 개발을 맡았고, "
        "오류 메시지와 테스트 케이스를 문서화하며 협업을 진행했습니다. "
        "샘플 지원자는 앞으로도 백엔드 개발 역량을 키우고 싶다고 작성했습니다."
    )

    print("=== AI 1차 필터 점검 결과 ===")
    print(check_resume_ai_filter(sample_text, sample_items))

    print("\n=== /blind 로컬 점검 결과 ===")
    found = check_blind_risks(sample_text)
    print(format_blind_report(found))
