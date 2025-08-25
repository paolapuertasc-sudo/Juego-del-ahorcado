
from dataclasses import dataclass, field
import unicodedata
from .words import random_word

ALPHABET = [*'abcdefghijklmnopqrstuvwxyz', 'ñ']  # soporte básico español

def strip_accents(s: str) -> str:
    # Mantener ñ, quitar tildes de áéíóúü
    s = s.replace("Ñ", "ñ").replace("Ü", "ü")
    nfkd = unicodedata.normalize("NFKD", s)
    return "".join(c for c in nfkd if not unicodedata.combining(c))

def normalize_text(s: str) -> str:
    return strip_accents(s).lower()

def normalize_letter(ch: str) -> str:
    ch = normalize_text(ch.strip())
    return ch[:1]  # solo primer carácter

@dataclass
class GameState:
    secret: str
    attempts: int
    used: set = field(default_factory=set)
    progress: list = field(default_factory=list)

    def __post_init__(self):
        self.secret = normalize_text(self.secret)
        if not self.progress:
            self.progress = ["_" for _ in self.secret]
        # Revelar guiones y espacios automáticamente si existieran
        for i, c in enumerate(self.secret):
            if not c.isalpha():
                self.progress[i] = c

    @property
    def max_attempts(self) -> int:
        return getattr(self, "_max_attempts", self.attempts)

    def set_max_attempts(self, n: int) -> None:
        self._max_attempts = n

    def finished(self) -> bool:
        return self.attempts <= 0 or "_" not in self.progress

    def won(self) -> bool:
        return "_" not in self.progress

def try_letter(state: GameState, ch: str) -> tuple[bool, str]:
    ch = normalize_letter(ch)
    if len(ch) != 1 or not ch.isalpha():
        return False, "Ingresa solo una letra (a-z, ñ)."
    if ch not in ALPHABET:
        return False, "Letra no válida."
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

def start_new_game(difficulty: str) -> GameState:
    difficulty = (difficulty or "medio").strip().lower()
    if difficulty in ("facil", "fácil", "1"):
        attempts = 8
    elif difficulty in ("medio", "2"):
        attempts = 6
    else:
        attempts = 5
    secret = random_word("facil" if attempts==8 else "medio" if attempts==6 else "dificil" if "dificil" in difficulty or "3" in difficulty else "medio")
    state = GameState(secret=secret, attempts=attempts)
    state.set_max_attempts(attempts)
    return state
