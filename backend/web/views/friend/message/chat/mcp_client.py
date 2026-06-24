import os

from langchain_mcp_adapters.client import MultiServerMCPClient

MAP_API_KEY = os.getenv("MAP_API_KEY")

async def load_amap_tools():

    client = MultiServerMCPClient(
        {
            "amap": {
                "command": "npx",
                "args": [
                    "-y",
                    "@amap/amap-maps-mcp-server"
                ],
                "env": {
                    "AMAP_MAPS_API_KEY": MAP_API_KEY
                },
                "transport": "stdio"
            }
        }
    )

    tools = await client.get_tools()

    return tools