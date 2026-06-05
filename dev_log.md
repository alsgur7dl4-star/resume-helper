## Day 4 self2 실행 로그

- 실행 시각: 2026-06-04

- SDK 버전 메모: Agent, Runner, handoff, input_guardrail을 사용함.

- 실행 명령: `uv run python resume_agents.py`

- Guardrail 차단 케이스:
  - 입력 Guardrail 함수는 구성되어 있음.
  - 허위 경력, 없는 경력, 개인정보 노출, 시스템 프롬프트, API 키, 비밀 지시 등 위험 키워드를 입력 단계에서 차단하도록 작성함.
  - 이번 실행 로그에는 분석·첨삭·최종본 라우팅 3건만 확인되었고, 별도 Guardrail 차단 요청 실행 결과는 아직 확인하지 않음.
  - Day 5 self1에서 Guardrail 차단 요청을 별도로 추가 테스트할 예정임.

- 라우팅 성공 케이스:
  - 테스트 1 분석 요청 담당 Agent: `자소서_분석_Specialist`
  - 테스트 2 첨삭 요청 담당 Agent: `자소서_첨삭_Specialist`
  - 테스트 3 최종본 요청 담당 Agent: `자소서_최종본_Specialist`

- 오분기 원인:
  - 초기 실행에서 분석 요청이 첨삭 Specialist로 라우팅되는 오분기가 있었음.
  - handoff 도구명을 ASCII 고유 이름으로 지정하고, 분석·첨삭·최종본 handoff 설명을 분리하여 수정함.
  - 최종 실행에서는 분석 요청, 첨삭 요청, 최종본 요청이 각각 의도한 Specialist로 라우팅됨.

- Day 5 self1 수정 항목:
  - 최종 검증 파이프라인에서 라우팅 결과 3건을 다시 확인함.
  - Guardrail 차단 요청을 별도로 실행하여 차단 여부를 로그로 남김.
  - 안전한 요청까지 차단되는 경우 위험 키워드 조건을 더 구체화함.

## day5-self1 실행 로그

- 실행 명령: `uv run python resume_helper.py`
- 시작 메시지 확인: [x] 확인함
- 첫 응답 요약: `/help`, `/style`, `/blind`, `/quit` 명령이 정상 동작함.
- 오류가 있었다면 오류 이름: 없음

## day5-self1 검증 항목

- 선택 항목 1: STAR 구조 충족 여부
- 선택 항목 2: 정량 근거 포함 여부
- 선택 항목 3: NCS 직무 키워드 밀도
- 선택 이유: 신입 개발자 자소서에서 경험 구조, 근거, 직무 연결성이 먼저 확인되어야 한다고 판단함.

## day5-self1 자유 기능

- 내가 고른 후보: C
- 명령 이름: /blind
- 구현 위치: day5_self1_resume_pipeline.py, resume_helper.py
- 실행 확인 로그 1줄: `/blind` 실행 결과 블라인드 채용 위험 표현 후보가 발견되지 않음.

## day5-self1 회귀 테스트

- `/help`: [x] 통과 / [ ] 수정 필요
- `/style`: [x] 통과 / [ ] 수정 필요
- `/analyze`: [ ] 통과 / [x] 수정 필요
- `/blind`: [x] 통과 / [ ] 수정 필요
- `/quit`: [x] 통과 / [ ] 수정 필요
- 끊긴 기능 원인 1줄: 현재 `/analyze`는 `resume_helper.py`가 아니라 `day3_self2_resume_mcp.py`에서 제공되는 명령임.
- 수정 후보 목록:
  - 최종 제출 전 README에서 `/analyze` 실행 파일이 `day3_self2_resume_mcp.py`임을 별도로 안내함.
  - 필요 시 추후 `resume_helper.py`에 `/analyze` 통합을 선택 개선으로 검토함.
  - `/blind` 기능이 추가되었으므로 `resume_helper.py`의 `/help` 출력에 `/blind` 설명을 1줄 추가함.

## README 입력 메모

### 실행 명령

- `uv run python resume_helper.py`

### 필요한 환경변수

- `OPENAI_API_KEY`
- `ANTHROPIC_API_KEY` (Claude 비교 기능을 사용한 경우)
- `MODEL_OPENAI`
- `MODEL_CLAUDE`

### 오늘 추가한 자유 기능

- 명령 이름: /blind
- 사용 방법 1줄: 자소서 본문에서 블라인드 채용 위험 표현 후보를 찾아 출력함.
- 실행 예시 1줄: `/blind` 입력 후 점검할 자소서를 붙여넣음.

### 최종 검증 결과

- 선택한 검증 항목 3개: STAR 구조 충족 여부, 정량 근거 포함 여부, NCS 직무 키워드 밀도
- 개선 권고 1개: 결과 항목을 실제 근거가 있는 수치로 보강하고, API·테스트·협업·버전관리 등 백엔드 직무 키워드를 자연스럽게 포함할 필요가 있음.
- 남은 수정 후보: `/analyze` 명령이 `resume_helper.py`에 통합되어 있지 않으므로 최종 제출 전 통합 여부 또는 별도 실행 안내가 필요함.

### 다음 시간에 넘길 것

- README에 넣을 기능 목록: 스타일 프리셋, 자소서 첨삭, Day3 분석 기능, Day4 Agent 라우팅, Day5 AI 1차 필터, /blind 블라인드 채용 점검
- GitHub push 전 개인정보 점검 여부: `.env`, `resumes/`, `*.txt`, `outputs/*.json`, `analyze_result.json`, `chat_history.json` 제외 여부를 확인해야 함.
