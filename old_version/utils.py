import functools
import time

# 기능이 실행되는 시간을 측정하고 기록하는 데코레이터입니다.
def logger(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"\n[LOG] '{func.__name__}' 기능을 실행합니다...")
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"[LOG] 완료! (소요시간: {end_time - start_time:.4f}초)")
        return result
    return wrapper