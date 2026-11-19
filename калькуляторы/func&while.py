def calculator():
    print("=== Калькулятор (введите 'q' для выхода) ===")
    while True:
        a = input("Введите первое число (или 'q'): ")
        if a.lower() == "q":
            print("Выход...")
            break

        op = input("Введите операцию (+, -, *, /): ")
        b = input("Введите второе число: ")

        try:
            a, b = float(a), float(b)
        except ValueError:
            print("Ошибка: введите числа!")
            continue

        if op == "+":
            print(f"Результат: {a + b}")
        elif op == "-":
            print(f"Результат: {a - b}")
        elif op == "*":
            print(f"Результат: {a * b}")
        elif op == "/":
            if b != 0:
                print(f"Результат: {a / b}")
            else:
                print("Ошибка: деление на ноль")
        else:
            print("Ошибка: неизвестная операция")

calculator()