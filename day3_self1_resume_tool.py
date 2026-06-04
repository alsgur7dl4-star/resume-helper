"""Day 3 self1: ResumeAnalysis 스키마 초안과 결함 Enum 후보 점검용 도구.

오늘 범위:
- ResumeAnalysis 5필드 스키마 초안
- 자소서 6대 결함 DefectType Enum 후보
- 예시 payload(TODO 스캐폴드)
- Pydantic 검증 로그 출력
"""

from enum import Enum

from pydantic import BaseModel, Field


class ResumeAnalysis(BaseModel):
    """자소서 분석 결과 5필드 스키마 초안."""

    growth: str = Field(..., description="성장 과정에서 직무와 연결되는 단서")

    # TODO: 지원 동기에서 회사 또는 직무와 연결되는 이유
    motivation: str = Field(
        ..., description="지원 동기에서 회사 또는 직무와 연결되는 이유"
    )

    # TODO: 입사 후 포부와 향후 기여 방향
    aspiration: str = Field(..., description="입사 후 포부와 향후 기여 방향")

    # TODO: 직무 관련 경험, 역할, 행동, 결과 단서
    experience: str = Field(..., description="직무 관련 경험, 역할, 행동, 결과 단서")

    # TODO: 성공 또는 실패 경험과 배운 점
    success_failure: str = Field(..., description="성공 또는 실패 경험과 배운 점")


class DefectType(Enum):
    """자소서 6대 결함 후보."""

    abstract_expression = "추상표현"
    missing_metric = "정량부재"
    keyword_mismatch = "키워드미스매치"
    self_promotion = "자기자랑"
    inconsistency = "일관성결여"
    generic_template = "공통템플릿"


def build_sample_payload() -> dict[str, str]:
    """5필드 TODO 스캐폴드 형태의 예시 payload를 반환한다.

    개인정보, API 키, 회사명, 학교명, 연락처는 넣지 않는다.
    """
    return {
        "growth": "TODO: 성장 과정에서 직무와 연결되는 단서를 한 문장으로 적어요.",
        "motivation": "TODO: 지원 동기에서 회사 또는 직무와 연결되는 이유를 한 문장으로 적어요.",
        "aspiration": "TODO: 입사 후 포부와 향후 기여 방향을 한 문장으로 적어요.",
        "experience": "TODO: 직무 관련 경험, 역할, 행동, 결과 단서를 한 문장으로 적어요.",
        "success_failure": "TODO: 성공 또는 실패 경험과 배운 점을 한 문장으로 적어요.",
    }


def validate_payload() -> None:
    """예시 payload를 ResumeAnalysis로 검증하고 점검 로그를 출력한다."""
    payload = build_sample_payload()

    analysis = ResumeAnalysis.model_validate(payload)
    print("[model_dump]")
    print(analysis.model_dump())

    schema = ResumeAnalysis.model_json_schema()
    print("\n[required]")
    print(schema["required"])
    print("\n[properties keys]")
    print(list(schema["properties"].keys()))

    print("\n[DefectType values]")
    print([defect.value for defect in DefectType])


if __name__ == "__main__":
    validate_payload()
