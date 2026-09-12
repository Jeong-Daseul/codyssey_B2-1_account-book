# budget_app/utils.py
import functools
from datetime import datetime

def handle_errors(func):
    """에러를 잡아내고 사용자에게 친절하게 안내하는 데코레이터"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            print(f"⚠️ 입력 오류: {e}")
        except Exception as e:
            print(f"🔥 예상치 못한 오류 발생: {e}")
    return wrapper

def log_action(func):
    """사용자의 주요 활동을 log.txt 파일에 기록하는 데코레이터"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        # 현재 시간과 실행된 함수 이름을 기록
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open("app_log.txt", "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] 실행된 작업: {func.__name__}\n")
        return result
    return wrapper