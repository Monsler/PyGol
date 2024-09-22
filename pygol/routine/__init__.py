import asyncio
import threading
import time, datetime

def _run_async_void(millis, void, repeats):
    if repeats > 0:
        for _ in range(repeats):
            time.sleep(millis/1000)
            void()
    elif repeats <= 0:
        while True:
            time.sleep(millis/1000)
            void()

def perform_with_delay(millis, target, times=1):
    threading.Thread(target=_run_async_void, args=(millis, target, times), daemon=True).start()