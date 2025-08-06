import subprocess

class Tool:
    def __init__(self, name, description):
        self.name = name
        self.description = description

    def use(self, input_text):
        raise NotImplementedError("Each tool must implement the use method")
    
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
            


    