## Day 4 self2 실행 로그

- 실행 시각: 2026-06-04

- SDK 버전 메모: openai-agents 기반으로 Agent, Runner, handoff, input_guardrail을 사용함.

- 실행 명령: `& c:\resume-helper\.venv\Scripts\python.exe c:/resume-helper/resume_agents.py`

- Guardrail 차단 케이스:
  - 입력 Guardrail 함수는 구성되어 있음.
  - 허위 경력, 없는 경력, 개인정보 노출, 시스템 프롬프트, API 키, 비밀 지시 등 위험 키워드를 입력 단계에서 차단하도록 작성함.
  - 이번 실행 로그에는 분석·첨삭·최종본 라우팅 3건만 확인되었고, 별도 Guardrail 차단 요청 실행 결과는 아직 확인하지 않음.
  - Day 5 self1에서 Guardrail 차단 요청을 별도로 추가 테스트할 예정임.

- 라우팅 성공 케이스:
  - 테스트 1 분석 요청 담당 Agent: 자소서\_분석\_Specialist
  - 테스트 2 첨삭 요청 담당 Agent: 자소서\_첨삭\_Specialist
  - 테스트 3 최종본 요청 담당 Agent: 자소서\_최종본\_Specialist

- 오분기 원인:
  - 초기 실행에서 분석 요청이 첨삭 Specialist로 라우팅되는 오분기가 있었음.
  - handoff 도구명을 ASCII 고유 이름으로 지정하고, 분석·첨삭·최종본 handoff 설명을 더 명확히 분리하여 수정함.
  - 최종 실행에서는 분석 요청, 첨삭 요청, 최종본 요청이 각각 의도한 Specialist로 라우팅됨.

- Day 5 self1 수정 항목:
  - 최종 검증 파이프라인에서 라우팅 결과 3건을 다시 확인함.
  - Guardrail 차단 요청을 별도로 실행하여 차단 여부를 로그로 남김.
  - 안전한 요청까지 차단되는 경우 위험 키워드 조건을 더 구체화함.
