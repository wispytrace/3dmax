from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import time
def func(i):
    print("Process", i)
    time.sleep(1)
    print("Process is end ")
if __name__ == "__main__":
    # ProcessPoolExecutor <==> Pool
    p = ProcessPoolExecutor(5)
    # submit <==> apply_async
    p.submit(func, 1)
    # shutdown <==> close + join
    p.shutdown()
    print("主线程")