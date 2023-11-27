import random
import string
import qrcode
import time
import hashlib
import getpass
import os


class ConsoleColors:
    HEADER = '\033[38;2;152;176;236m'
    OKBLUE = '\033[38;2;114;171;224m'
    OKGREEN = '\033[38;2;109;194;56m'
    WARNING = '\033[93m'
    FAIL = '\033[38;2;209;53;37m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def generate_password(length, use_letters=True, use_digits=True, use_symbols=True):
    characters = ""
    if use_letters:
        characters += string.ascii_letters
    if use_digits:
        characters += string.digits
    if use_symbols:
        characters += string.punctuation

    if not characters:
        raise ValueError(ConsoleColors.FAIL + "Ошибка: выберите хотя бы один тип символов." + ConsoleColors.ENDC)

    password = ''.join(random.choice(characters) for _ in range(length))
    return password


def save_password(password, filename="passwords.txt"):
    hashed_password = hash_password(password)
    with open(filename, "a") as file:
        file.write(f"Хеш пароля: {hashed_password}\n")
    print(ConsoleColors.OKGREEN + f"Пароль сохранен в файл {filename} в хэшированном виде." + ConsoleColors.ENDC)


def generate_multiple_passwords(count, length, use_letters=True, use_digits=True, use_symbols=True):
    if count < 1:
        raise ValueError(
            ConsoleColors.FAIL + "Ошибка: количество паролей должно быть положительным числом." + ConsoleColors.ENDC)

    if count > 10:
        raise ValueError(ConsoleColors.FAIL + "Ошибка: количество паролей не может превышать 10." + ConsoleColors.ENDC)

    passwords = [generate_password(length, use_letters, use_digits, use_symbols) for _ in range(count)]
    return passwords


def generate_qrcode(data, filename="qrcode.png", directory="qrcodes"):
    timestamp = int(time.time())
    filename = f"{directory}/{filename.split('.')[0]}_{timestamp}.png"

    # Проверка наличия папки qrcodes и её создание при необходимости
    if not os.path.exists(directory):
        os.makedirs(directory)

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(filename)
    print(ConsoleColors.OKBLUE + f"QR-код сохранен в файл {filename}." + ConsoleColors.ENDC)


def is_weak_password(password):
    return len(password) < 6


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


