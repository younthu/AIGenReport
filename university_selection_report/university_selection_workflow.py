import os
from typing import Union, Dict, Any
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.llms.base import BaseLLM

# Placeholders for future imports
# from normalization.university_normalization import UniversityNormalization
# from knowledge_base.university_knowledge import UniversityKnowledge

os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"

# LLM registry for switching
LLM_REGISTRY = {}

try:
    from langchain_openai import ChatOpenAI
    LLM_REGISTRY['openai'] = lambda: ChatOpenAI()
except ImportError:
    pass
try:
    from langchain_google_genai import ChatGoogleGenerativeAI
    LLM_REGISTRY['gemini'] = lambda: ChatGoogleGenerativeAI()
except ImportError:
    pass


def get_llm(llm_name: str) -> BaseLLM:
    if llm_name not in LLM_REGISTRY:
        raise ValueError(f"LLM '{llm_name}' is not supported or not installed.")
    return LLM_REGISTRY[llm_name]()


def read_profile(profile_input: str) -> str:
    if os.path.exists(profile_input):
        with open(profile_input, 'r', encoding='utf-8') as f:
            return f.read()
    return profile_input


class UniversitySelectionWorkflow:
    def __init__(self, llm_name: str = 'openai', debug: bool = True, project_name: str = "university-selection"):
        self.llm_name = llm_name
        self.llm = get_llm(llm_name)
        self.debug = debug
        self.project_name = project_name
        # self.univ_norm = UniversityNormalization()
        # self.univ_knowledge = UniversityKnowledge()
        
        # 设置LangSmith tracing
        self._setup_langsmith()

    def _setup_langsmith(self):
        """设置LangSmith tracing和observability"""
        # 设置LangSmith环境变量
        if not os.getenv("LANGSMITH_API_KEY"):
            print("[WARNING] LANGSMITH_API_KEY not set. LangSmith tracing will be disabled.")
            return
        
        # 设置项目名称
        os.environ["LANGCHAIN_PROJECT"] = self.project_name
        
        # 设置tracing
        os.environ["LANGCHAIN_TRACING_V2"] = "true"
        
        if self.debug:
            print(f"[DEBUG] LangSmith tracing enabled for project: {self.project_name}")

    def log(self, message: str, data: Any = None):
        if self.debug:
            print(f"[DEBUG] {message}")
            if data is not None:
                print(data)

    def recommend_majors(self, profile: str) -> str:
        """专业推荐章节 - 独立的LangSmith trace"""
        prompt = PromptTemplate(
            input_variables=["profile"],
            template=(
                "你是一名美国本科留学选校专家。根据以下学生profile，推荐3个最适合的专业，并给出每个专业的推荐理由。\n"
                "学生profile：\n{profile}\n"
                "请用markdown格式输出，包含专业名称和推荐理由。"
            )
        )
        chain = LLMChain(llm=self.llm, prompt=prompt)
        
        # 尝试记录到LangSmith（如果可用）
        try:
            if os.getenv("LANGSMITH_API_KEY"):
                # 使用LangChain内置的tracing
                from langchain.callbacks import LangChainTracer
                tracer = LangChainTracer()
                result = chain.run({"profile": profile}, callbacks=[tracer])
                self.log("专业推荐结果：", result)
                return result
        except Exception as e:
            if self.debug:
                print(f"[DEBUG] LangSmith tracing failed: {e}")
        
        # 如果没有LangSmith或出错，使用普通方式
        result = chain.run({"profile": profile})
        self.log("专业推荐结果：", result)
        return result

    def recommend_schools(self, profile: str, majors_report: str) -> str:
        """学校推荐章节 - 独立的LangSmith trace"""
        prompt = PromptTemplate(
            input_variables=["profile", "majors_report"],
            template=(
                "你是一名美国本科留学选校专家。根据以下学生profile和专业推荐报告，推荐1所保底学校，1所主申学校，1所冲刺学校，并给出推荐理由。\n"
                "学生profile：\n{profile}\n"
                "专业推荐报告：\n{majors_report}\n"
                "请用markdown格式输出，包含学校名称和推荐理由。"
            )
        )
        chain = LLMChain(llm=self.llm, prompt=prompt)
        
        # 尝试记录到LangSmith（如果可用）
        try:
            if os.getenv("LANGSMITH_API_KEY"):
                # 使用LangChain内置的tracing
                from langchain.callbacks import LangChainTracer
                tracer = LangChainTracer()
                result = chain.run({"profile": profile, "majors_report": majors_report}, callbacks=[tracer])
                self.log("学校推荐结果：", result)
                return result
        except Exception as e:
            if self.debug:
                print(f"[DEBUG] LangSmith tracing failed: {e}")
        
        # 如果没有LangSmith或出错，使用普通方式
        result = chain.run({"profile": profile, "majors_report": majors_report})
        self.log("学校推荐结果：", result)
        return result

    def fill_school_info(self, school_name: str, context: Dict[str, Any]) -> str:
        """学校信息填充章节 - 独立的LangSmith trace"""
        # Placeholder: context should include school json info from knowledge base
        prompt = PromptTemplate(
            input_variables=["school_name", "context"],
            template=(
                "你是一名美国本科留学选校专家。请根据以下学校信息，生成该校的选校报告章节，内容包括：\n"
                "1. 学校描述、简介\n2. 推荐理由\n3. 学校的历史招生数据\n4. 学校的录取要求\n5. 学校的录取率，亚洲学生录取概况\n"
                "学校名称：{school_name}\n学校信息：{context}\n"
                "请用markdown格式输出。"
            )
        )
        chain = LLMChain(llm=self.llm, prompt=prompt)
        
        # 尝试记录到LangSmith（如果可用）
        try:
            if os.getenv("LANGSMITH_API_KEY"):
                # 使用LangChain内置的tracing
                from langchain.callbacks import LangChainTracer
                tracer = LangChainTracer()
                result = chain.run({"school_name": school_name, "context": context}, callbacks=[tracer])
                self.log(f"学校 {school_name} 详细信息：", result)
                return result
        except Exception as e:
            if self.debug:
                print(f"[DEBUG] LangSmith tracing failed: {e}")
        
        # 如果没有LangSmith或出错，使用普通方式
        result = chain.run({"school_name": school_name, "context": context})
        self.log(f"学校 {school_name} 详细信息：", result)
        return result

    def extract_school_names(self, schools_report: str) -> list:
        """从学校推荐报告中提取学校名称"""
        import re
        
        # 方法1: 使用正则表达式提取学校名称
        # 匹配常见的学校名称模式
        patterns = [
            r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\s+(?:University|College|Institute))',
            r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\s+(?:大学|学院))',
            r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\s+(?:University|College))',
        ]
        
        school_names = []
        for pattern in patterns:
            matches = re.findall(pattern, schools_report, re.IGNORECASE)
            school_names.extend(matches)
        
        # 去重并过滤
        school_names = list(set(school_names))
        school_names = [name.strip() for name in school_names if len(name.strip()) > 3]
        
        # 如果正则表达式没有找到足够的学校，使用LLM提取
        if len(school_names) < 3:
            try:
                extract_prompt = PromptTemplate(
                    input_variables=["schools_report"],
                    template=(
                        "请从以下学校推荐报告中提取3所学校的名称。"
                        "只返回学校名称，每行一个，不要其他内容：\n\n"
                        "{schools_report}"
                    )
                )
                extract_chain = LLMChain(llm=self.llm, prompt=extract_prompt)
                extracted_text = extract_chain.run({"schools_report": schools_report})
                
                # 解析LLM返回的学校名称
                llm_schools = [line.strip() for line in extracted_text.split('\n') 
                              if line.strip() and len(line.strip()) > 3]
                school_names.extend(llm_schools[:3])
                school_names = list(set(school_names))  # 去重
                
            except Exception as e:
                if self.debug:
                    print(f"[DEBUG] LLM提取学校名称失败: {e}")
        
        # 如果还是没有找到足够的学校，使用默认名称
        if len(school_names) < 3:
            school_names = ["保底大学", "主申大学", "冲刺大学"]
            if self.debug:
                print("[DEBUG] 使用默认学校名称")
        
        # 确保返回3所学校
        while len(school_names) < 3:
            school_names.append("待定大学")
        
        return school_names[:3]

    def run(self, profile_input: str) -> str:
        """主workflow - 使用管道操作符连接各个步骤"""
        profile = read_profile(profile_input)
        self.log("学生profile：", profile)
        
        # 定义各个步骤的函数
        def recommend_majors_step(profile: str) -> str:
            """专业推荐步骤"""
            return self.recommend_majors(profile)
        
        def recommend_schools_step(inputs: dict) -> dict:
            """学校推荐步骤"""
            profile = inputs["profile"]
            majors_report = inputs["majors_report"]
            schools_report = self.recommend_schools(profile, majors_report)
            return {"profile": profile, "majors_report": majors_report, "schools_report": schools_report}
        
        def extract_schools_step(inputs: dict) -> dict:
            """提取学校名称步骤"""
            schools_report = inputs["schools_report"]
            school_names = self.extract_school_names(schools_report)
            self.log("提取的学校名称：", school_names)
            return {**inputs, "school_names": school_names}
        
        def fill_school_info_step(inputs: dict) -> dict:
            """填充学校信息步骤"""
            school_names = inputs["school_names"]
            school_sections = []
            
            for school in school_names:
                # context = self.univ_knowledge.query(school)  # Placeholder
                context = {"desc": "学校信息占位符"}
                section = self.fill_school_info(school, context)
                school_sections.append(section)
            
            full_school_report = "\n\n".join(school_sections)
            return {**inputs, "full_school_report": full_school_report}
        
        def generate_final_report_step(inputs: dict) -> str:
            """生成最终报告步骤"""
            majors_report = inputs["majors_report"]
            schools_report = inputs["schools_report"]
            full_school_report = inputs["full_school_report"]
            
            final_report = f"# 专业推荐报告\n\n{majors_report}\n\n# 选校报告\n\n{schools_report}\n\n{full_school_report}"
            self.log("最终报告：", final_report)
            return final_report
        
        # 尝试记录到LangSmith（如果可用）
        try:
            if os.getenv("LANGSMITH_API_KEY"):
                # 使用LangChain内置的tracing包装整个流程
                from langchain.callbacks import LangChainTracer
                tracer = LangChainTracer()
                
                # 创建管道流程
                from langchain.schema.runnable import RunnablePassthrough, RunnableLambda
                
                # 定义管道
                pipeline = (
                    {"profile": RunnablePassthrough()} 
                    | {"profile": RunnablePassthrough(), "majors_report": RunnableLambda(recommend_majors_step)}
                    | RunnableLambda(recommend_schools_step)
                    | RunnableLambda(extract_schools_step)
                    | RunnableLambda(fill_school_info_step)
                    | RunnableLambda(generate_final_report_step)
                )
                
                # 执行管道
                result = pipeline.invoke(profile, config={"callbacks": [tracer]})
                return result
                    
        except Exception as e:
            if self.debug:
                print(f"[DEBUG] LangSmith tracing failed: {e}")
        
        # 如果没有LangSmith或出错，使用普通方式
        # 定义管道（普通版本）
        def recommend_majors_step_plain(profile: str) -> str:
            """专业推荐步骤（普通版本）"""
            return self.recommend_majors(profile)
        
        def recommend_schools_step_plain(inputs: dict) -> dict:
            """学校推荐步骤（普通版本）"""
            profile = inputs["profile"]
            majors_report = inputs["majors_report"]
            schools_report = self.recommend_schools(profile, majors_report)
            return {"profile": profile, "majors_report": majors_report, "schools_report": schools_report}
        
        def extract_schools_step_plain(inputs: dict) -> dict:
            """提取学校名称步骤（普通版本）"""
            schools_report = inputs["schools_report"]
            school_names = self.extract_school_names(schools_report)
            self.log("提取的学校名称：", school_names)
            return {**inputs, "school_names": school_names}
        
        def fill_school_info_step_plain(inputs: dict) -> dict:
            """填充学校信息步骤（普通版本）"""
            school_names = inputs["school_names"]
            school_sections = []
            
            for school in school_names:
                # context = self.univ_knowledge.query(school)  # Placeholder
                context = {"desc": "学校信息占位符"}
                section = self.fill_school_info(school, context)
                school_sections.append(section)
            
            full_school_report = "\n\n".join(school_sections)
            return {**inputs, "full_school_report": full_school_report}
        
        def generate_final_report_step_plain(inputs: dict) -> str:
            """生成最终报告步骤（普通版本）"""
            majors_report = inputs["majors_report"]
            schools_report = inputs["schools_report"]
            full_school_report = inputs["full_school_report"]
            
            final_report = f"# 专业推荐报告\n\n{majors_report}\n\n# 选校报告\n\n{schools_report}\n\n{full_school_report}"
            self.log("最终报告：", final_report)
            return final_report
        
        # 创建普通管道流程
        from langchain.schema.runnable import RunnablePassthrough, RunnableLambda
        
        pipeline_plain = (
            {"profile": RunnablePassthrough()} 
            | {"profile": RunnablePassthrough(), "majors_report": RunnableLambda(recommend_majors_step_plain)}
            | RunnableLambda(recommend_schools_step_plain)
            | RunnableLambda(extract_schools_step_plain)
            | RunnableLambda(fill_school_info_step_plain)
            | RunnableLambda(generate_final_report_step_plain)
        )
        
        # 执行普通管道
        result = pipeline_plain.invoke(profile)
        return result


