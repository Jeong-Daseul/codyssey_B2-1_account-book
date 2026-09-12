미션 요구사항에 명시된 **'유지보수 가능한 설계'**, **'데이터 안전성'**, **'제너레이터/데코레이터 활용'** 등의 핵심 가치를 모두 담아 아주 상세하게 작성해 드립니다. 

이 내용을 `README.md`에 그대로 복사해서 사용하시면 됩니다.

---

# 💰 실무형 가계부 관리 시스템 (Budget App)

> **"작은 서비스란 기능이 많은 것이 아니라, 예외 상황에서도 데이터가 안전한 것을 말합니다."**

본 프로젝트는 단순한 가계부 기능을 넘어, **유지보수 가능한 아키텍처**와 **대용량 데이터 처리**를 고려한 실무형 콘솔 애플리케이션입니다. Python의 고급 기능(Generator, Decorator, Type Hinting)을 활용하여 설계되었습니다.

---

## 🚀 1. 시작하기 (Installation & Execution)

### 환경 요구 사항
- **Python 3.8 이상** (Type Hinting 및 Dataclass 사용)

### 실행 방법
별도의 설치 과정 없이 패키지 형태로 즉시 실행 가능합니다.
```bash
# 프로젝트 루트 디렉토리에서 실행
python -m budget_app
```

---

## 🏗 2. 시스템 아키텍처 (Architecture)

본 프로그램은 **Service-Repository 패턴**을 채택하여 관심사를 분리하였습니다.

- **UI Layer (`__main__.py`)**: 사용자의 입력을 받고 결과를 출력하는 인터페이스 담당
- **Service Layer (`service.py`)**: 비즈니스 로직(통계 계산, ID 생성, 유효성 검증) 담당
- **Repository Layer (`repository.py`)**: 데이터의 영구 저장 및 로드 담당 (JSONL 핸들링)
- **Model Layer (`models.py`)**: 데이터 구조 정의 (Dataclass 활용)
- **Utils Layer (`utils.py`)**: 공통 데코레이터 및 유틸리티 함수

---

## ✨ 3. 주요 기능 (Key Features)

| 기능 | 설명 |
| :--- | :--- |
| **거래 추가 (Add)** | 날짜, 타입, 카테고리, 금액, 메모를 입력받아 `YYYYMMDD###` 형식의 고유 ID 부여 |
| **목록 조회 (List)** | 전체 내역을 최신순으로 출력. **제너레이터 스트리밍**으로 메모리 효율 극대화 |
| **내역 검색 (Search)** | 기간(From-To), 카테고리, 타입, 키워드 검색 지원 |
| **월별 요약 (Summary)** | 월별 총수입/지출/잔액 계산 및 **지출 TOP N 카테고리** 리포트 제공 |
| **예산 관리 (Budget)** | 월별 예산 설정 기능. 요약 시 **예산 사용률 계산 및 초과 경고** 알림 |
| **카테고리 관리** | 수입/지출별 카테고리 커스텀 관리 (사용 중인 카테고리 삭제 방지 로직 포함) |
| **수정/삭제 (Update/Delete)** | 고유 ID 기반의 안전한 데이터 조작 |
| **데이터 내보내기 (Export)** | 특정 기간의 데이터를 표준 **CSV 형식**으로 추출 |
| **데이터 가져오기 (Import)** | 외부 CSV 파일을 읽어 기존 데이터와 병합 (데이터 무결성 검증) |

---

## 💾 4. 데이터 저장 방식 (Data Storage)

데이터 안전성을 위해 3개의 독립된 파일로 관리하며, 대용량 처리에 적합한 **JSONL(JSON Lines)** 형식을 사용합니다.

1.  **`transactions.jsonl`**: 모든 수입/지출 거래 내역 저장
2.  **`categories.jsonl`**: 사용자가 정의한 카테고리 목록 저장
3.  **`budgets.jsonl`**: 월별 예산 설정 데이터 저장

### 📁 CSV 스키마 (Import/Export 전용)
외부 파일과 연동 시 아래 스키마를 준수해야 합니다.

| Column | Type | Description | Example |
| :--- | :--- | :--- | :--- |
| **id** | String | 고유 식별자 (YYYYMMDD###) | 20231027001 |
| **date** | String | 거래 날짜 (YYYY-MM-DD) | 2023-10-27 |
| **type** | String | 수입 또는 지출 | 지출 |
| **category** | String | 등록된 카테고리명 | 식비 |
| **amount** | Integer | 거래 금액 | 15000 |
| **memo** | String | 상세 내용 또는 태그 | 점심 식사 |

---

## 🛠 5. 기술적 특징 (Technical Implementation)

### 1) 제너레이터 스트리밍 (Generator Streaming)
데이터 파일이 커져도 시스템이 느려지지 않도록 `Repository`에서 데이터를 읽을 때 `yield` 키워드를 사용하여 한 줄씩 처리합니다.
```python
# 예시: 메모리에 전체를 올리지 않고 한 줄씩 필터링
def find_all(self):
    with open(self.file_path, 'r') as f:
        for line in f:
            yield self._to_model(json.loads(line))
```

### 2) 데코레이터 기반 공통 로직 분리 (Decorators)
반복되는 예외 처리와 로깅을 데코레이터로 분리하여 비즈니스 로직의 가독성을 높였습니다.
- `@exception_handler`: 프로그램 중단을 방지하고 사용자 친화적 에러 메시지 출력
- `@log_execution`: 주요 작업의 실행 여부와 시간을 기록

### 3) 타입 힌트 (Type Hinting)
`typing` 모듈을 활용하여 함수 간의 데이터 계약을 명확히 함으로써 개발 단계에서의 버그를 최소화했습니다.

---

## 📝 6. 주요 명령어 사용 예시

- **거래 추가**: 메뉴에서 `1` 선택 후 대화형 입력 진행
- **예산 설정**: 메뉴에서 `5` 선택 -> `2023-10` 입력 -> `500000` 입력
- **데이터 내보내기**: 메뉴에서 `9` 선택 -> 파일명 `my_data.csv` 입력
- **검색**: 메뉴에서 `3` 선택 -> 검색어(예: "편의점") 입력

---

### 💡 유지보수 참고 사항
- 새로운 기능을 추가할 때는 `service.py`에 로직을 구현하고 `__main__.py`에서 호출하는 구조를 유지하세요.
- 데이터 필드 변경 시 `models.py`의 `Transaction` 데이터 클래스를 먼저 수정해야 합니다.

---

