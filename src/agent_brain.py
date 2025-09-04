import requests
from tools import ShellTool, CalculatorTool

#definig Agent class
class Agent:
    def __init__(self, name="Agent", model="mistral"):
        self.name = name
        self.model = model
        self.tools = {
            "shell" : ShellTool(),
            "calc" : CalculatorTool()
        }

    #method for thinking: gives LLM prompt to generate an input either for tools or to give an output of its own
    def think(self, user_input):    
        history = []

        #loop for multiple thinking sessions
        for _ in range(5):
            #dic of all tools
            tool_descriptions = "\n".join(
                f"- {tool.name} : {tool.description}"
                for tool in self.tools.values()
            )

            tool_history = "\n".join(history)

            system_prompt = (
                "You are an autonomous AI agent that can choose tools to help the user.\n"
                "Available tools:\n"
                f"{tool_descriptions}\n\n"
                "When the user asks something, respond like this:\n"
                "TOOL: <tool_name>\n"
                "INPUT: <input to pass to the tool>\n\n"
                "If you're done, respond with your final answer as plain text.\n\n"
                f"{tool_history}\n"
            )

            full_prompt = f"{system_prompt}User: {user_input}"
            
            #post to OLlama server
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

            #if tool being used
            if output.strip().startswith("TOOL:"):
                try:
                    tool_line, input_line = output.strip().split("\n", 1)
                    tool_name = tool_line.replace("TOOL:", "").strip()
                    lines = input_line.strip().split("\n")
                    #ignore any input after tool input
                    for line in lines:
                        if line.strip().startswith('INPUT:'):
                            tool_input = line.replace('INPUT:',"").strip()
                            break

                    if tool_name in self.tools:
                        tool_result = self.tools[tool_name].use(tool_input)
                        history.append(
                            f"Tool used: {tool_name}\nInput: {tool_input}\nOutput {tool_result}\n"
                        )
                    else:
                        return f"[ERROR] Tool ' {tool_name} ' not found"
                    
                except Exception as e:
                    return f"[ERROR] failed to parse tool call: {e}"
            else: 
                return output.strip()


if __name__ == "__main__":
    agent = Agent("jarvis", "mistral")

    while True:
        user_input = input("\n Enter Prompt: ")
        if user_input.lower() in ["exit, quit"]:
            break

        print(f"{agent.name}: {agent.think(user_input)}")





