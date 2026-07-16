#!/usr/bin/env python3
"""Tkinter controller for three Raspberry Pi LEDs."""

import tkinter as tk
from gpiozero import LED

BLUE_PIN = 17
RED_PIN = 27
GREEN_PIN = 23


class LedController:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.leds = {
            "Red": LED(RED_PIN),
            "Green": LED(GREEN_PIN),
            "Blue": LED(BLUE_PIN),
        }

        root.title("Raspberry Pi LED Controller")
        root.protocol("WM_DELETE_WINDOW", self.close)

        self.selection = tk.StringVar(value="Off")
        for row, name in enumerate((*self.leds.keys(), "Off")):
            tk.Radiobutton(
                root,
                text=f"{name}",
                variable=self.selection,
                value=name,
                command=self.apply_selection,
            ).grid(row=row, column=0, sticky="w", padx=12, pady=4)

        tk.Button(root, text="Exit", command=self.close).grid(
            row=4, column=0, padx=12, pady=12
        )

    def apply_selection(self) -> None:
        for led in self.leds.values():
            led.off()

        selected = self.selection.get()
        if selected in self.leds:
            self.leds[selected].on()

    def close(self) -> None:
        for led in self.leds.values():
            led.off()
            led.close()
        self.root.destroy()


def main() -> None:
    root = tk.Tk()
    LedController(root)
    root.mainloop()


if __name__ == "__main__":
    main()
