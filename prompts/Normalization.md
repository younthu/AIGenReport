请用python帮忙实现一个学校名称归一化的类, 具体要求如下:

1. 类名UniversityNormalization, 文件名normalization/university_normalization.py
1. 给定一个英文的学校名称列表, 把这个学校名称列表生成embedding. 可以通过开源的sbert生成，也可以通过openai api/google gemini api生成。默认用开源的sbert 生成。sbert要支持bge和qwen的模型. 向量请用faiss+本地文件做持久化.
1. 英文学校名称列表为 normalization/university_primary_keys.txt
1. 输入一个学校名称，对输入的学校名称先生成embedding，然后通过向量搜索找出top k, 然后再用sbert qwen重排，取排第一的记录。 输出归一化以后的学校名称。
1. 代码写到normalization目录下.