import os

from dotenv import load_dotenv
from openai import OpenAI
from anthropic import Anthropic

from styles import STYLE_PRESETS, list_style_names


RESUME_SYSTEM_PROMPT = """당신은 한국 채용 맥락을 깊이 이해하는 자소서(자기소개서) 첨삭 전문가입니다.

[역할]
지원자가 제출한 자소서를 읽고, 채용 담당자 관점에서 구체적이고 실행 가능한 피드백을 제공합니다.

[한국 자소서 구조 이해]
- 한국 기업 자소서는 보통 3~5개 문항으로 구성됩니다.
  (예: 지원 동기, 성장 과정, 직무 역량/강점, 입사 후 포부, 협업/갈등 경험 등)
- 각 문항은 글자 수 제한이 있는 경우가 많으므로 간결함과 핵심 전달을 중시합니다.

[자주 나타나는 결함 패턴 — 최소 2~3개를 점검]
1. 추상적이고 모호한 표현 (예: "최선을 다했습니다", "열정이 있습니다")만 있고 근거가 없음
2. 회사/직무와 무관한 자기 자랑 나열
3. 두괄식이 아니라 결론이 맨 뒤에 묻혀 있음
4. 정량적 성과(숫자, 기간, 규모)가 없어 설득력이 약함
5. 추상적 다짐만 있고 구체적 행동/기여 계획이 없음
6. 문장이 길고 수동태/번역투가 많아 가독성이 떨어짐

[NCS 역량 관점]
- 직무 관련성, 문제 해결 능력, 의사소통 능력, 조직 이해 능력, 자기개발 능력 관점에서 자소서 내용을 점검합니다.

[추천 글쓰기 프레임워크 — 최소 1개를 활용해 첨삭 제안]
- STAR: Situation(상황) → Task(과제) → Action(행동) → Result(결과)
- PREP: Point(결론) → Reason(이유) → Example(예시) → Point(재강조)
- CAR: Context(맥락) → Action(행동) → Result(결과)

[블라인드 채용 주의 — 개인정보 노출 경계]
- 다음과 같은 정보는 블라인드 채용에서 불이익이나 편향을 줄 수 있으므로 빼도록 안내합니다.
  (예: 출신 학교명, 학점, 거주 지역, 가족 구성/직업, 나이, 성별, 사진, 출신지)

[출력 방식]
- 먼저 잘된 점 1~2가지를 짚고, 이어서 개선이 필요한 부분을 우선순위 순으로 제시합니다.
- 가능하면 "이렇게 고치면 좋습니다"라는 구체적 수정 예시를 함께 제안합니다.
- 친절하지만 솔직하게, 한국어로 답변합니다.
"""


def load_settings() -> dict[str, bool]:
    load_dotenv()
    return {
        "openai_key_exists": bool(os.getenv("OPENAI_API_KEY")),
        "anthropic_key_exists": bool(os.getenv("ANTHROPIC_API_KEY")),
    }


def make_openai_client() -> OpenAI:
    return OpenAI()


def make_claude_client() -> Anthropic:
    return Anthropic()


def get_sample_resume() -> str:
    return (
        "[지원 동기]\n"
        "저는 Java 기반 웹 개발 경험을 바탕으로 안정적인 서비스를 만드는 개발자로 성장하고 싶습니다. "
        "SI 인턴 과정에서 Java를 사용하며 실무 개발 흐름을 경험했고, "
        "프로젝트에서는 Spring Boot, React, Node.js, MySQL 등을 활용해 웹 서비스 기능을 구현했습니다. "
        "현재는 MCP 서비스 개발자 교육과정을 통해 AI 서비스와 백엔드 개발 역량을 함께 확장하고 있습니다.\n\n"
        "[직무 역량]\n"
        "프로젝트에서 결제, 장바구니, 쿠폰, 마일리지, 회원가입, 로그인, 소셜 로그인, JWT 기반 인증 기능을 구현한 경험이 있습니다. "
        "또한 팀 프로젝트 과정에서 개발 환경 문제와 역할 분담 문제를 조율하며 협업의 중요성을 배웠습니다. "
        "앞으로도 Java와 웹 개발 경험을 기반으로 API 설계, 인증·보안, 배포 자동화 역량을 강화해 실무에 기여하는 개발자가 되고 싶습니다."
    )


