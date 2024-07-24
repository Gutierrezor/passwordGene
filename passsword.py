import random
import string

def generate_password(length, use_uppercase=True, use_digits=True, use_special_chars=True):
    lower = string.ascii_lowercase
    upper = string.ascii_uppercase if use_uppercase else ''
    digits = string.digits if use_digits else ''
    special = string.punctuation if use_special_chars else ''
    
    all_chars = lower + upper + digits + special
    
    password = [
        random.choice(lower),
        random.choice(upper) if use_uppercase else '',
        random.choice(digits) if use_digits else '',
        random.choice(special) if use_special_chars else ''
    ]
    
    password += random.choices(all_chars, k=length - len(password))
    
    random.shuffle(password)
    
    return ''.join(password)

def main():
    print("Generador de Contraseñas")
    length = int(input("Introduce la longitud de la contraseña: "))
    use_uppercase = input("¿Usar letras mayúsculas? (s/n): ").lower() == 's'
    use_digits = input("¿Usar números? (s/n): ").lower() == 's'
    use_special_chars = input("¿caracteres especiales? (s/n): ").lower() == 's'
    
    password = generate_password(length, use_uppercase, use_digits, use_special_chars)
    print(f"Contraseña generada: {password}")

if __name__ == "__main__":
    main()
