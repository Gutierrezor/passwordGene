"""Generador de contraseñas seguras (CLI).

Uso:
    python -m src.password_generator

Funciona con Python 3.8+ y usa el módulo `secrets` para generación segura.
"""
import secrets
import string
import random
import argparse
from typing import List


def generate_password(
    length: int,
    use_uppercase: bool = True,
    use_digits: bool = True,
    use_special_chars: bool = True,
) -> str:
    """Genera una contraseña segura y garantiza la inclusión de los tipos seleccionados.

    Lanza `ValueError` si `length` es menor que el número de grupos requeridos.
    """
    if length <= 0:
        raise ValueError("La longitud debe ser un entero positivo mayor que 0")

    lowercase = string.ascii_lowercase
    pools: List[str] = []
    required: List[str] = []

    # Siempre incluimos al menos una minúscula
    pools.append(lowercase)
    required.append(secrets.choice(lowercase))

    if use_uppercase:
        pools.append(string.ascii_uppercase)
        required.append(secrets.choice(string.ascii_uppercase))

    if use_digits:
        pools.append(string.digits)
        required.append(secrets.choice(string.digits))

    if use_special_chars:
        pools.append(string.punctuation)
        required.append(secrets.choice(string.punctuation))

    min_required = len(required)
    if length < min_required:
        raise ValueError(
            f"La longitud es demasiado corta para satisfacer los requisitos: necesita al menos {min_required} caracteres"
        )

    all_chars = "".join(pools)

    # Construir la contraseña asegurando incluir los caracteres requeridos
    password_chars: List[str] = list(required)
    for _ in range(length - len(password_chars)):
        password_chars.append(secrets.choice(all_chars))

    # Mezclamos de forma segura usando SystemRandom
    random.SystemRandom().shuffle(password_chars)

    return "".join(password_chars)


def ask_bool(question: str) -> bool:
    """Pregunta al usuario una respuesta sí/no (acepta 's' o 'n')."""
    while True:
        ans = input(question + " (s/n): ").strip().lower()
        if ans in ("s", "si", "sí"):
            return True
        if ans in ("n", "no"):
            return False
        print("Respuesta no válida. Escribe 's' o 'n'.")


def main() -> None:
    print("=== Generador de Contraseñas Seguras ===")

    try:
        length_raw = input("Introduce la longitud de la contraseña: ").strip()
        length = int(length_raw)
    except ValueError:
        print("Longitud inválida: introduce un número entero.")
        return

    use_uppercase = ask_bool("¿Usar letras mayúsculas?")
    use_digits = ask_bool("¿Usar números?")
    use_special_chars = ask_bool("¿Usar caracteres especiales?")

    try:
        pwd = generate_password(length, use_uppercase, use_digits, use_special_chars)
    except ValueError as exc:
        print(f"Error: {exc}")
        return

    print("\nContraseña generada:", pwd)


def _cli_main() -> None:
    parser = argparse.ArgumentParser(description="Generador de contraseñas seguras")
    parser.add_argument("--length", "-l", type=int, help="Longitud de la contraseña")
    parser.add_argument("--no-uppercase", action="store_true", help="Desactivar mayúsculas")
    parser.add_argument("--no-digits", action="store_true", help="Desactivar dígitos")
    parser.add_argument("--no-special", action="store_true", help="Desactivar caracteres especiales")

    args = parser.parse_args()

    # If any CLI argument provided, operate in non-interactive mode
    if args.length is not None or args.no_uppercase or args.no_digits or args.no_special:
        length = args.length if args.length is not None else 12
        use_uppercase = not args.no_uppercase
        use_digits = not args.no_digits
        use_special_chars = not args.no_special

        try:
            pwd = generate_password(length, use_uppercase, use_digits, use_special_chars)
        except ValueError as exc:
            print(f"Error: {exc}")
            raise SystemExit(2)

        print(pwd)
    else:
        main()


if __name__ == "__main__":
    _cli_main()
