# 快速开始：
## 1.配置python环境（我用的3.12.0版本）

## 2.第三方库安装
### requirements.txt安装
pip install -r requirements.txt

或者

### 手动命令行安装第三方库
pip install pypdf
pip install selenium
pip install openai
pip install python-dotenv

## 3.配置OPENAI API
找到目录下的.env配置文件：
1.OPENAI_API_KEY：填入官方或第三方APIKEY
3.OPENAI_BASE_URL：默认为OPENAI官方地址，如使用第三方APIKEY需配置第三方代理地址

## 4.运行：
python run main.py

# 功能：
1.支持BOSS直聘-搜索页-岗位投递
2.自定义匹配Prompt，完成简历与JD匹配
3.支持PDF格式简历文件
4.默认使用gpt-3.5-turbo

# TODO：
1.增加沟通次数上限自动结束代码
2.兼容更多简历格式
3.增加支持推荐页岗位投递