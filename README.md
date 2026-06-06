# 나만의 자소서 도우미

## 프로젝트 목적

- 한국 자소서의 3~5문항 작성 과정에서 추상 표현, 정량 근거 부족, 직무 키워드 부족, 블라인드 채용 위험 표현을 점검하는 CLI 도구입니다.
- STAR/PREP/CAR 구조, NCS/JD 키워드, 스타일 프리셋, Agent 라우팅, `/blind` 점검을 통해 제출 전 자소서 품질을 확인합니다.

## 실행 환경

- Python: `>=3.11` (현재 프로젝트에서 확인된 실행 버전은 3.11.15)
- 실행 도구: uv
- 주요 패키지: `openai`, `anthropic`, `openai-agents`, `python-dotenv`, `pydantic`

## 실행 방법

```powershell
uv run python resume_helper.py
```

## 필요한 설정

`.env` 파일에 아래 환경변수를 설정합니다.
실제 키 값은 README에 적지 않으며, `.env`는 GitHub에 올리지 않습니다.

- `OPENAI_API_KEY`
- `ANTHROPIC_API_KEY`
- `MODEL_OPENAI`
- `MODEL_CLAUDE`

## 주요 기능

- 일반 자소서 첨삭: 입력한 자소서를 현재 선택된 스타일 기준으로 첨삭합니다.
- `/style`: 작성 스타일(간결형, 스토리형, 직무맞춤형, 친근한 버전, AI 서비스 연결형 등)을 전환합니다.
- `/blind`: 블라인드 채용 위험 표현 후보를 점검합니다. (`day5_self1_resume_pipeline.py`의 `check_blind_risks()`, `format_blind_report()` 사용)
- `day3_self2_resume_mcp.py`의 `/analyze`: 점수, 결함, 키워드 매칭, 블라인드 위험을 로컬에서 분석합니다. (`resume_helper.py`가 아니라 별도 파일에서 실행)
- `resume_agents.py`: 분석/첨삭/최종본 Specialist와 Triage Agent 라우팅을 확인합니다.

각 기능별 실행 명령:

```powershell
uv run python resume_helper.py
uv run python day3_self2_resume_mcp.py
uv run python resume_agents.py
uv run python day5_self1_resume_pipeline.py
```

## 예시 입출력

실제 자소서 원문 대신 익명화된 예시만 사용합니다.

- 지원 직무: 백엔드 개발자
- 문항: 직무 역량
- 초안(샘플): 샘플 지원자는 웹 개발 프로젝트에서 인증 기능과 API 흐름을 점검하며 문제 해결 경험을 쌓았습니다.

출력 예시:

- 요약: 직무 관련 경험은 있으나 행동과 결과가 구체적으로 드러나지 않음.
- 발견한 결함: 정량 근거 부재, NCS 직무 키워드 밀도 낮음.
- 개선 방향: STAR 구조로 상황·행동·결과를 분리하고, 인증/API 관련 직무 키워드를 자연스럽게 보강.
- 다음 행동: 본인이 실제로 한 행동과 확인 가능한 결과를 한 문장씩 추가.

## 보안 주의

- `.env`는 GitHub에 올리지 않습니다.
- 자소서 원문 `*.txt`, `resumes/`, `outputs/*.json`, `outputs/*.log`, `logs/`는 GitHub에 올리지 않습니다.
- 이름, 학교명, 연락처, 가족 정보 등 개인정보는 README 예시에 포함하지 않습니다.
- `.gitignore`에는 `.env`, `.venv/`, `*.txt`, `resumes/`, `outputs/*.json`, `outputs/*.log`, `logs/`, `submit_local/` 등 민감 파일 제외 항목을 포함합니다.

## 제출 전 점검 명령

GitHub에 올리기 전에 아래 명령으로 commit 대상 파일을 확인합니다.

```powershell
git status --short
git diff --stat
```

`git status --short` 결과에 아래 항목이 보이면 commit하지 않습니다.

```text
.env
resumes/
*.txt
analyze_result.json
chat_history.json
outputs/*.json
outputs/*.log
logs/
```

민감 파일이 보이면 `.gitignore`를 먼저 수정한 뒤 다시 확인합니다.

## 제출 기록

- 저장소 공개 범위: Public
- 마지막 commit 메시지: `Finalize resume helper submission`
- push 시각: 2026-06-06 12:54
- push 결과: 성공
- 로컬 제출 대체 사유: 해당 없음
- 민감 파일 점검: `git status --short` 결과에 `.env`, `*.txt`, `resumes/`, `analyze_result.json`, `chat_history.json`, `outputs/*.json`, `outputs/*.log`, `logs/`가 포함되지 않음을 확인함.

## 5일 회고

- Day 1: `.env` 로딩과 OpenAI/Claude 호출 구조를 확인하며 자소서 첨삭 CLI의 기본 흐름을 구성함.
- Day 2: `/style` 명령으로 작성 스타일을 전환하며 사용자 입력에 따라 첨삭 기준을 바꾸는 방식을 학습함.
- Day 3: `/analyze`와 `ResumeAnalysis` 구조를 통해 자소서를 점수, 결함, 키워드 매칭, 블라인드 위험으로 나누어 분석함.
- Day 4: 분석, 첨삭, 최종본 Specialist와 Triage Agent를 구성하며 요청 의도에 따라 Agent를 분기하는 흐름을 확인함.
- Day 5: AI 1차 필터, `/blind` 점검, README, `.gitignore`, 제출 기록을 정리하며 프로젝트를 제출 가능한 상태로 마무리함.

## 남은 위험

- API 키 누출 위험: `.env`나 로그에 키가 들어가지 않도록 계속 점검 필요.
- 토큰 비용 증가 위험: 긴 자소서 반복 호출 시 비용이 늘 수 있음.
- raw error 노출 위험: 예외 메시지가 사용자에게 그대로 노출될 수 있음.
- `/analyze` 구조 혼동 가능성: `/analyze`는 `resume_helper.py`가 아니라 `day3_self2_resume_mcp.py`에서 별도 실행되는 구조라 혼동될 수 있음.

## 9주차 TODO (Streamlit 전환)

- 재사용 후보 함수:
  - `resume_helper.py`의 첨삭 흐름(`chat_loop` 내 OpenAI 호출, 스타일 프리셋 적용)
  - `day3_self2_resume_mcp.py`의 `analyze_resume()`
  - `day5_self1_resume_pipeline.py`의 `check_blind_risks()`, `format_blind_report()`, `check_resume_ai_filter()`

- 화면 구성(TODO만, 코드 없음): 자소서 입력칸, 스타일 선택, 분석 실행 버튼, 블라인드 점검 결과 영역.
