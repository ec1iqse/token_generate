# -*- coding:UTF-8 -*-
# @Filename:    生成长度文本.py
# @Author:      zhaopengtao
# @Time:        2025/7/16 10:21
from transformers import AutoTokenizer

# 1. 初始化 Tokenizer
tokenizer = AutoTokenizer.from_pretrained("deepseek-ai/DeepSeek-R1-0528")

# 2. 定义标记和生成规则
markers: dict = {
    "---START---": 0.0,  # 开头
    "---MID_1---": 0.25,  # 1/4处
    "---MID_2---": 0.5,  # 中间
    "---MID_3---": 0.75,  # 3/4处
    "---END---": 0.99  # 末尾
}


# 3. 生成文本的函数
def generate_text():
    base_text: str = "DeepSeek 128K上下文测试文本。此段落重复填充以达到长度要求。" * 100  # 基础重复文本
    full_text: str = ""
    current_tokens: int = 0
    target_tokens: int = 64 * 1024  # 128K tokens

    # 插入标记
    for marker, pos in markers.items():
        required_tokens: int = int(target_tokens * pos) - current_tokens
        full_text += base_text * (required_tokens // len(tokenizer.encode(base_text)))
        full_text += f"\n{marker}\n"  # 插入标记
        current_tokens: int = len(tokenizer.encode(full_text))

    # 填充剩余部分
    remaining_tokens: int = target_tokens - current_tokens
    full_text += base_text * (remaining_tokens // len(tokenizer.encode(base_text)))

    # 验证长度
    final_tokens: int = len(tokenizer.encode(full_text))
    print(f"生成完成！总Tokens: {final_tokens} (~{final_tokens / 1024:.1f}K)")
    return full_text


def main():
    # 4. 生成并保存文件
    text: str = generate_text()
    with open(file="128k_context_test.txt", mode="w") as f:
        f.write(text)


if __name__ == '__main__':
    main()
