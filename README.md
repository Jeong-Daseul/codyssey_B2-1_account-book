

# 💰 실무형 가계부 관리 시스템 (budget_app)

파이썬 표준 라이브러리만을 활용하여 구축한 **객체지향 기반 콘솔 가계부 프로그램**입니다. 
단순한 기능 구현을 넘어, 데이터 안정성, 메모리 효율성, 그리고 유지보수가 용이한 **Service-Repository 아키텍처**를 설계하는 데 중점을 두었습니다.

## 🌟 주요 기능 (10가지 핵심 기능)
1.  **거래 기록(Add)**: 수입/지출 내역 저장 (ID 체계: `YYYYMMDD###` 형식)
2.  **목록 조회(List)**: 최신순 정렬 및 조회 개수 제한(`--limit`) 지원
3.  **조건 검색(Search)**: 기간, 카테고리, 타입, 메모 키워드, 태그 기반 필터링
4.  **월별 요약(Summary)**: 지출 TOP N 분석 및 예산 대비 사용률 산출
5.  **예산 관리(Budget)**: 월별 예산 설정 및 현황 조회
6.  **카테고리 관리(Category)**: 수입/지출별 커스텀 카테고리 관리 (삭제 시 대체 카테고리 지정 가능)
7.  **데이터 수정(Update)**: 특정 ID 기반 필드별 부분 수정 (옵션 방식)
8.  **데이터 삭제(Delete)**: 특정 ID 기반 데이터 삭제
9.  **데이터 연동(Import/Export)**: CSV 파일 대량 가져오기 및 내보내기 (데이터 검증 포함)
10. **데이터 시각화(Visualize)**: 콘솔 기반 카테고리별 지출 비중 차트 출력

## 🛠 기술적 특징 (Technical Highlights)

### 1. 효율적인 데이터 처리 및 안정성
- **Generator Streaming**: 수만 개의 데이터를 처리할 때 메모리 부하를 방지하기 위해 파일을 한 번에 올리지 않고, 제너레이터를 통해 한 줄씩 읽어 파싱하는 스트리밍 방식을 적용했습니다.
- **Atomic Write (원자적 쓰기)**: 데이터 수정/삭제 시 임시 파일에 기록 후 `os.replace()`로 교체하여, 작업 중 프로그램이 종료되어도 원본 데이터가 손상되지 않도록 설계했습니다.
- **JSONL 포맷**: 행 단위 JSON 구조를 사용하여 데이터 확장성과 가독성을 모두 확보했습니다.

### 2. 실무형 아키텍처 설계
- **Layered Architecture**: `CLI(입출력)` → `Service(비즈니스 로직)` → `Repository(데이터 저장)` → `Model(데이터 구조)`로 계층을 분리하여 코드의 응집도를 높였습니다.
- **Dataclasses**: `dataclass`를 활용하여 데이터 모델을 정의하고, 타입 힌팅을 통해 코드의 안정성을 높였습니다.

### 3. 공통 관심사 분리 (AOP)
- **Custom Decorators**: 요구사항에 따라 `@handle_errors`, `@log_execution`, `@measure_time` 데코레이터를 구현했습니다. 이를 통해 비즈니스 로직을 더럽히지 않고 예외 처리, 실행 로그 기록, 성능 측정을 공통적으로 적용했습니다.

## 🚀 실행 방법
Python 3.10 이상 환경에서 별도의 패키지 설치 없이 즉시 실행 가능합니다.

```bash
# 전체 도움말 확인
python -m budget_app --help

# 거래 내역 추가 (대화형)
python -m budget_app add

# 월별 요약 및 예산 사용률 확인
python -m budget_app summary --month 2024-01

# 지출 비중 시각화
python -m budget_app visualize --month 2024-01

# 특정 조건 검색
python -m budget_app search --category food --q 점심
```

## 📂 프로젝트 구조
```text
budget_app/
  ├── __main__.py    # 프로그램 진입점 및 CLI 명령어 정의
  ├── models.py      # Transaction, Category, Budget 데이터 모델
  ├── service.py     # 비즈니스 로직 (검증, 계산, CRUD 연산)
  ├── repository.py  # 데이터 저장소 (JSONL 읽기/쓰기, 스트리밍)
  ├── utils.py       # 데코레이터(로깅, 예외처리), 포맷팅 도구
  ├── validators.py  # 데이터 유효성 검증 로직
  └── exceptions.py  # 사용자 정의 예외 클래스
```

## ⚠️ 오류 처리 정책
- 모든 오류는 스택트레이스 대신 `[오류] 원인` + `[힌트] 해결 방법` 형태로 출력하여 사용자 친화적인 경험을 제공합니다.
- 정상 종료 시 `0`, 사용자 취소(Ctrl+C) 시 `130`, 일반 오류 시 `1`의 종료 코드를 반환합니다.
