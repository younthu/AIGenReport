请帮我写一个美国本科留学选校报告workflow.

1. 用langchain做workflow编排。
1. 入口参数是输入一个学生profile, 里面包含学生的基本信息。可以是profile文件路径，也可以是完整的profile字符串。
1. university_selection_report/StudentProfile.txt是一个样本文件，可以用来做测试.
1. 代码写入university_selection_report目录。
1. 整个报告生成过程中要求能切换LLM, 要能支持主流的模型，比如OpenAI, gemini, deepseek和qwen.
1. 整个生成过程中会用到很多prompt, 请帮忙根据需求生成对应的prompt.
1. 要求整个过程可观测，好调试。
1. 主体workflow文件名为university_selection_report/university_selection_workflow.py.
1. 类名为UniversitySelectionWorkflow
1. 添加main，添加对workflow的支持。
1. langsmith记log的时候每个章节区分开，方便调试. 注意，如果没有配置langchain api key的情况下代码不要抛错，给出错误提示就可以了。
1. 帮我写一个脚本, 用于启动langserve, 对外提供university_selection_workflow.py的调用服务

选校报告生成流程如下:
1. 拿到学生profile以后先用AI分析,结合学生的基本情况，推荐3个专业。给出每个专业的推荐理由. 生成markdown， 形成专业报告.
1. 然后再推荐1所保底的学校，1所主申的学校，1所冲刺学校。给出推荐理由。
1. 对前面推荐的学校，请填充相关的学校信息。填充的时候需要用到knowledge_base/目录下的知识库内容。先通过学校名称提取相关的学校信息json内容，然后通过上下文传给llm, 让AI帮忙生成对应的markdown内容。
1. 需要填充的学校信息如下:
    1. 学校描述, 简介.
    1. 推荐理由.
    1. 学校的历史招生数据。
    1. 学校的录取要求。
    1. 学校的录取率，亚洲学生录取概况。
1. 每个章节都生成单独的markdown, 最后拼接到一起，形成单个学校的选校报告。然后把所有学校的内容拼接到一起，形成完整的选校报告。
1. 最后把专业报告和选校报告拼接到一起, 形成完整的markdown内容。

请一步一步思考.