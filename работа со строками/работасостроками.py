
import re

def info():
    print("=" * 60)
    print("ПРОГРАММА ДЛЯ РАБОТЫ СО СТРОКАМИ")
    print("=" * 60)
    print("""
УРОВЕНЬ 1: upper(), lower(), capitalize()
  'Hello_World'.upper()      -> 'HELLO_WORLD'
  'Hello_World'.lower()      -> 'hello_world'
  'hello world'.capitalize() -> 'Hello world'

УРОВЕНЬ 2: find(), replace(), count()
  'Hello_World'.find('World')        -> 6
  'Hello_World'.replace('_', ' ')    -> 'Hello World'
  'Hello_World'.count('l')           -> 3

УРОВЕНЬ 3: split(), join()
  'Hello_World'.split('_')           -> ['Hello', 'World']
  '_'.join(['Hello', 'World'])       -> 'Hello_World'

УРОВЕНЬ 4: isdigit(), split(), isalpha()
  '12345'.isdigit()                  -> True
  'HelloWorld'.isalpha()             -> True
  'Hello_World'.split('_')           -> ['Hello', 'World']

УРОВЕНЬ 5: Нормализация строки
  '  HELLO___world!!!  '             -> 'Hello world'
""")


def level_1():
    print("1.upper 2.lower 3.capitalize")
    c = input("Функция: ").strip()
    s = input("Строка: ")
    if c == "1": print(s.upper())
    elif c == "2": print(s.lower())
    elif c == "3": print(s.capitalize())
    else: print("Неверно")


def level_2():
    print("1.find 2.replace 3.count")
    c = input("Функция: ").strip()
    s = input("Строка: ")
    if c == "1": print(s.find(input("Подстрока: ")))
    elif c == "2": print(s.replace(input("Что: "), input("На что: ")))
    elif c == "3": print(s.count(input("Подстрока: ")))
    else: print("Неверно")


def level_3():
    print("1.split 2.join")
    c = input("Функция: ").strip()
    if c == "1":
        s = input("Строка: ")
        sep = input("Разделитель: ")
        print(s.split() if sep == "" else s.split(sep))
    elif c == "2":
        items = [x.strip() for x in input("Элементы через запятую: ").split(",")]
        print(input("Разделитель: ").join(items))
    else: print("Неверно")


def level_4():
    print("1.isdigit 2.split 3.isalpha")
    c = input("Функция: ").strip()
    s = input("Строка: ")
    if c == "1": print(s.isdigit())
    elif c == "2":
        sep = input("Разделитель: ")
        print(s.split() if sep == "" else s.split(sep))
    elif c == "3": print(s.isalpha())
    else: print("Неверно")


def level_5():
    s = input("Строка: ")
    s = re.sub(r'[\s_\-]+', ' ', s.strip())
    s = re.sub(r'[^\w\s]', '', s, flags=re.UNICODE)
    print(s.lower().capitalize())


def tests():
    t = "Hello_World"
    checks = [
        (t.upper(), "HELLO_WORLD"),
        (t.lower(), "hello_world"),
        ("hello world".capitalize(), "Hello world"),
        (t.find("World"), 6),
        (t.replace("_", " "), "Hello World"),
        (t.count("l"), 3),
        (t.split("_"), ["Hello", "World"]),
        ("_".join(["Hello", "World"]), "Hello_World"),
        ("12345".isdigit(), True),
        ("HelloWorld".isalpha(), True),
    ]
    ok = sum(a == b for a, b in checks)
    for a, b in checks:
        print(("correct" if a == b else "uncorrect"), f"{a!r} vs {b!r}")
    print(f"Пройдено: {ok}/{len(checks)}")


def main():
    info()
    levels = {"1": level_1, "2": level_2, "3": level_3, "4": level_4, "5": level_5, "t": tests}
    while True:
        c = input("\nУровень (1-5), t - тесты, q - выход: ").strip().lower()
        if c == "q":
            break
        levels.get(c, lambda: print("Неверно"))()


if __name__ == "__main__":
    main()
