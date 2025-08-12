from game.words import random_word
from game.engine import GameState
from game.ui_cli import loop

def select_difficulty() -> tuple[str, int]:
    """
    Permite seleccionar la dificultad antes de iniciar el juego.
    Devuelve la dificultad y la cantidad de intentos.
    """
    while True:
        print("\nSelecciona dificultad:")
        print("1 - Fácil   (8 intentos)")
        print("2 - Medio   (6 intentos)")
        print("3 - Difícil (5 intentos)")
        choice = input("Opción: ").strip()

        if choice == "1":
            return "facil", 8
        elif choice == "2":
            return "medio", 6
        elif choice == "3":
            return "dificil", 5
        else:
            print("Opción inválida. Intenta nuevamente.")

def main():
    print("=== Juego del Ahorcado ===")

    while True:
        difficulty, attempts = select_difficulty()
        secret = random_word(difficulty)
        state = GameState(secret=secret, attempts=attempts)

        loop(state)  # Ejecuta la partida

        again = input("\n¿Quieres jugar otra vez? (s/n): ").strip().lower()
        if again != "s":
            print("Gracias por jugar. ¡Hasta la próxima!")
            break

if __name__ == "__main__":
    main()
