import requests
from src.tools import ShellTool

class Agent:
    def __init__(self, name="Agent", model="mistral"):
        self.name = name
        self.model = model
        self.tools = {
            "shell" : ShellTool()
        }

    def think(self, prompt):

        if prompt.startswith("!shell"):
            command = prompt.replace("!shell", "").strip()
            return self.tools["shell"].use(command)

        print(f"[{self.name}] Thinking about: {prompt} ")
        response = requests.post("http://localhost:11434/api/generate", json={
            "model" : self.model,
            "prompt" : prompt,
            "stream" : False
        })

        if response.status_code == 200:
            return response.json()["response"]
        else:
            return f"[ERROR] LLM failed: {response.text}"
        

if __name__ == "__main__":
    agent = Agent("jarvis", "mistral")

    while True:
        user_input = input("\n Enter Prompt: ")
        if user_input.lower() in ["exit, quit"]:
            break

        output = agent.think(user_input)
        print("Jarvis:", output)





