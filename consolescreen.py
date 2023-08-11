import curses, time
import threading
from ConsoleGraphics.consoleelement import ConsoleElement
import ConsoleGraphics.events

def center_text(main_text, sub_text):
    padding = (len(main_text) - len(sub_text)) // 2
    centered_text = (
        main_text[:padding] + sub_text + main_text[padding + len(sub_text) :]
    )
    return centered_text

class ConsoleScreen:
    def __init__(self, name, backgroundcolor = curses.COLOR_BLACK):
        self.name = name
        self.wrapper = None
        self.backgroundcolor = backgroundcolor
        self.elements = []
        self.run = False
    
    def click(self, pos, button):
        for element in self.elements:
            if element.rect().contains(pos[0], pos[1]):
                print(element.rect())
                print(pos)
                if element.onclick:
                    element.onclick(ConsoleGraphics.events.clickeventdata(button, pos))

    def hover(self, pos):
        pass

    def main(self, win: curses.window):
        curses.curs_set(0)
        curses.mousemask(1)
        win.keypad(1)
        curses.curs_set(0) 
        curses.mousemask(curses.ALL_MOUSE_EVENTS)
        curses.halfdelay(1)

        pressed = False
        isright = False
        lastpos = (0, 0)
        button = -1
        "▁▃▄▅▆▇█▇▆▅▄▃▁"
        txt = " -=+0+=- "
        tick = time.monotonic_ns()
        while self.run:
            win.clear()
            curses.init_pair(1, curses.COLOR_WHITE, self.backgroundcolor)
            win.bkgd(' ', curses.color_pair(1) | curses.A_BOLD)
            win.addstr(0, int((win.getmaxyx()[1]-len(self.name))/2), self.name)
            for element in self.elements:
                element._renderforconsole(win, (time.monotonic_ns() - tick) / 1000000000)
            win.refresh()
            key = win.getch()
            if key == 27:
                break
            elif key == curses.KEY_MOUSE:
                _, mx, my, _, event = curses.getmouse()
                if (event & curses.BUTTON1_CLICKED != 0):
                    if pressed:
                        if (button != 1):
                            pressed = True
                            lastpos = (mx, my)
                            button = 1
                            isright = True
                        if not (abs(lastpos[0] - mx) <= 1 and abs(lastpos[1] - my) <= 1):
                            isright = False
                            win.refresh()
                        pressed = True
                    else:
                        pressed = True
                        button = 1
                        lastpos = (mx, my)
                        isright = True
                elif (event & curses.BUTTON3_CLICKED != 0):
                    if pressed:
                        if (button != 3):
                            pressed = True
                            lastpos = (mx, my)
                            button = 3
                            isright = True
                        if not (abs(lastpos[0] - mx) <= 1 and abs(lastpos[1] - my) <= 1):
                            isright = False
                            win.refresh()
                        pressed = True
                    else:
                        pressed = True
                        lastpos = (mx, my)
                        button = 3
                        isright = True
            else:
                if isright and pressed:
                    self.click((my, mx), button)
                    win.refresh()
                pressed = False
                _, mx, my, _, event = curses.getmouse()
                self.hover((my, mx))
            tick = time.monotonic_ns()
            time.sleep(0.01)
    
    def addelement(self, element:ConsoleElement, line:int):
        self.elements.append(element)
        element.line = line
    
    def _start(self):
        self.wrapper = curses.wrapper(self.main)
    
    def start(self):
        self.thread = threading.Thread(target=self._start)
        self.run = True
        self.thread.start()
    
    def stop(self):
        self.run = False
        curses.endwin()