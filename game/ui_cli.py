from .engine import GameState, try_letter

def render(state: GameState) -> None:
    print("\nPalabra: ", " ".join(state.progress))
    print("Intentos:", state.attempts, "| Usadas:", ", ".join(sorted(state.used)) or "-")

def loop(state: GameState) -> None:
    while not state.finished():
        render(state)
        ch = input("Ingresa una letra: ")
        ok, msg = try_letter(state, ch)
        if not ok:
            print(">>", msg)
            continue
        print(">>", msg)
    render(state)
    if state.won():
        print("\n🎉 ¡Ganaste!")
    else:
        print(f"\n💀 Perdiste. La palabra era: {state.secret}")
