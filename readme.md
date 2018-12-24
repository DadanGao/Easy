2018年高等软件工程 团队1 项目代码
===============================

# update notes
## 2018.12.24

    在分支情感判定和分支合并过程中加入了情感分析（使用lstm)和tf相似度
    更新项目依赖库文件，可以使用requirements.txt进行环境的搭建
```
sudo pip install -r requirements.txt
```
    
    

## 2018.12.9
    项目使用的是Python 3.6版本， Django 2.1.4版本， jieba分词
    项目运行说明，参考命令
    1 git clone 或 download代码，工程名为Easy
    2 安装Python
    3 安装Django， 命令pip install Django
    4 安装jieba分词，命令为pip install jieba
    5 进入Easy/mysite/, 使用terimal终端，输入python manage.py runserver
    6 使用IE浏览器打开127.0.0.1:8000/transform/，要求打开IE浏览器的 获取本地文件真实路径 选项（只能是IE游览器，必须打开 获取本地文件真实路径 ，否则报错)（获取本地文件真实路径：IE浏览器-选项-安全-自定义级别-启用 将文件上传服务器时包含本地目录路径）
    7 上传GWT文件进行测试（需满足格式要求，可使用工程中的gwt文件，路径为Easy/gwt files/gwt.txt）(其他gwt文档可能因为领域背景知识不足导致转换结果不理想)

## 2018.12.2
    兼容输入路径或文件
    默认导入RUCM关键字
    导入领域背景词汇，默认放置在dict文件夹下
[参考方法：载入词典一节](https://github.com/Ming-Yang/jieba)
## 2018.12.1 
    增加jieba中文分词模块
    使用方法共四步，直接使用，无需install，可在其他模块中共同使用：
```Bash
git submodule init
git submodule update
cd jieba
git checkout dev
```
