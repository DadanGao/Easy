2018年高等软件工程 团队1 项目代码
===============================

# update notes
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
