# coding: utf-8
# Description: Boss直聘简历JD匹配投递助手，使用Selenium + Openai API + Pypdf
# Author：Meteor

import random
import os
import time

# Selenium导入
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# 导入greeting.py中的函数
from functions import (
    append_log,
    check_resume_file,
    create_greeting,
    create_log,
    pdf_to_text,
)


# 1. 初始化浏览器
def init_browser():
    # 创建Chrome浏览器对象
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")  # 信任代码，禁沙盒可避免资源受限加载失败/慢
    options.add_argument(
        "--disable-blink-features=AutomationControlled"
    )  # 避免检测自动
    options.add_argument("--disable-extensions")
    driver = webdriver.Chrome(options=options)

    # 最大化窗口
    driver.maximize_window()
    return driver


# 2. 登录Boss直聘
def login_boss(driver, wait):
    # 打开Boss直聘登录页面
    driver.get("https://login.zhipin.com/?ka=header-login")

    # 显式等待：等待页面加载，直到出现登录框
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "sms-form-wrapper")))

    # 点击微信登录
    driver.find_element(By.CLASS_NAME, "wx-login-icon").click()

    # 显式等待：等待页面加载，直到出现用户昵称
    WebDriverWait(driver, 120).until(
        EC.presence_of_element_located((By.XPATH, '//a[@ka="header-username"]'))
    )
    print("已完成登录")


# 搜索&筛选岗位
def search_job(driver, wait):
    # 点击搜索
    driver.find_element(By.XPATH, '//a[@ka="header-job"]').click()

    # 显式等待：等待页面加载，直到出现搜索框
    wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "input")))
    print("----进入搜索页----")

    # 交给用户手动筛选
    input("请继续完成筛选，筛选完后在此处回车继续")


