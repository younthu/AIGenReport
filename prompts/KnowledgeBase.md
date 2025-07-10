# 知识库构建

请帮我构建一个知识库大学数据知识库, 需求如下:
1. 类名UniversityKnowledge, python代码, university_knowledge.py
1. 用llamaindex构建知识库。
1. 知识库的内容是大学的录取相关的数据和一些其它基本信息，json结构.
1. 每所大学都有一个University Name字段，请对这个字段的内容做索引。
1. 查询的时候输入大学名称，通过向量查询和关键词检索来查询，然后做多路召回。
1. 查询出top k以后再做rerank。
1. rerank以后去排名第一的那个学校名称，然后取出对应的json数据返回。
1. 要求可以测试，可以观测，可以看到每一步的输入输出。
1. 请给代码写好注释。
1. 向量数据持久化请抽象一下，同时支持faiss+本地文件和milvus lite。默认用faiss.
1. 生成的内容放knowledge_base下面。
1. 
