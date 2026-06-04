# Day 3 self1 스키마 점검표

## 학생 기록용

선택한 샘플: AI 서비스 연결형

선택 이유: 기존 SI 자바 웹개발 인턴 경험을 MCP·AI 서비스 개발 방향과 연결하기에 좋을거 같습니다.

개인정보 점검: 통과  
API 키 노출 점검: 통과

다음 입력으로 사용할 문단:
SI 자바 웹개발 3개월 인턴을 마쳤습니다. SI/SM 프로젝트를 진행하면서 배치 실행 중 발생한 오류를 처리하는 방법을 경험했고, 여러 기능을 하나로 합치는 역할을 맡았습니다. 이 경험을 바탕으로 MCP·AI 서비스 개발 과정에서 기능 통합과 오류 대응 역량을 확장하고자 합니다.

## 필드 점검표

- [x] 성장 필드가 있다.
- [x] 동기 필드가 있다.
- [x] 포부 필드가 있다.
- [x] 경험 필드가 있다.
- [x] 성공실패 필드가 있다.
- [x] 결함 Enum 후보 6개가 있다.
- [x] 예시 JSON 스캐폴드가 있다.
- [x] 다음 시간 `/analyze` 입력으로 넘길 파일명을 적었다. → day3_self1_resume_tool.py

## 실행 로그

실행 명령:
`uv run python day3_self1_resume_tool.py`

실행 결과:

```
[model_dump]
{'growth': 'TODO: 성장 과정에서 직무와 연결되는 단서를 한 문장으로 적어요.', 'motivation': 'TODO: 지원 동기에서 회사 또는 직무와 연결되는 이유를 한 문장으로 적어요.', 'aspiration': 'TODO: 입사 후 포부와 향후 기여 방향을 한 문장으로 적어요.', 'experience': 'TODO: 직무 관련 경험, 역할, 행동, 결과 단서를 한 문장으로 적어요.', 'success_failure': 'TODO: 성공 또는 실패 경험과 배운 점을 한 문장으로 적어요.'}

[required]
['growth', 'motivation', 'aspiration', 'experience', 'success_failure']

[properties keys]
['growth', 'motivation', 'aspiration', 'experience', 'success_failure']

[DefectType values]
['추상표현', '정량부재', '키워드미스매치', '자기자랑', '일관성결여', '공통템플릿']
```

<!-- 참고: PowerShell 콘솔 코드페이지가 UTF-8이 아니면 한글이 깨져 보일 수 있으나 데이터 자체는 정상입니다. -->

## 자기 점검 결과

- [x] ResumeAnalysis 5필드 초안이 있다.
- [x] 자소서 6대 결함 Enum 초안이 있다.
- [x] 예시 JSON 스캐폴드가 있다.
- [x] 실행 로그 또는 필드 누락 점검표가 있다.

완료율: 100%
다음 조치: 다음 시간 `/analyze` 명령에서 위 입력 문단을 ResumeAnalysis 스키마로 분석

## 필드별 메모

- growth: 웹 개발자로 준비해 온 경험을 바탕으로 MCP·AI 서비스 개발 방향으로 확장하고 있습니다.
- motivation: 단순 웹 기능 구현을 넘어 AI 기능을 실제 서비스에 연결하는 개발자가 되고 싶습니다.
- aspiration: 기능 통합과 오류 대응 경험을 바탕으로 안정적인 AI 서비스 개발에 기여하고 싶습니다.
- experience: SI/SM 프로젝트에서 배치 실행 중 발생한 오류 처리와 여러 기능을 하나로 합치는 역할을 경험했습니다.
- success_failure: 배치 오류 처리 경험을 통해 기능이 안정적으로 동작하려면 오류 흐름과 기능 간 연결을 이해해야 한다는 점을 배웠습니다.