def ask_openai_once(sample_text: str) -> str:
    client = make_openai_client()
    model = os.getenv("MODEL_OPENAI", "gpt-5-mini")
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": RESUME_SYSTEM_PROMPT},
            {"role": "user", "content": sample_text},
        ],
        max_completion_tokens=4096,
        reasoning_effort="minimal",
    )

    return response.choices[0].message.content or ""


def ask_claude_once(sample_text: str) -> str:
    client = make_claude_client()
    model = os.getenv("MODEL_CLAUDE", "claude-sonnet-4-5")
    message = client.messages.create(
        model=model,
        system=RESUME_SYSTEM_PROMPT,
        max_tokens=1024,
        messages=[
            {"role": "user", "content": sample_text},
        ],
    )
    return message.content[0].text


def print_help() -> None:
    print("=== 도움말 ===")
    print(
        "- 자소서 내용을 입력하면 현재 선택된 스타일 기준으로 첨삭 피드백을 받습니다."
    )
    print("- /help : 도움말을 출력합니다.")
    print("- /style : 현재 스타일과 사용 가능한 스타일 목록을 출력합니다.")
    print("- /style 간결형 : 짧고 명료하게 첨삭합니다.")
    print("- /style 스토리형 : 경험을 이야기 흐름으로 정리합니다.")
    print("- /style 직무맞춤형 : 지원 직무와의 연결성을 중심으로 첨삭합니다.")
    print("- /style 친근한 버전 : 문장을 부드럽고 자연스럽게 다듬습니다.")
    print("- /style AI 서비스 연결형 : 웹 개발 경험을 MCP·AI 서비스 역량과 연결합니다.")
    print("- /quit : 대화를 종료합니다.")
    print(
        "- 이름, 연락처, 학교명, 가족 정보, 회사 내부 정보 등 개인정보는 입력하지 마세요."
    )
    print("- .env와 자소서 원문 파일은 GitHub에 올리지 마세요.")


def handle_style_command(user_input: str, current_style_key: str) -> str:
    parts = user_input.split(maxsplit=1)
    requested = parts[1].strip() if len(parts) > 1 else ""

    if not requested:
        print("현재 스타일:", current_style_key)
        print("사용 가능한 스타일:", list_style_names())
        print("사용법: /style 간결형")
        return current_style_key

    if requested in STYLE_PRESETS:
        print(f"스타일을 '{requested}'(으)로 변경했습니다.")
        return requested

    print(f"알 수 없는 스타일입니다: {requested}")
    print("사용 가능한 스타일:", list_style_names())
    return current_style_key


def chat_loop() -> None:
    settings = load_settings()
    print("OpenAI 키 존재 여부:", settings["openai_key_exists"])
    print("자소서 첨삭 도우미입니다. /help 로 사용법을 확인하세요.")

    client = make_openai_client()
    model = os.getenv("MODEL_OPENAI", "gpt-5.4-nano")
    current_style_key = "간결형"

    while True:
        user_input = input("자소서 입력 > ").strip()

        if user_input == "/help":
            print_help()
            continue

        if user_input == "/quit":
            print("대화를 종료합니다. 수고하셨습니다.")
            break

        if user_input == "/style" or user_input.startswith("/style "):
            current_style_key = handle_style_command(user_input, current_style_key)
            continue

        if not user_input:
            print("내용을 입력해 주세요. (/help 도움말, /quit 종료)")
            continue

        messages = [
            {"role": "system", "content": STYLE_PRESETS[current_style_key]["system"]},
            {"role": "user", "content": user_input},
        ]

        response = client.chat.completions.create(
            model=model,
            max_completion_tokens=700,
            messages=messages,
        )
        answer = response.choices[0].message.content
        print(answer)


def main() -> None:
    settings = load_settings()
    print("OpenAI 키 존재 여부:", settings["openai_key_exists"])
    print("Anthropic 키 존재 여부:", settings["anthropic_key_exists"])

    sample_text = get_sample_resume()

    provider = input("사용할 제공사를 입력하세요 (openai/claude): ").strip().lower()

    if provider == "openai":
        result = ask_openai_once(sample_text)
    elif provider == "claude":
        result = ask_claude_once(sample_text)
    else:
        print("openai 또는 claude 중 하나를 입력해요.")
        return

    print("\n=== 첨삭 결과 (앞부분) ===")
    print(result[:500])


if __name__ == "__main__":
    chat_loop()
