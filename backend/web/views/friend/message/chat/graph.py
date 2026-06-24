import os
import asyncio

from pprint import pprint

from django.conf import settings
from typing import TypedDict, Annotated, Sequence
from langchain_core.messages import BaseMessage
from langchain_openai import ChatOpenAI
from langgraph.constants import START, END
from langgraph.graph import add_messages, StateGraph
from langgraph.prebuilt import ToolNode

from web.views.friend.message.chat.ai_tool import get_time, search_knowledge_base, read_file, write_file, search_web, \
    execute_terminal_command
from web.views.friend.message.chat.mcp_client import load_amap_tools

class ChatGraph:
    @staticmethod
    def create_app():
        tools = [
            get_time,
            search_knowledge_base,
            read_file,
            write_file,
            search_web,
        ]

        if settings.DEBUG:
            tools.append(execute_terminal_command)

        try:
            amap_tools = asyncio.run(load_amap_tools())
            tools.extend(amap_tools)

        except Exception as e:
            print(f"加载高德MCP失败: {e}")

        llm = ChatOpenAI(
            model='deepseek-v4-flash',
            openai_api_key=os.getenv('API_KEY'),
            openai_api_base=os.getenv('API_BASE'),
            streaming=True,
            model_kwargs={
                "stream_options": {
                    "include_usage": True,  # 输出token消耗数量
                }
            }
        ).bind_tools(tools)

        class AgentState(TypedDict):
            messages: Annotated[Sequence[BaseMessage], add_messages]

        def model_call(state: AgentState) -> AgentState:
            pprint(state['messages'])
            res = llm.invoke(state['messages'])
            return {'messages': [res]}

        def should_continue(state: AgentState) -> str:
            last_message = state['messages'][-1]
            if last_message.tool_calls:
                return "tools"
            return "end"

        tool_node = ToolNode(tools)

        graph = StateGraph(AgentState)
        graph.add_node('agent', model_call)
        graph.add_node('tools', tool_node)

        graph.add_edge(START, 'agent')
        graph.add_conditional_edges(
            'agent',
            should_continue,
            {
                'tools': 'tools',
                'end': END,
            }
        )
        graph.add_edge('tools', 'agent')

        return graph.compile()