# 遍历列表，与面试官打招呼
def greet_interviewer(driver, wait, resume_text, log_file):
    # 储存当前窗口句柄
    original_window = driver.current_window_handle

    # 检查一下是否有打开其他的窗口
    assert len(driver.window_handles) == 1

    # 定位到options-pages下倒数第二个a标签（即下一页按钮的前一个按钮：总页数）,获取总页数
    sum_page = driver.find_element(
        By.XPATH,
        '(//div[@class="options-pages"]/a[contains(@href, "javascript:")])[last()-1]',
    ).text

    # 打印总页数
    print("当前筛选条件下有" + sum_page + "页相关岗位")

    # 遍历总页数
    for p in range(0, int(sum_page)):
        # 获取搜索页面招聘列表
        jobs = driver.find_elements(By.XPATH, "//li[contains(@ka, 'search_list')]")
        print("本页招聘列表总数：" + str(len(jobs)))

        # 遍历搜索页面招聘列表
        for i in range(0, len(jobs) - 1):
            print(
                "正在处理第"
                + str(i + 1)
                + "个岗位，本页剩余"
                + str(len(jobs) - i - 1)
                + "个岗位"
            )

            # 打开岗位
            driver.find_element(
                By.XPATH, '//li[@ka="{}"]'.format(jobs[i].get_attribute("ka"))
            ).click()

            # 等待新窗口或标签页
            wait.until(EC.number_of_windows_to_be(2))

            # 循环执行，直到找到一个新的窗口句柄
            for window_handle in driver.window_handles:
                if window_handle != original_window:
                    # 切换到新窗口
                    driver.switch_to.window(window_handle)
                    break
            print("----打开岗位详情页----")

            # 显式等待：等待页面加载，直到出现岗位描述
            wait.until(
                EC.presence_of_element_located((By.XPATH, '//h3[text()="职位描述"]'))
            )

            # 获取岗位标题
            job_title = driver.find_element(By.CLASS_NAME, "name").text
            print("岗位标题：" + job_title)

            # 获取岗位标签
            job_tags = driver.find_elements(By.CLASS_NAME, "job-keyword-list")
            print("岗位标签：" + "、".join([tag.text for tag in job_tags]))

            # 获取JD文本
            job_content = driver.find_element(By.CLASS_NAME, "job-sec-text").text
            print("岗位描述:\n" + job_content + "\n")

            # JD为岗位标题+岗位标签+岗位描述
            jd = (
                "岗位名称："
                + job_title
                + "\n"
                + "岗位标签："
                + "、".join([tag.text for tag in job_tags])
                + "\n"
                + "岗位描述："
                + job_content
            )

            # 生成招呼语
            greeting_text = create_greeting(resume_text, jd)
            print("已生成招呼语:\n" + greeting_text + "\n")

            # 追加日志
            append_log(jd, greeting_text, log_file)

            # 设置等待延迟（防封）
            time.sleep(random.randint(3, 5))

            # 获取沟通按钮文本
            chat_text = driver.find_element(By.CSS_SELECTOR, "a.btn.btn-startchat").text
            # 判断是否已沟通
            if chat_text == "立即沟通":
                # 点击立即沟通
                driver.find_element(By.CSS_SELECTOR, "a.btn.btn-startchat").click()

                # 显式等待：等待页面加载，直到出现聊天输入框
                wait.until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="chat-input"]'))
                )

                # 定位聊天输入框
                chat_box = driver.find_element(By.XPATH, '//*[@id="chat-input"]')

                # 清除输入框中可能存在的任何文本
                chat_box.clear()

                # 设置等待延迟（防封）
                time.sleep(random.randint(3, 5))

                # 将响应粘贴到输入框
                chat_box.send_keys(greeting_text)

                # 模拟按下回车键来发送消息
                # chat_box.send_keys(Keys.ENTER)
            else:
                print("这家已沟通过,跳过")

            # 设置等待延迟（防封）
            time.sleep(random.randint(3, 5))

            # 关闭标签页或窗口
            driver.close()

            # 切回到之前的标签页或窗口
            driver.switch_to.window(original_window)
            print("----回到搜索页----")

            # 设置等待延迟（防封）
            time.sleep(random.randint(3, 5))

        # 定位到.options-pages下的最后一个a标签 即“下一页”元素
        next_page_element = driver.find_element(
            By.CSS_SELECTOR, ".options-pages a:last-child"
        )

        # 检查其父级元素是否包含 "disabled" 类，检查下一页按钮是否被禁用（禁用即代表没有下一页）
        is_disabled = "disabled" in next_page_element.get_attribute("class")

        # 如果不包含 "disabled" 类，则点击下一页
        if not is_disabled:
            next_page_element.click()

            # 显式等待：等待页面加载，直到出现搜索框
            wait.until(
                EC.visibility_of_element_located(
                    (By.CSS_SELECTOR, ".options-pages a:last-child")
                )
            )

            # 设置等待延迟（防封）
            time.sleep(random.randint(3, 5))
            print("已进入第" + str(p) + "页")
        else:
            print("已到最后一页")
            break


if __name__ == "__main__":
    # 每次程序执行前，关闭已存在的chrome进程，避免影响
    os.system('taskkill /im chrome.exe /F')
    # 调用检查简历文件，返回简历名
    resume_name = check_resume_file()
    # 读取简历内容，转换为文本
    resume_text = pdf_to_text(f"./resume/{resume_name}")
    # 生成日志
    log_file = create_log(resume_text)
    try:
        # 初始化浏览器
        driver = init_browser()
        # 设置常规等待延时
        wait = WebDriverWait(driver, 10)
        # 登录Boss直聘
        login_boss(driver, wait)
        # 搜索岗位
        search_job(driver, wait)
        # 与面试官打招呼
        greet_interviewer(driver, wait, resume_text, log_file)
    except Exception as e:
        print("发生异常:", e)
    finally:
        # 无论是否发生异常，都会执行这里的代码
        driver.quit()
