import functools

def handle_errors(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            print(f"❌ 입력 값이 올바르지 않습니다: {e}")
        except Exception as e:
            print(f"❌ 오류 발생: {e}")
    return wrapper

def log_action(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        # print(f"LOG: {func.__name__} 실행 완료")
        return result
    return wrapper