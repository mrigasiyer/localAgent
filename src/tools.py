import subprocess
import math

class Tool:
    def __init__(self, name, description):
        self.name = name
        self.description = description

    def use(self, input_text):
        raise NotImplementedError("Each tool must implement the use method")
    
    def as_dict(self):
        return{
            "name" : self.name,
            "description" : self.description
        }
    
class ShellTool(Tool):
    def __init__(self):
        super().__init__("shell", "Run terminal shell commands")

    def use(self, command):
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=10)
            if result.returncode != 0:
                return f"[ERROR] {result.stderr.strip()}"
            return result.stdout.strip()
        except Exception as e:
            return f"[EXCEPTION] {str(e)}"
    
class CalculatorTool(Tool):
    def __init__(self):
        super().__init__("calc", "Do basic math. Input should be math expressions like 2+2 or 3 * (4 + 5)")

    def use(self, command):
        try:
            allowed_names = {}
            for k,v in math.__dict__.items():
                if not k.startswith("__"):
                    allowed_names[k] = v

            allowed_names.update({
                "abs" : abs,
                "round" : round
            })

            result = eval(command, {"__builtins__": {}}, allowed_names)

            return f"Result: {result}"
            
        except Exception as e:
            return f"[CALCULATOR ERROR] {e}"


    