def main():
    # 默认使用openai（或Tongyi）模型，调试模式开启
    workflow = UniversitySelectionWorkflow(llm_name='openai', debug=True)
    # 使用样例profile文件
    profile_path = os.path.join(os.path.dirname(__file__), 'StudentProfile.txt')
    report = workflow.run(profile_path)
    output_path = os.path.join(os.path.dirname(__file__), 'UniversitySelectionReport.md')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(report)
    print("\n===== 生成的完整选校报告 =====\n")
    print(report)
    print(f"\n报告已保存为: {output_path}\n")

    # 尝试将Markdown渲染为PDF
    pdf_path = os.path.join(os.path.dirname(__file__), 'UniversitySelectionReport.pdf')
    
    # 尝试多种PDF生成方式
    pdf_generated = False
    
    # 方式1: 使用pypandoc
    if not pdf_generated:
        try:
            import importlib
            pypandoc = importlib.import_module('pypandoc')
            pypandoc.convert_file(output_path, 'pdf', outputfile=pdf_path)
            print(f"PDF已保存为: {pdf_path}\n")
            pdf_generated = True
        except ImportError:
            print("未检测到pypandoc库，尝试其他方式...")
        except Exception as e:
            if "No pandoc was found" in str(e):
                print("pandoc未安装，尝试其他方式...")
            else:
                print(f"pypandoc转换失败: {e}")
    
    # 方式2: 使用weasyprint
    if not pdf_generated:
        try:
            import weasyprint
            from markdown import markdown
            
            # 读取markdown内容
            with open(output_path, 'r', encoding='utf-8') as f:
                md_content = f.read()
            
            # 转换为HTML
            html_content = markdown(md_content, extensions=['tables', 'fenced_code'])
            
            # 添加CSS样式
            styled_html = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
                <style>
                    body {{ font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; }}
                    h1, h2, h3 {{ color: #333; }}
                    h1 {{ border-bottom: 2px solid #333; padding-bottom: 10px; }}
                    h2 {{ border-bottom: 1px solid #ccc; padding-bottom: 5px; }}
                    code {{ background-color: #f4f4f4; padding: 2px 4px; border-radius: 3px; }}
                    pre {{ background-color: #f4f4f4; padding: 10px; border-radius: 5px; overflow-x: auto; }}
                    blockquote {{ border-left: 4px solid #ccc; margin: 0; padding-left: 20px; }}
                </style>
            </head>
            <body>
                {html_content}
            </body>
            </html>
            """
            
            # 生成PDF
            weasyprint.HTML(string=styled_html).write_pdf(pdf_path)
            print(f"PDF已保存为: {pdf_path} (使用weasyprint)\n")
            pdf_generated = True
            
        except ImportError:
            print("未检测到weasyprint库，尝试其他方式...")
        except Exception as e:
            print(f"weasyprint转换失败: {e}")
    
    # 方式3: 使用markdown-pdf (如果可用)
    if not pdf_generated:
        try:
            import subprocess
            result = subprocess.run(['markdown-pdf', output_path, '-o', pdf_path], 
                                  capture_output=True, text=True, timeout=30)
            if result.returncode == 0:
                print(f"PDF已保存为: {pdf_path} (使用markdown-pdf)\n")
                pdf_generated = True
            else:
                print(f"markdown-pdf转换失败: {result.stderr}")
        except FileNotFoundError:
            print("未检测到markdown-pdf命令")
        except Exception as e:
            print(f"markdown-pdf转换失败: {e}")
    
    # 如果所有方式都失败，提供安装指导
    if not pdf_generated:
        print("\n=== PDF生成失败 ===\n")
        print("已尝试多种PDF生成方式，但都失败了。")
        print("\n要启用PDF生成，请安装以下工具之一：")
        print("\n1. pandoc + pypandoc:")
        print("   pip install pypandoc")
        print("   # 然后安装pandoc: https://pandoc.org/installing.html")
        print("\n2. weasyprint:")
        print("   pip install weasyprint markdown")
        print("\n3. markdown-pdf (Node.js):")
        print("   npm install -g markdown-pdf")
        print("\n4. 手动转换:")
        print("   可以使用在线工具如 https://www.markdowntopdf.com/")
        print("   或使用本地编辑器如Typora、VSCode等")
        print(f"\nMarkdown文件已保存为: {output_path}")
        print("可以手动将其转换为PDF。\n")

if __name__ == "__main__":
    main() 