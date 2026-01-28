import os
import time

def main():
    # 先空跑，保证容器能起来
    while True:
        print("worker alive")
        time.sleep(10)

if __name__ == "__main__":
    main()
