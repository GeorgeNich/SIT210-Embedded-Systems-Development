"""Hardware-independent helper functions used by the portfolio examples."""

MORSE = {
    "a": ".-", "b": "-...", "c": "-.-.", "d": "-..", "e": ".",
    "f": "..-.", "g": "--.", "h": "....", "i": "..", "j": ".---",
    "k": "-.-", "l": ".-..", "m": "--", "n": "-.", "o": "---",
    "p": ".--.", "q": "--.-", "r": ".-.", "s": "...", "t": "-",
    "u": "..-", "v": "...-", "w": ".--", "x": "-..-", "y": "-.--",
    "z": "--..", "0": "-----", "1": ".----", "2": "..---",
    "3": "...--", "4": "....-", "5": ".....", "6": "-....",
    "7": "--...", "8": "---..", "9": "----.",
}


def encode_morse(text: str) -> list[str]:
    """Return Morse tokens; `/` represents a word break.

    Raises:
        ValueError: if text contains an unsupported character.
    """
    tokens: list[str] = []
    for char in text.strip().lower():
        if char == " ":
            tokens.append("/")
        elif char in MORSE:
            tokens.append(MORSE[char])
        else:
            raise ValueError(f"Unsupported Morse character: {char!r}")
    return tokens


def classify_lux(lux: float) -> str:
    """Classify a BH1750 reading with complete, non-overlapping ranges."""
    if lux >= 1000:
        return "Too bright"
    if lux >= 300:
        return "Bright"
    if lux >= 100:
        return "Medium"
    if lux >= 30:
        return "Dark"
    return "Too dark"


def distance_cm(pulse_seconds: float) -> float:
    """Convert ultrasonic round-trip time in seconds to centimetres."""
    if pulse_seconds < 0:
        raise ValueError("Pulse duration cannot be negative")
    return round(pulse_seconds * 17150, 2)
