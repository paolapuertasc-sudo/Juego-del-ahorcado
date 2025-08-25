import random

EASY = ["sol", "casa", "uva", "luz", "mar", "perro", "gato"]
MEDIUM = ["python", "bucle", "lista", "modulo", "paquete", "variable"]
HARD = ["condicional", "arquitectura", "persistencia", "abstraccion", "polimorfismo"]

def random_word(difficulty: str) -> str:
    """Devuelve una palabra aleatoria según la dificultad."""
    if difficulty == "facil":
        return random.choice(EASY)
    elif difficulty == "medio":
        return random.choice(MEDIUM)
    else:
        return random.choice(HARD)
