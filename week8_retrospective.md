# Week 8 Retrospective

## Day 1

- `.env` 로딩과 OpenAI/Claude 호출 구조를 확인하며 자소서 첨삭 CLI의 기본 흐름을 구성했습니다.

## Day 2

- `/style` 명령으로 작성 스타일을 전환하며 사용자 입력에 따라 첨삭 기준을 바꾸는 방식을 확인했습니다.

## Day 3

- `/analyze`와 `ResumeAnalysis` 구조를 통해 자소서를 점수, 결함, 키워드 매칭, 블라인드 위험으로 나누어 분석했습니다.

## Day 4

- 분석, 첨삭, 최종본 Specialist와 Triage Agent를 구성하며 요청 의도에 따라 Agent를 분기하는 흐름을 확인함.

## Day 5

- AI 1차 필터, `/blind` 점검, README, `.gitignore`, 제출 기록을 정리하며 프로젝트를 제출 가능한 상태로 마무리함.

## 배운 점

- system/user 역할 분리, PCT 구조, 스타일별 프롬프트 차별화, 구조화 출력, Agent 라우팅의 필요성을 확인함.
- API 키와 자소서 원문을 GitHub에 올리지 않도록 `.gitignore`와 `git status --short` 확인이 필요함을 정리함.

## 남은 개선점

- `/analyze`가 `resume_helper.py`와 별도 파일에서 실행되는 구조이므로 README에서 실행 방법을 명확히 안내해야 함.
- 긴 자소서 입력 시 토큰 비용 증가와 raw error 노출 가능성을 줄이는 예외 처리가 필요함.
