#!/usr/bin/env python3
"""Flash user-entered text as Morse code on a Raspberry Pi LED."""

import threading
import time
import tkinter as tk
from pathlib import Path
import sys

from gpiozero import LED

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from projects.common.logic import encode_morse  # noqa: E402

LED_PIN = 23
MAX_CHARACTERS = 12
UNIT_SECONDS = 0.25


class MorseGui:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.led = LED(LED_PIN)
        self.text = tk.StringVar()
        self.status = tk.StringVar(value="Ready")

        root.title("Morse Code LED")
        root.protocol("WM_DELETE_WINDOW", self.close)

        tk.Label(root, text="Text to flash (maximum 12 characters):").grid(
            row=0, column=0, padx=12, pady=(12, 4)
        )
        tk.Entry(root, textvariable=self.text, width=24).grid(
            row=1, column=0, padx=12, pady=4
        )
        self.start_button = tk.Button(root, text="Flash Morse", command=self.start)
        self.start_button.grid(row=2, column=0, padx=12, pady=4)
        tk.Label(root, textvariable=self.status).grid(row=3, column=0, padx=12, pady=4)
        tk.Button(root, text="Exit", command=self.close).grid(
            row=4, column=0, padx=12, pady=(4, 12)
        )

    def start(self) -> None:
        message = self.text.get().strip()
        if not message:
            self.status.set("Enter a message.")
            return
        if len(message) > MAX_CHARACTERS:
            self.status.set("Message is longer than 12 characters.")
            return

        try:
            tokens = encode_morse(message)
        except ValueError as exc:
            self.status.set(str(exc))
            return

        self.start_button.config(state=tk.DISABLED)
        self.status.set("Flashing...")
        threading.Thread(target=self.flash_tokens, args=(tokens,), daemon=True).start()

    def flash_tokens(self, tokens: list[str]) -> None:
        try:
            for token in tokens:
                if token == "/":
                    time.sleep(7 * UNIT_SECONDS)
                    continue

                for symbol in token:
                    self.led.on()
                    time.sleep((3 if symbol == "-" else 1) * UNIT_SECONDS)
                    self.led.off()
                    time.sleep(UNIT_SECONDS)
                time.sleep(2 * UNIT_SECONDS)
        finally:
            self.led.off()
            self.root.after(0, self.finish)

    def finish(self) -> None:
        self.status.set("Complete")
        self.start_button.config(state=tk.NORMAL)

    def close(self) -> None:
        self.led.off()
        self.led.close()
        self.root.destroy()


def main() -> None:
    root = tk.Tk()
    MorseGui(root)
    root.mainloop()


if __name__ == "__main__":
    main()
