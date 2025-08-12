from dataclasses import dataclass, field

@dataclass
class GameState:
    secret: str
    attempts: int = 6
    used: set = field(default_factory=set)
    progress: list = field(default_factory=list)

    def __post_init__(self):
        if not self.progress:
            self.progress = ["_" for _ in self.secret]

    def finished(self) -> bool:
        return self.attempts <= 0 or "_" not in self.progress

    def won(self) -> bool:
        return "_" not in self.progress

def normalize_letter(ch: str) -> str:
    return ch.lower().strip()

def try_letter(state: GameState, ch: str) -> tuple[bool, str]:
    ch = normalize_letter(ch)
    if len(ch) != 1 or not ch.isalpha():
        return False, "Ingresa solo una letra."
    if ch in state.used:
        return False, "Letra repetida."
    state.used.add(ch)
    if ch in state.secret:
        for i, c in enumerate(state.secret):
            if c == ch:
                state.progress[i] = ch
        return True, "¡Acierto!"
    else:
        state.attempts -= 1
        return True, "Fallaste."
