import psutil
import time
import gc

def clean_memory_windows(target_ratio=0.5):
    mem = psutil.virtual_memory()
    print(f"[Before] Available: {mem.available / 1e6:.2f} MB, Total: {mem.total / 1e6:.2f} MB")

    if mem.available / mem.total > target_ratio:
        print("十分な空きがあります。メモリ確保はスキップします。")
        return

    reserve_size = max(0, int(mem.total * (1 - target_ratio)) - int(mem.available))
    print(f"Reserving approx: {reserve_size / 1e6:.2f} MB")

    if reserve_size <= 0:
        print("十分な空きがあります。メモリ確保はスキップします。")
        return

    try:
        # メモリ確保
        block = bytearray(reserve_size)
        # ページングを強制するため触れる
        for i in range(0, len(block), 4096):
            block[i] = 1
        print("メモリ使用中...一時待機")
        time.sleep(2)
    finally:
        del block
        print("メモリ解放完了")

    gc.collect()
    # 状態確認
    mem = psutil.virtual_memory()
    print(f"[After] Available: {mem.available / 1e6:.2f} MB")
