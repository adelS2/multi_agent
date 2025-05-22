class ToolBase:
    name = "UnnamedTool"
    description = ""

    async def invoke(self, input_text: str) -> str:
        raise NotImplementedError("Tool muss 'invoke()' implementieren.")
