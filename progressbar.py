import enum
from ConsoleGraphics.consoleelement import ConsoleElement


class ProgressField(enum.IntEnum):
    NONE = 0
    NAME = 1
    STEP = 2
    PROGRESS_NUMBER = 3
    PROGRESS_NUMBER_AND_LENGTH = 4
    PROGRESS_PERCENT = 5
    ELAPSED_TIME = 6
    ESTIMATED_TIME = 7
    ELAPSED_AND_ESTIMATED_FULL_TIME = 8


class ProgressBar(ConsoleElement):
    import time
    import os
    import ConsoleGraphics.consolescreen as consolescreen
    from threading import Thread
    import math
    from ConsoleGraphics.rect import Rect

    def __init__(
        self,
        length=100,
        name="Progress",
        step="First Step",
        chars="▏▎▍▌▋▊▉█",
        # chars = "⠁⠃⠇⡇⣇⣧⣷⣿",
        # chars = "\|/-",
        borders="▕▏",
        leftfield: ProgressField = ProgressField.NAME,
        centerfield: ProgressField = ProgressField.PROGRESS_PERCENT,
        rightfield: ProgressField = ProgressField.ELAPSED_AND_ESTIMATED_FULL_TIME,
        smoothness=0,
    ):
        self.length = length
        self.progress = 0
        self.animatedPos = 0
        self.name = name
        self.step = step
        self.chars = chars if chars != "snake" else "⠁⠃⠇⡇⣇⣧⣷⣿"
        if borders == "snake":
            self.borderleft = "⢸"
            self.borderright = "⡇"
        else:
            self.borderleft = "" if len(borders) == 0 else borders[0]
            self.borderright = (
                ""
                if len(borders) == 0
                else borders[0]
                if len(borders) == 1
                else borders[1]
            )
        self.starttime = self.time.monotonic()
        self.finished = False
        self.leftfield = leftfield
        self.centerfield = centerfield
        self.rightfield = rightfield

        self.fields = {0: ""}

        if smoothness < 0:
            raise ValueError("smoothness musn't be negative")
        self.smoothness = smoothness
        self.animating = False

        self._thread = None

    def setprogress(self, progress):
        self.progress = min(progress, self.length)

    def setstep(self, step):
        self.step = step

    def _animate(self):
        self.animatedPos = self.progress
        while (not self.finished) and self.animating:
            if self.smoothness > 0:
                self.animatedPos = (
                    self.math.ceil(
                        (
                            (self.progress + self.animatedPos * self.smoothness)
                            / (self.smoothness + 1)
                        )
                        * 10.0
                    )
                    / 10.0
                )
            else:
                self.animatedPos = self.progress
            self._printprogress(self.animatedPos)
            if self.animatedPos >= self.length:
                print()
                self.finished = True
            self.time.sleep(0.01)

    def start(self):
        self._thread = self.Thread(target=self._animate)
        self.animating = True
        self._thread.start()

    def stop(self):
        self.animating = False
        self._printprogress(self.progress)

    def _renderbar(self, progress, terminallength=None):
        if 1 in [self.leftfield, self.centerfield, self.rightfield]:
            self.fields[1] = self.name
        if 2 in [self.leftfield, self.centerfield, self.rightfield]:
            self.fields[2] = self.step
        if 3 in [self.leftfield, self.centerfield, self.rightfield]:
            self.fields[3] = str(self.progress)
        if 4 in [self.leftfield, self.centerfield, self.rightfield]:
            self.fields[4] = str(self.progress) + "/" + str(self.length)
        if 5 in [self.leftfield, self.centerfield, self.rightfield]:
            self.fields[5] = f"{((self.progress / self.length) * 100):.1f}%"
        if 6 in [self.leftfield, self.centerfield, self.rightfield] or 8 in [
            self.leftfield,
            self.centerfield,
            self.rightfield,
        ]:
            a = self.time.monotonic() - self.starttime
            self.fields[6] = (
                str(int(a / 3600)).rjust(3, "0")
                + ":"
                + str(int(a / 60) - int(a / 3600) * 60).rjust(2, "0")
                + ":"
                + str(int(a) - int(a / 60) * 60).rjust(2, "0")
                + " et."
            )
        if 7 in [self.leftfield, self.centerfield, self.rightfield]:
            if self.progress == 0:
                self.fields[7] = "∞∞∞:∞∞:∞∞ est."
            else:
                a = ((self.time.monotonic() - self.starttime) / self.progress) * (
                    self.length - self.progress
                )
                self.fields[7] = (
                    str(int(a / 3600)).rjust(3, "0")
                    + ":"
                    + str(int(a / 60) - int(a / 3600) * 60).rjust(2, "0")
                    + ":"
                    + str(int(a) - int(a / 60) * 60).rjust(2, "0")
                    + " est."
                )
        if 8 in [self.leftfield, self.centerfield, self.rightfield]:
            if self.progress == 0:
                self.fields[8] = self.fields[6] + " / ∞∞∞:∞∞:∞∞ est."
            else:
                a = ((self.time.monotonic() - self.starttime) / self.progress) * (
                    self.length
                )
                self.fields[8] = (
                    self.fields[6]
                    + " / "
                    + str(int(a / 3600)).rjust(3, "0")
                    + ":"
                    + str(int(a / 60) - int(a / 3600) * 60).rjust(2, "0")
                    + ":"
                    + str(int(a) - int(a / 60) * 60).rjust(2, "0")
                    + " est."
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
        terminal -= len(leftfield) + len(self.borderleft) + len(self.borderright) + len(rightfield)
        text += self.chars[-1] * (progress / self.length * terminal).__floor__()
        odd = float((progress / self.length) * terminal) - int(
            (progress / self.length) * terminal
        )
        if odd > 0:
            text += self.chars[int(odd * len(self.chars))]
        text += " " * int(terminal - float((progress / self.length) * terminal))
        text = text[: len(leftfield) + 1] + self.consolescreen.center_text(
            text[len(leftfield) + 1 :], centerfield
        )
        text += self.borderright + f"{rightfield}"
        return text

    def _printprogress(self, progress):
        text = self._renderbar(progress)
        print(text, end="")

    def _renderforconsole(self, window, deltatime):
        if self.smoothness > 0:
            self.animatedPos = (
                self.math.ceil(
                    (
                        (self.progress + self.animatedPos * (self.smoothness))
                        / ((self.smoothness) + 1)
                    )
                    * 10.0
                )
                / 10.0
            )
        else:
            self.animatedPos = self.progress
        text = self._renderbar(self.animatedPos)
        if self.animatedPos >= self.length:
            self.finished = True
        window.addstr(self.line, 0, text)

    def print(self):
        self._printprogress(self.progress)
        if self.progress >= self.length:
            print()
            self.finished = True
        
    def onclick(self, event):
        return super().onclick(event)

    def rect(self):
        return self.Rect(1, self.os.get_terminal_size().columns, self.line, 0)