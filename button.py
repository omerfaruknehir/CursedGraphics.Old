from ConsoleGraphics.consoleelement import ConsoleElement

class Button(ConsoleElement):
    import os
    import ConsoleGraphics.consolescreen as consolescreen
    import curses
    from ConsoleGraphics.rect import Rect

    def __init__(
        self,
        text="Click me!",
        y=0,
        x=0,
        width=13,
        height=3,
        backgroundcolor=(0, 0, 0),
        textcolor=(0, 0, 0),
        clickable=True,
        onclick=None,
    ):
        self.text = text
        self.y = y
        self.x = x
        self.width = width
        self.height = height
        self.backgroundcolor = backgroundcolor
        self.textcolor = textcolor
        self.clickable = clickable
        self.onclickevent = onclick
    
    def rect(self):
        return self.Rect(self.height, self.width, self.y, self.x)

    def _renderbutton(self):
        text = (" " * self.width + "\n") * int((self.height - 1) / 2)
        text += self.consolescreen.center_text((" " * self.width), self.text.replace("\\", "\\\\")) + "\n"
        text += (" " * self.width + "\n") * (self.height - int((self.height) / 2))

        return text

    def _renderforconsole(self, window, deltatime):
        maxwidth = max(
            0, min(self.width + self.x, self.os.get_terminal_size().columns) - self.x
        )
        maxheight = max(
            0, min(self.height + self.y, self.os.get_terminal_size().lines) - self.y
        )

        text = self._renderbutton()

        self.curses.init_pair(99, 230, 255)

        y = self.y
        for line in text.split("\n"):
            if y > maxheight-1:
                break
            window.addstr(y, self.x, line[:maxwidth], self.curses.color_pair(99) | self.curses.A_BOLD)
            y += 1

    def onclick(self, e):
        if self.onclickevent != None:
            self.onclickevent()