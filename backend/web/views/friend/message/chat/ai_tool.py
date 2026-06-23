import os
import httpx
import lancedb
from dotenv import load_dotenv
from pathlib import Path
import platform
import subprocess
from langchain_core.tools import tool
from django.utils.timezone import now, localtime
from langchain_community.vectorstores import LanceDB
from web.documents.utils.custom_embeddings import CustomEmbeddings
from web.views.friend.message.chat.risk_level import calculate_risk

PROJECT_ROOT = Path(__file__).resolve().parents[5]
FILE_DIR = PROJECT_ROOT / "media" / "documents"
load_dotenv()
SEARCH_API_KEY = os.getenv("SEARCH_API_KEY")
SEARCH_API_URL = "https://www.searchapi.io/api/v1/search"

@tool
def get_time() -> str:
    """当需要查询精确时间时，调用此函数。返回格式为：[年-月-日 时:分:秒]"""
    return localtime(now()).strftime('%Y-%m-%d %H:%M:%S')

@tool
def search_knowledge_base(query: str) -> str:
    """当用户查询苏州大学的相关信息时，调用此函数。输入为要查询的问题，输出为查询结果。"""
    db = lancedb.connect('./web/documents/lancedb_storage')
    embeddings = CustomEmbeddings()
    vector_db = LanceDB(
        connection=db,
        embedding=embeddings,
        table_name='my_knowledge_base',
    )
    docs = vector_db.similarity_search(query, k=3)
    context = '\n\n'.join([f'内容片段：{i + 1}\n{doc.page_content}' for i, doc in enumerate(docs)])
    return f'从知识库中找到以下相关信息：\n\n{context}\n'

@tool
def read_file(file_name: str) -> str:
    """
    当需要查看、分析、总结已有文件内容时调用此工具。

    参数:
        file_name: 待读取的文件名称

    返回:
        文件完整内容
    """
    try:
        file_path = FILE_DIR / file_name
        print(file_path)
        if not file_path.exists():
            return f"文件不存在：{file_name}"

        return file_path.read_text(
            encoding="utf-8"
        )

    except Exception as e:
        return f"读取文件失败：{str(e)}"

@tool
def write_file(file_name: str, content: str) -> str:
    """
    当需要创建文件、保存代码、保存文档、更新文件内容时调用此工具。

    参数:
        file_name: 文件名称
        content: 文件内容

    返回:
        文件保存结果
    """
    try:
        FILE_DIR.mkdir(
            parents=True,
            exist_ok=True
        )

        file_path = FILE_DIR / file_name

        file_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        file_path.write_text(
            content,
            encoding="utf-8"
        )

        return f"文件已成功保存到：{file_path}"

    except Exception as e:
        return f"写入文件失败：{str(e)}"

@tool
def search_web(query: str) -> str:
    """
    当需要搜索最新信息、外部知识、网络资料、新闻或无法确定的事实时调用此工具。

    适用场景：
    - 查询实时信息（新闻、事件、价格等）
    - 查找无法从本地知识回答的问题
    - 获取外部网页内容摘要
    - 补充背景知识

    参数:
        query: 搜索关键词（自然语言或短语）

    返回:
        返回搜索结果的前5条结构化信息（JSON字符串拼接）
    """

    try:
        params = {
            "q": query,
            "api_key": SEARCH_API_KEY,
            "engine": "baidu"
        }

        response = httpx.get(SEARCH_API_URL, params=params, timeout=10)
        response.raise_for_status()

        data = response.json()

        organic_results = data.get("organic_results", [])

        # 取前5条
        top_results = organic_results[:5]

        # 拼接结果（保持和Java一致的行为）
        result = ",".join(
            str(item) for item in top_results
        )

        return result if result else "未找到相关搜索结果"

    except Exception as e:
        return f"搜索失败：{str(e)}"

@tool
def execute_terminal_command(command: str) -> str:
    """
    当需要执行系统命令、调试程序、运行脚本、查看环境时调用。

    ⚠️ 安全规则：
    - 系统会对命令进行风险评分
    - 高风险命令会被阻止执行
    - 请优先使用安全命令（ls, pwd, python, git status等）

    返回：
    - 执行结果
    - 或安全拦截信息
    """

    try:
        risk_score, reason = calculate_risk(command)

        # ❌ 强制阻断
        if risk_score >= 80:
            return f"""
            ❌ 命令被阻止执行
            
            Risk Score: {risk_score}/100
            Reason: {reason}
            Command: {command}
            """

        # ⚠️ 高风险提示但允许执行
        if risk_score >= 50:
            warning = f"[WARNING] High risk command (score={risk_score})\n{reason}\n\n"
        else:
            warning = ""

        system = platform.system().lower()

        if system == "windows":
            process = subprocess.Popen(
                ["cmd.exe", "/c", command],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
        else:
            process = subprocess.Popen(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

        stdout, stderr = process.communicate()

        output = warning

        if stdout:
            output += stdout

        if stderr:
            output += "\n[stderr]\n" + stderr

        output += f"\n\nRisk Score: {risk_score}/100\nReason: {reason}"

        return output.strip()

    except Exception as e:
        return f"执行失败：{str(e)}"
