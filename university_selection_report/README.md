# 美国本科留学选校报告生成服务

基于LangChain和LangServe的美国本科留学选校报告生成服务。

## 功能特性

- 🎯 **专业推荐**: 基于学生profile推荐3个最适合的专业
- 🏫 **学校推荐**: 推荐保底、主申、冲刺学校
- 📊 **详细信息**: 生成学校描述、录取要求、历史数据等
- 🔄 **LLM切换**: 支持OpenAI、Gemini、DeepSeek、Qwen等主流模型
- 📈 **可观测性**: 集成LangSmith tracing，便于调试和优化
- 🌐 **API服务**: 通过LangServe提供REST API接口

## 快速开始

### 1. 安装依赖

```bash
pip install langchain langserve fastapi uvicorn
```

### 2. 设置环境变量（可选）

```bash
# LangSmith tracing（可选）
export LANGCHAIN_API_KEY="your_api_key_here"

# 服务配置
export HOST="0.0.0.0"
export PORT="8000"
```

### 3. 启动服务

#### 方式一：使用启动脚本（推荐）

```bash
cd university_selection_report
python start_langserve.py
```

#### 方式二：直接使用langserve命令

```bash
cd university_selection_report
langserve run --host 0.0.0.0 --port 8000 university_selection_workflow:UniversitySelectionWorkflow
```

### 4. 访问服务

- **服务地址**: http://localhost:8000
- **API文档**: http://localhost:8000/docs
- **健康检查**: http://localhost:8000/health

## API使用

### 生成选校报告

```bash
curl -X POST "http://localhost:8000/invoke" \
  -H "Content-Type: application/json" \
  -d '{
    "input": {
      "profile": "学生profile内容或文件路径",
      "llm_name": "openai",
      "debug": false
    }
  }'
```

### Python客户端示例

```python
import requests

# 准备学生profile
profile = """
学生 Profile
姓名：张小明
GPA：3.6
托福：95分
目标专业：计算机科学
"""

# 调用API
response = requests.post(
    "http://localhost:8000/invoke",
    json={
        "input": {
            "profile": profile,
            "llm_name": "openai",
            "debug": True
        }
    }
)

# 获取结果
result = response.json()
print(result["output"])
```

## 配置说明

### 环境变量

| 变量名 | 默认值 | 说明 |
|--------|--------|------|
| `HOST` | `0.0.0.0` | 服务监听地址 |
| `PORT` | `8000` | 服务端口 |
| `LANGSMITH_API_KEY` | - | LangSmith API密钥（可选） |
| `LANGCHAIN_ENDPOINT` | `https://api.smith.langchain.com` | LangSmith端点 |

~~~
LANGSMITH_TRACING=true
LANGSMITH_ENDPOINT="https://api.smith.langchain.com"
LANGSMITH_API_KEY="<your-api-key>"
OPENAI_API_KEY="<your-openai-api-key>"
~~~

### 支持的LLM模型

- `openai`: OpenAI GPT模型
- `gemini`: Google Gemini模型
- `deepseek`: DeepSeek模型
- `qwen`: 阿里通义千问模型

## 文件结构

```
university_selection_report/
├── university_selection_workflow.py  # 主workflow文件
├── start_langserve.py               # LangServe启动脚本
├── langserve_app.py                 # FastAPI应用（备用）
├── StudentProfile.txt               # 样例学生profile
└── README.md                       # 说明文档
```

## 开发说明

### 本地测试

```bash
# 直接运行workflow
python university_selection_workflow.py
```

### 自定义配置

可以修改 `university_selection_workflow.py` 中的以下参数：

- `llm_name`: 默认LLM模型
- `debug`: 调试模式
- `project_name`: LangSmith项目名称

### 扩展功能

1. **集成知识库**: 取消注释并实现 `UniversityKnowledge` 类
2. **学校归一化**: 取消注释并实现 `UniversityNormalization` 类
3. **自定义prompt**: 修改各方法中的prompt模板

## 故障排除

### 常见问题

1. **找不到langserve命令**
   ```bash
   pip install langserve
   ```

2. **LLM模型不可用**
   - 检查相关包是否安装
   - 确认API密钥设置正确

3. **LangSmith连接失败**
   - 检查网络连接
   - 确认API密钥有效
   - 服务仍可正常运行，只是不会记录到LangSmith

### 日志查看

启动时开启debug模式可以看到详细的执行日志：

```bash
export DEBUG=true
python start_langserve.py
```


# Langsmith
有集成langsmith, 可以在https://smith.langchain.com/查看日志。 langsmith是闭源的Saas服务，自行取舍。个人免费。

![langsmith](/screenshots/langsmith.png)

## 许可证

MIT License 