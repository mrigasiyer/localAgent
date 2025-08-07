import requests
from tools import ShellTool, CalculatorTool

class Agent:
    def __init__(self, name="Agent", model="mistral"):
        self.name = name
        self.model = model
        self.tools = {
            "shell" : ShellTool(),
            "calc" : CalculatorTool()
        }

    def think(self, user_input):    

        tool_descriptions = "\n".join(
            f"- {tool.name} : {tool.description}"
            for tool in self.tools.values()
        )

        system_prompt = (
        "You are an autonomous AI agent that can choose tools to help the user.\n"
        "Available tools:\n"
        f"{tool_descriptions}\n\n"
        "When the user asks something, reply with a tool call like this:\n"
        "TOOL: <tool_name>\n"
        "INPUT: <input to pass to the tool>\n\n"
        "If no tool is needed, just respond directly.\n"
        )

        full_prompt = f"{system_prompt}User: {user_input}"
        
        response = requests.post("http://localhost:11434/api/generate", json={
            "model" : self.model,
            "prompt" : full_prompt,
            "stream" : False
        })

        if response.status_code != 200:
            return "[LLM ERROR]"
        
        output = response.json()["response"]
        print(f"[LLM OUTPUT]\n{output}")

        print("break")

        if output.strip().startswith("TOOL:"):
            try:
                tool_line, input_line = output.strip().split("\n", 1)
                tool_name = tool_line.replace("TOOL:", "").strip()
                lines = input_line.strip().split("\n")
                for line in lines:
                    if line.strip().startswith('INPUT:'):
                        tool_input = line.replace('INPUT:',"").strip()
                        break

                if tool_name in self.tools:
                    return self.tools[tool_name].use(tool_input)
                else:
                    return f"[ERROR] Tool ' {tool_name} ' not found"
                
            except Exception as e:
                return f"[ERROR] failed to parse tool call: {e}"

        return output.strip()


if __name__ == "__main__":
    agent = Agent("jarvis", "mistral")

    while True:
        user_input = input("\n Enter Prompt: ")
        if user_input.lower() in ["exit, quit"]:
            break

        print(f"{agent.name}: {agent.think(user_input)}")
        # output = agent.think(user_input)
        # print("Jarvis:", output)