if __name__ == "__main__":
    print(ConsoleColors.HEADER + "Добро пожаловать в генератор паролей!" + ConsoleColors.ENDC)

    while True:
        try:
            length = input(ConsoleColors.BOLD + "Введите длину пароля: " + ConsoleColors.ENDC)
            if not length.isdigit() or int(length) < 6:
                raise ValueError("Длина пароля должна быть числом и не менее 6 символов.")
            length = int(length)

            while True:
                use_letters = input(ConsoleColors.BOLD + "Включить буквы? (да/нет): " + ConsoleColors.ENDC).lower()
                if use_letters in ['да', 'нет']:
                    break
                else:
                    print(ConsoleColors.WARNING + "Введите 'да' или 'нет'." + ConsoleColors.ENDC)

            while True:
                use_digits = input(ConsoleColors.BOLD + "Включить цифры? (да/нет): " + ConsoleColors.ENDC).lower()
                if use_digits in ['да', 'нет']:
                    break
                else:
                    print(ConsoleColors.WARNING + "Введите 'да' или 'нет'." + ConsoleColors.ENDC)

            while True:
                use_symbols = input(ConsoleColors.BOLD + "Включить символы? (да/нет): " + ConsoleColors.ENDC).lower()
                if use_symbols in ['да', 'нет']:
                    break
                else:
                    print(ConsoleColors.WARNING + "Введите 'да' или 'нет'." + ConsoleColors.ENDC)

            count = input(ConsoleColors.BOLD + "Введите количество паролей для генерации: " + ConsoleColors.ENDC)
            if not count.isdigit() or int(count) < 1 or int(count) > 10:
                raise ValueError("Количество паролей должно быть числом от 1 до 10.")
            count = int(count)

            use_letters = use_letters == 'да'
            use_digits = use_digits == 'да'
            use_symbols = use_symbols == 'да'

            if count == 1:
                password = generate_password(length, use_letters, use_digits, use_symbols)

                if password:
                    print(ConsoleColors.OKGREEN + f"Сгенерированный пароль: {password}" + ConsoleColors.ENDC)

                    if is_weak_password(password):
                        print(
                            ConsoleColors.WARNING + "Предупреждение: Этот пароль может считаться слабым." + ConsoleColors.ENDC)

                    save_option = input(
                        ConsoleColors.BOLD + "Хотите сохранить пароль? (да/нет): " + ConsoleColors.ENDC).lower()
                    while save_option not in ['да', 'нет']:
                        print(ConsoleColors.WARNING + "Введите 'да' или 'нет'." + ConsoleColors.ENDC)
                        save_option = input(
                            ConsoleColors.BOLD + "Хотите сохранить пароль? (да/нет): " + ConsoleColors.ENDC).lower()

                    if save_option == 'да':
                        save_password(hash_password(password))

                    generate_qrcode_option = input(
                        ConsoleColors.BOLD + "Хотите сгенерировать QR-код для пароля? (да/нет): " + ConsoleColors.ENDC).lower()
                    while generate_qrcode_option not in ['да', 'нет']:
                        print(ConsoleColors.WARNING + "Введите 'да' или 'нет'." + ConsoleColors.ENDC)
                        generate_qrcode_option = input(
                            ConsoleColors.BOLD + "Хотите сгенерировать QR-код для пароля? (да/нет): " + ConsoleColors.ENDC).lower()

                    if generate_qrcode_option == 'да':
                        generate_qrcode(password)
            elif count > 1:
                passwords = generate_multiple_passwords(count, length, use_letters, use_digits, use_symbols)

                for i, password in enumerate(passwords, 1):
                    print(ConsoleColors.OKGREEN + f"Пароль {i}: {password}" + ConsoleColors.ENDC)

                    if is_weak_password(password):
                        print(
                            ConsoleColors.WARNING + "Предупреждение: Этот пароль может считаться слабым." + ConsoleColors.ENDC)

                    save_option = input(
                        ConsoleColors.BOLD + "Хотите сохранить пароль? (да/нет): " + ConsoleColors.ENDC).lower()
                    while save_option not in ['да', 'нет']:
                        print(ConsoleColors.FAIL + "Введите 'да' или 'нет'." + ConsoleColors.ENDC)
                        save_option = input(
                            ConsoleColors.BOLD + "Хотите сохранить пароль? (да/нет): " + ConsoleColors.ENDC).lower()

                    if save_option == 'да':
                        save_password(hash_password(password))

                    generate_qrcode_option = input(
                        ConsoleColors.BOLD + "Хотите сгенерировать QR-код для пароля? (да/нет): " + ConsoleColors.ENDC).lower()
                    while generate_qrcode_option not in ['да', 'нет']:
                        print(ConsoleColors.FAIL + "Введите 'да' или 'нет'." + ConsoleColors.ENDC)
                        generate_qrcode_option = input(
                            ConsoleColors.BOLD + "Хотите сгенерировать QR-код для пароля? (да/нет): " + ConsoleColors.ENDC).lower()

                    if generate_qrcode_option == 'да':
                        generate_qrcode(password)
            else:
                raise ValueError(
                    ConsoleColors.FAIL + "Количество паролей должно быть положительным числом." + ConsoleColors.ENDC)
        except ValueError as e:
            print(ConsoleColors.FAIL + f"Ошибка: {e}" + ConsoleColors.ENDC)

        try_again = input(
            ConsoleColors.BOLD + "Хотите сгенерировать еще пароли? (да/нет): " + ConsoleColors.ENDC).lower()
        if try_again != 'да':
            break
