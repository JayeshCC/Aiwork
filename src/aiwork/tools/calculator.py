from src.aiwork.tools.registry import tool_registry

@tool_registry.register("calculator")
class CalculatorTool:
    def run(self, payload: dict):
        expression = payload.get("expression")
        if not expression:
            return {"error": "Missing 'expression' field"}

        try:
            return {"result": eval(expression)}
        except Exception as e:
            return {"error": str(e)}
