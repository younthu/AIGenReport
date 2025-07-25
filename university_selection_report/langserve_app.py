#!/usr/bin/env python3
"""
LangServe应用 - 美国本科留学选校报告生成服务
提供REST API接口，支持学生profile输入，返回完整的选校报告
"""

import os
import sys
from typing import Dict, Any
from fastapi import FastAPI
from langserve import add_routes
from pydantic import BaseModel, Field

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from university_selection_workflow import UniversitySelectionWorkflow


class StudentProfileRequest(BaseModel):
    """学生profile请求模型"""
    profile: str = Field(..., description="学生profile内容，可以是完整文本或文件路径")
    llm_name: str = Field(default="openai", description="使用的LLM模型名称")
    debug: bool = Field(default=False, description="是否开启调试模式")

# Rebuild model to ensure all references are resolved
StudentProfileRequest.model_rebuild()


class UniversitySelectionResponse(BaseModel):
    """选校报告响应模型"""
    report: str = Field(..., description="生成的完整选校报告")
    llm_used: str = Field(..., description="使用的LLM模型")
    debug_mode: bool = Field(..., description="调试模式状态")

# Rebuild model to ensure all references are resolved
UniversitySelectionResponse.model_rebuild()


class UniversitySelectionWorkflowService:
    """选校报告生成服务类"""
    
    def __init__(self):
        self.workflows = {}  # 缓存不同配置的workflow实例
    
    def _get_workflow(self, llm_name: str, debug: bool) -> UniversitySelectionWorkflow:
        """获取或创建workflow实例"""
        key = f"{llm_name}_{debug}"
        if key not in self.workflows:
            self.workflows[key] = UniversitySelectionWorkflow(
                llm_name=llm_name,
                debug=debug
            )
        return self.workflows[key]
    
    def generate_report(self, profile: str, llm_name: str = "openai", debug: bool = False) -> Dict[str, Any]:
        """生成选校报告"""
        try:
            workflow = self._get_workflow(llm_name, debug)
            report = workflow.run(profile)
            
            return {
                "report": report,
                "llm_used": llm_name,
                "debug_mode": debug,
                "status": "success"
            }
        except Exception as e:
            return {
                "report": "",
                "llm_used": llm_name,
                "debug_mode": debug,
                "status": "error",
                "error": str(e)
            }


# 创建FastAPI应用
app = FastAPI(
    title="美国本科留学选校报告生成服务",
    description="基于AI的美国本科留学选校报告生成API服务",
    version="1.0.0"
)

# 创建服务实例
service = UniversitySelectionWorkflowService()


@app.get("/")
async def root():
    """根路径，返回服务信息"""
    return {
        "service": "美国本科留学选校报告生成服务",
        "version": "1.0.0",
        "endpoints": {
            "/generate_report": "生成选校报告",
            "/health": "健康检查"
        }
    }


@app.get("/health")
async def health_check():
    """健康检查端点"""
    return {"status": "healthy", "service": "university-selection-workflow"}


@app.post("/generate_report", response_model=UniversitySelectionResponse)
async def generate_report(request: StudentProfileRequest):
    """生成选校报告的主要端点"""
    result = service.generate_report(
        profile=request.profile,
        llm_name=request.llm_name,
        debug=request.debug
    )
    
    if result["status"] == "error":
        raise Exception(f"报告生成失败: {result.get('error', '未知错误')}")
    
    return UniversitySelectionResponse(
        report=result["report"],
        llm_used=result["llm_used"],
        debug_mode=result["debug_mode"]
    )


from langchain_core.runnables import RunnableLambda

# 添加LangServe路由
add_routes(
    app,
    RunnableLambda(service.generate_report),
    path="/langserve/generate_report",
    input_type=StudentProfileRequest,
    output_type=UniversitySelectionResponse
)


if __name__ == "__main__":
    import uvicorn
    
    # 从环境变量获取配置
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    reload = os.getenv("RELOAD", "false").lower() == "true"
    
    print(f"启动选校报告生成服务...")
    print(f"服务地址: http://{host}:{port}")
    print(f"API文档: http://{host}:{port}/docs")
    print(f"健康检查: http://{host}:{port}/health")
    
    uvicorn.run(
        "langserve_app:app",
        host=host,
        port=port,
        reload=reload,
        log_level="info"
    )
