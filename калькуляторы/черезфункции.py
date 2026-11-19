def add(a, b):
    return a + b

def sub(a, b):
    return a - b

def mul(a, b):
    return a * b

def div(a, b):
    if b == 0:
        return "Ошибка: деление на ноль"
    return a / b

def calculator():
    print("=== Калькулятор ===")
    a = float(input("Введите первое число: "))
    op = input("Введите операцию (+, -, *, /): ")
    b = float(input("Введите второе число: "))

    operations = {
        "+": add,
        "-": sub,
        "*": mul,
        "/": div,
    }

    if op in operations:
        result = operations[op](a, b)
    else:
        result = "Ошибка: неизвестная операция"

    print(f"Результат: {result}")

calculator()