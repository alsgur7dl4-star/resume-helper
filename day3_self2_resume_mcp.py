"""Day 3 self2: /analyze 명령으로 자소서를 로컬 분석하는 도구.

실제 OpenAI/Claude API는 호출하지 않습니다.
로컬 함수와 Pydantic 검증만 사용합니다.
"""

from pathlib import Path

from pydantic import BaseModel, Field


class ResumeAnalysis(BaseModel):
    """자소서 분석 결과 5필드 스키마."""

    score: int = Field(ge=0, le=100)
    defects: list[str]
    keyword_match: dict[str, object]
    blind_violations: list[str]
    revised_text: str


def normalize_keywords(raw_keywords: str) -> list[str]:
    """쉼표로 나누고 공백 제거, 빈 문자열은 버린다."""
    keywords = []
    for token in raw_keywords.split(","):
        cleaned = token.strip()
        if cleaned:
            keywords.append(cleaned)
    return keywords


def match_keywords(resume_text: str, required_keywords: list[str]) -> dict[str, object]:
    """자소서 원문과 요구 키워드를 비교해 매칭 결과를 반환한다.

    대소문자 차이는 무시한다.
    """
    lowered = resume_text.lower()
    matched = [kw for kw in required_keywords if kw.lower() in lowered]
    missing = [kw for kw in required_keywords if kw.lower() not in lowered]

    if not required_keywords:
        score = 0
    else:
        score = round(len(matched) / len(required_keywords) * 100)

    return {
        "required": required_keywords,
        "matched": matched,
        "missing": missing,
        "score": score,
    }


def detect_blind_violations(resume_text: str) -> list[str]:
    """블라인드 채용 위험 표현을 일반 패턴으로 감지한다."""
    violations = []

    # 학교명, 학력 직접 노출
    if "대학교" in resume_text or "대학" in resume_text or "학번" in resume_text:
        violations.append("학력/학교명 노출 위험")
    # 나이
    if "나이" in resume_text or "살" in resume_text or "세입니다" in resume_text:
        violations.append("나이 노출 위험")
    # 성별
    if "남성" in resume_text or "여성" in resume_text or "성별" in resume_text:
        violations.append("성별 노출 위험")
    # 지역 출신
    if "출신" in resume_text or "고향" in resume_text:
        violations.append("지역 출신 노출 위험")
    # 연락처 또는 이메일
    if "@" in resume_text or "연락처" in resume_text or "전화" in resume_text:
        violations.append("연락처 또는 이메일 노출 위험")

    return violations


def detect_flaws(resume_text: str, required_keywords: list[str]) -> list[str]:
    """자소서 6대 결함을 감지한다.

    6대 결함:
    - STAR/PREP 프레임 미준수
    - NCS 키워드 누락
    - 블라인드 채용 위반
    - 공백 문장
    - 일반화 표현
    - 수동태 남발
    """
    defects = []

    # STAR/PREP 프레임 미준수: 상황/과제/행동/결과/근거/이유 단서 확인
    star_prep_clues = ["상황", "과제", "행동", "결과", "근거", "이유"]
    if not any(clue in resume_text for clue in star_prep_clues):
        defects.append("STAR/PREP 프레임 미준수")

    # NCS 키워드 누락
    match = match_keywords(resume_text, required_keywords)
    if match["missing"]:
        defects.append("NCS 키워드 누락")

    # 블라인드 채용 위반
    if detect_blind_violations(resume_text):
        defects.append("블라인드 채용 위반")

    # 공백 문장: 빈 줄이나 문장 사이의 비어 있는 문장
    if "\n\n" in resume_text or ".." in resume_text or "。。" in resume_text:
        defects.append("공백 문장")

    # 일반화 표현
    generic_words = ["최선을", "열심히", "좋은", "성장하고 싶습니다"]
    if any(word in resume_text for word in generic_words):
        defects.append("일반화 표현")

    # 수동태 남발: "되었습니다", "하게 되었습니다", "했습니다" 반복
    passive_count = resume_text.count("되었습니다") + resume_text.count("했습니다")
    if passive_count >= 2:
        defects.append("수동태 남발")

    return defects


def analyze_resume(resume_text: str, raw_keywords: str) -> ResumeAnalysis:
    """자소서 원문과 키워드를 받아 ResumeAnalysis로 분석한다."""
    required_keywords = normalize_keywords(raw_keywords)
    keyword_match = match_keywords(resume_text, required_keywords)
    blind_violations = detect_blind_violations(resume_text)
    defects = detect_flaws(resume_text, required_keywords)

    # score: 키워드 매칭 점수를 int로 변환해서 사용 (0~100 범위)
    score = int(keyword_match["score"])

    revised_text = "구체적인 행동, 결과, 직무 키워드를 보완해 다시 작성하세요."

    payload = {
        "score": score,
        "defects": defects,
        "keyword_match": keyword_match,
        "blind_violations": blind_violations,
        "revised_text": revised_text,
    }
    return ResumeAnalysis.model_validate(payload)


def save_analysis(
    analysis: ResumeAnalysis, output_path: str = "analyze_result.json"
) -> None:
    """분석 결과를 UTF-8 JSON으로 저장한다."""
    path = Path(output_path)
    path.write_text(analysis.model_dump_json(indent=2), encoding="utf-8")
    print(f"저장 위치: {path.resolve()}")


def run_cli() -> None:
    """CLI로 /analyze 명령을 받아 자소서를 분석한다."""
    print("자소서 도우미입니다. /analyze 를 입력해요.")
    command = input("명령: ").strip()

    if command == "/analyze":
        resume_text = input("자소서 원문: ")
        raw_keywords = input("NCS/JD 키워드(쉼표 구분): ")

        analysis = analyze_resume(resume_text, raw_keywords)
        save_analysis(analysis)

        print(f"score: {analysis.score}")
        print(f"defects: {analysis.defects}")
        print("saved: analyze_result.json")
    else:
        print("지원하는 명령: /analyze")


if __name__ == "__main__":
    run_cli()
