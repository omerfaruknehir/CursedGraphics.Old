class ConsoleElement:
    def __init__(self, line):
        self.line = line

    def _renderforconsole(self, window, deltatime):
        window.addstr(0, self.line, "CONTEXT")
    
    def onclick(self, event):
        pass