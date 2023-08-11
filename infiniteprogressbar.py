import enum
from ConsoleGraphics.consoleelement import ConsoleElement
from ConsoleGraphics.funcs import tides, smooth_tides


class InfiniteProgressBarStyle:
    def _render(self, tick):
        return tick


class SnakeBar(InfiniteProgressBarStyle):
    def __init__(
        self,
        length=20,
        tides=False,
        rtl=False,
        spacelength=50,
        filler="⣿",
        tail="⣿⣾⣼⣸⢸⠸⠘⠈",
        head="⠁⠃⠇⡇⣇⣧⣷⣿",
        smooth_tides=False,
    ) -> None:
        self.length = length
        if length < 2:
            raise ValueError("Length cannot be less than 2")
        self.tides = tides
        self.rtl = rtl
        self.spacelength = spacelength
        self.filler = filler
        self.head = head
        self.tail = tail
        self.smooth_tides = smooth_tides

    def _render(self, tick, width):
        if self.tides:
            self.spacelength = width + self.length * 2
            self.rtl = False
            if self.smooth_tides:
                tick = int(smooth_tides(tick / 8, -self.length, width) * 8)
            else:
                tick = int(tides(tick / 8, -self.length * 1.5, width + self.length*.5) * 8)
        bar = [" "] * width
        if self.rtl:
            tick = -tick
        loop = (
            self.tail[tick % len(self.tail)]
            + self.filler * (self.length - 2)
            + self.head[tick % len(self.head)]
            + " " * self.spacelength
        )
        for col in range(width):
            bar[col] = loop[
                int((int((((7 if self.rtl else 0) - tick) / len(self.head))) + col))
                % (self.length + self.spacelength)
            ]

        return "".join(bar)


class SmoothBar(SnakeBar):
    def __init__(
        self,
        length=40,
        tides=False,
        rtl=False,
        spacelength=50,
        filler="█",
        #SMOOTHEST: █🮋🮊▐▐▐▕▕
        tail="███▐▐▐▕▕",
        head="▏▎▍▌▋▊▉█",
        smooth_tides=True,
    ):
        self.snakebar = SnakeBar(length, tides, rtl, spacelength, filler, tail, head, smooth_tides)
        
    def _render(self, tick, width):
        return self.snakebar._render(tick, width)


class InfiniteProgressField(enum.IntEnum):
    NONE = 0
    NAME = 1
    STEP = 2
    ELAPSED_TIME = 3


class InfiniteProgressBar(ConsoleElement):
    import time
    import os
    import ConsoleGraphics.consolescreen as consolescreen
    from threading import Thread
    from ConsoleGraphics.rect import Rect

    def __init__(
        self,
        name="Progress",
        step="First Step",
        speed=1,
        barstyle: InfiniteProgressBarStyle = SnakeBar(),
        borders="▕▏",
        reverse=False,
        leftfield: InfiniteProgressField = InfiniteProgressField.NAME,
        centerfield: InfiniteProgressField = InfiniteProgressField.STEP,
        rightfield: InfiniteProgressField = InfiniteProgressField.ELAPSED_TIME,
    ):
        self.name = name
        self.step = step
        self.borderleft = "" if len(borders) == 0 else borders[0]
        self.borderright = (
            "" if len(borders) == 0 else borders[0] if len(borders) == 1 else borders[1]
        )
        self.starttime = self.time.monotonic()
        self.finished = False
        self.leftfield = leftfield
        self.centerfield = centerfield
        self.rightfield = rightfield
        self.speed = speed
        self.reverse = reverse

        self.barstyle = barstyle

        self.fields = {0: ""}

        self._thread = None
        self.tick = 0
        self._tick = 0

    def next(self):
        self.tick += 1

    def finish(self):
        self.finished = True

    def _animate(self):
        while (not self.finished) and self.animating:
            self._printprogress(self.tick)
            self.next()
            self.time.sleep(0.01)

    def start(self):
        if self.finished:
            raise RuntimeError("Progress bar is already finished")
        self._thread = self.Thread(target=self._animate)
        self.animating = True
        self._thread.start()

    def stop(self):
        self.animating = False
        self._printprogress(self.tick)

    def _renderbar(self, tick, terminallength=None):
        if 1 in [self.leftfield, self.centerfield, self.rightfield]:
            self.fields[1] = self.name
        if 2 in [self.leftfield, self.centerfield, self.rightfield]:
            self.fields[2] = self.step
        if 3 in [self.leftfield, self.centerfield, self.rightfield] or 8 in [
            self.leftfield,
            self.centerfield,
            self.rightfield,
        ]:
            a = self.time.monotonic() - self.starttime
            self.fields[3] = (
                str(int(a / 3600)).rjust(3, "0")
                + ":"
                + str(int(a / 60) - int(a / 3600) * 60).rjust(2, "0")
                + ":"
                + str(int(a) - int(a / 60) * 60).rjust(2, "0")
                + " et."
            )

        leftfield = self.fields[self.leftfield] + " " if self.leftfield != 0 else ""
        centerfield = (
            (" " if self.centerfield != 0 else "") + self.fields[self.centerfield] + " "
            if self.centerfield != 0
            else ""
        )
        rightfield = (" " if self.rightfield != 0 else "") + self.fields[
            self.rightfield
        ]

        terminal = (
            self.os.get_terminal_size().columns
            if terminallength is None
            else terminallength
        )
        text = "\r" + leftfield + self.borderleft
        terminal -= (
            len(leftfield)
            + len(self.borderleft)
            + len(self.borderright)
            + len(rightfield)
        )
        text += self.consolescreen.center_text(
            self.barstyle._render(tick, terminal-1), centerfield
        )
        text += self.borderright + f"{rightfield}"
        return text[:self.os.get_terminal_size().columns if terminallength is None else terminallength]

    def _printprogress(self, tick):
        text = self._renderbar(tick)
        print(text, end="")

    def _renderforconsole(self, window, deltatime):
        text = self._renderbar(self.tick)
        self._tick += deltatime * 10 * self.speed * (-1 if self.reverse else 1)
        self.tick = int(self._tick)
        window.addstr(self.line, 0, text)

    def print(self):
        self._printprogress(self.progress)

    def rect(self):
        return self.Rect(1, self.os.get_terminal_size().columns, self.line, 0)