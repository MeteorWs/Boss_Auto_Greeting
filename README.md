# Boss简历-招聘岗位匹配投递助手

本项目旨在利用ChatGPT模型，结合Selenium、OpenAI API和pypdf技术，自动化个人简历与Boss直聘等招聘网站上的招聘岗位 JD（Job Description）的匹配过程，并完成自动打招呼语。

***免责声明：本文章涉及到的应用仅供学习交流使用，不得用于任何商业用途，数据来源于互联网公开内容，没有获取任何私有和有权限的信息（个人信息等）。由此引发的任何法律纠纷与本人无关！禁止将本文技术或者本文所关联的Github项目源码用于任何目的。***

## 需求

- Python 3.x环境

- OpenAI 或第三方转发APIKEY

## 注意事项

  - 请注意遵守各网站的使用协议和法律法规，避免违反网站的使用规定。

## 快速开始

1. ### 配置python环境（我用的3.12.0版本）

2. ### 第三方库安装

   #### 打包安装

   ```
   pip install -r requirements.txt
   ```

   #### 手动命令行安装

   ```
   pip install pypdf
   pip install selenium
   pip install openai
   pip install python-dotenv
   ```
3. ### 配置OPENAI API
找到目录下的.env配置文件：
OPENAI_API_KEY：填入官方或第三方APIKEY
OPENAI_BASE_URL：默认为OPENAI官方地址，如使用第三方APIKEY需配置第三方代理地址

4. ### 将简历放入目录
将简历放入resume目录下，注意目前只支持pdf格式

5. ### 运行

    ```
    python run main.py
    ```

## 功能
- 支持BOSS直聘-搜索页-岗位投递
- 自定义匹配Prompt，完成简历与JD匹配
- 支持PDF格式简历文件
- 默认使用gpt-3.5-turbo模型，可自行在functions.py中替换
- 打印简历解析及招呼语日志，方便分析调整prompt效果

## TODO
- 增加沟通次数上限自动结束代码
- 兼容更多简历格式
- 增加支持推荐页岗位投递

## 请作者喝杯咖啡

如果你觉得这个项目对你有帮助，可以请我喝杯咖啡 ^_^

<img src="https://mybucket-1308772293.cos.ap-guangzhou.myqcloud.com/picture/202404141649095.jpg" alt="请我喝杯咖啡" style="zoom:20%;" />



