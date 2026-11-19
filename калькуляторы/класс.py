class Calculator:
    def __init__(self):
        self.history = []

    def add(self, a, b):
        return a + b

    def sub(self, a, b):
        return a - b

    def mul(self, a, b):
        return a * b

    def div(self, a, b):
        if b == 0:
            raise ZeroDivisionError("Деление на ноль")
        return a / b

    def calculate(self, a, op, b):
        operations = {
            "+": self.add,
            "-": self.sub,
            "*": self.mul,
            "/": self.div,
        }
        if op not in operations:
            raise ValueError("Неизвестная операция")
        result = operations[op](a, b)
        self.history.append(f"{a} {op} {b} = {result}")
        return result

    def show_history(self):
        if not self.history:
            print("История пуста")
        else:
            print("=== История ===")
            for record in self.history:
                print(record)


def main():
    calc = Calculator()
    print("=== Калькулятор (введите 'h' — история, 'q' — выход) ===")
    while True:
        first = input("Введите первое число (или 'h'/'q'): ")
        if first.lower() == "q":
            print("Выход...")
            break
        if first.lower() == "h":
            calc.show_history()
            continue

        op = input("Введите операцию (+, -, *, /): ")
        second = input("Введите второе число: ")

        try:
            a, b = float(first), float(second)
            result = calc.calculate(a, op, b)
            print(f"Результат: {result}")
        except ValueError as e:
            print(f"Ошибка: {e}")
        except ZeroDivisionError as e:
            print(f"Ошибка: {e}")


if __name__ == "__main__":
    main()