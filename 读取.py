# -*- coding:UTF-8 -*-
# @Filename:    读取.py
# @Author:      zhaopengtao
# @Time:        2025/7/16 11:34
import requests

FILE_PATH = ""


def main():
    # 1. 读取 128K 文本
    with open(file=FILE_PATH, mode="r") as f:
        long_text = f.read()

    # 2. 构造请求
    url = "http://localhost:8000/v1/completions"
    headers = {"Content-Type": "application/json"}
    data = {
        "model": "deepseek",
        "prompt": f"{long_text}\n请列出所有标记（如---START---）及其大致位置。",
        "max_tokens": 100,  # 限制回答长度
        "temperature": 0  # 确定性输出
    }

    # 3. 发送请求
    response = requests.post(
        url=url,
        headers=headers,
        json=data,
    )
    json_response = response.json()
    print(f"json_response: {json_response}")


if __name__ == '__main__':
    main()
