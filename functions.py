import datetime
import os
import sys

from dotenv import load_dotenv
from openai import OpenAI
from pypdf import PdfReader

from prompts import prompt

# 读取环境变量
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL")

# 初始化 OpenAI 客户端
client = OpenAI(
    api_key=OPENAI_API_KEY,
    base_url=OPENAI_BASE_URL,
)


# 生成日志
def create_log(resume):
    # 获取当前时间
    current_time = datetime.datetime.now()

    # 格式化时间为字符串
    formatted_time = current_time.strftime("%Y-%m-%d_%H-%M-%S")

    # 将变量文本写入文件
    with open(f"./log/{formatted_time}.txt", "w", encoding="utf-8") as file:
        file.write(resume)

    print(f"已生成日志：{formatted_time}.txt")
    return formatted_time


# 追加日志
def append_log(jd, greeting_text, log_file):
    with open(f"./log/{log_file}.txt", "a", encoding="utf-8") as file:
        file.write("\n\n\n")
        file.write("公司招聘要求：\n")
        file.write(jd)
        file.write("\n\n")
        file.write("生成招呼语：\n")
        file.write(greeting_text)
    print(f"已追加日志：{log_file}.txt")


# 检查简历文件是否存在、是否只有一个，如果正常则返回文件名
def check_resume_file():
    resume_files = [file for file in os.listdir("./resume") if file.endswith(".pdf")]
    if len(resume_files) == 0:
        print("没有找到简历文件! 程序已结束！")
        sys.exit()
    elif len(resume_files) > 1:
        print("只能处理一个简历文件! 程序已结束！")
        sys.exit()
    else:
        return resume_files[0]


# 读取简历内容，转换为文本
def pdf_to_text(pdf_path):
    reader = PdfReader(pdf_path)
    resume_text = ""
    for page in reader.pages:
        resume_text += page.extract_text()
    return resume_text


# 生成问候语
def create_greeting(resume, jd):
    # 调用 OpenAI API
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": "这是简历：\n" + resume},
            {"role": "user", "content": "这是公司招聘要求：\n" + jd},
        ],
        stream=False,  # 是否开启流式输出
    )
    return str(completion.choices[0].message.content).replace("\n", " ")



