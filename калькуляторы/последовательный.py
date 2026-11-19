print("=== Калькулятор ===")
a = float(input("Введите первое число: "))
op = input("Введите операцию (+, -, *, /): ")
b = float(input("Введите второе число: "))

if op == "+":
    result = a + b
elif op == "-":
    result = a - b
elif op == "*":
    result = a * b
elif op == "/":
    if b != 0:
        result = a / b
    else:
        result = "Ошибка: деление на ноль"
else:
    result = "Ошибка: неизвестная операция"

print(f"Результат: {result}")