from pydantic import BaseModel, Field


class ResumeDraftInput(BaseModel):
    selected_style: str = Field(description="선택한 스타일 키")
    original_text: str = Field(description="원본 자소서 텍스트")
    rewritten_text: str = Field(description="첨삭/재작성된 자소서 텍스트")
    observation: list[str] = Field(default_factory=list, description="관찰/메모 목록")


if __name__ == "__main__":
    draft = ResumeDraftInput(
        selected_style="간결형",  # TODO: 실제 선택한 스타일로 교체
        original_text="TODO: 원본 자소서 텍스트",
        rewritten_text="TODO: 재작성된 자소서 텍스트",
        observation=["TODO: 관찰 1", "TODO: 관찰 2"],
    )
    print(draft.model_dump())
