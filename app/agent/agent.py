from app.agent.prompt import build_prompt
from app.agent.parser import parse_action

class Agent:
    def __init__(self, llm, tools):
        self.llm = llm
        self.tools = {t.name: t for t in tools}
        self.memory = []

    def run(self, input_data):
        goal = "Analyze bitcoin news and generate final report"

        for step in range(5):
            prompt = build_prompt(goal, self.tools.values(), self.memory, input_data)

            response = self.llm.generate(prompt)

            action = parse_action(response)

            if not action:
                raise Exception("Invalid agent response")

            tool_name = action["tool"]
            tool_input = action.get("input", {})

            if tool_name == "finish":
                return tool_input

            if tool_name not in self.tools:
                raise Exception(f"Unknown tool {tool_name}")

            result = self.tools[tool_name].run({
                **input_data,
                **tool_input
            })

            self.memory.append(response)
            self.memory.append(f"Observation: {result}")

        raise Exception("Max steps reached")