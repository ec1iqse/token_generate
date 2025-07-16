# -*- coding:UTF-8 -*-
# @Filename:    生成长度文本.py
# @Author:      zhaopengtao
# @Time:        2025/7/16 10:21
import numpy as np
from transformers import AutoTokenizer

# 1. 初始化 Tokenizer（替换为你的模型名称）
tokenizer = AutoTokenizer.from_pretrained("deepseek-ai/DeepSeek-R1-0528")

# 2. 定义标记和生成规则
markers = {
    "---START---": 0.0,  # 开头
    "---MID_1---": 0.25,  # 1/4处
    "---MID_2---": 0.5,  # 中间
    "---MID_3---": 0.75,  # 3/4处
    "---END---": 0.99  # 末尾
}


# 3. 生成文本的函数
def generate_128k_text():
    base_text = "DeepSeek 64K上下文测试文本。此段落重复填充以达到长度要求。" * 100  # 基础重复文本
    full_text = ""
    current_tokens = 0
    target_tokens = 64 * 1024  # 128K tokens

    # 插入标记
    for marker, pos in markers.items():
        required_tokens = int(target_tokens * pos) - current_tokens
        full_text += base_text * (required_tokens // len(tokenizer.encode(base_text)))
        full_text += f"\n{marker}\n"  # 插入标记
        current_tokens = len(tokenizer.encode(full_text))

    # 填充剩余部分
    remaining_tokens = target_tokens - current_tokens
    full_text += base_text * (remaining_tokens // len(tokenizer.encode(base_text)))

    # 验证长度
    final_tokens = len(tokenizer.encode(full_text))
    print(f"生成完成！总Tokens: {final_tokens} (~{final_tokens / 1024:.1f}K)")
    return full_text


# 4. 生成并保存文件
text = generate_128k_text()
with open("64k_context_test.txt", "w") as f:
    f.write(text)
