import tkinter as tk
from tkinter import ttk, messagebox

# Демо-курсы к рублю (в реальном приложении — загрузка с API ЦБ)
RATES = {
    "RUB": 1.0,
    "USD": 92.5,
    "EUR": 100.3,
    "CNY": 12.8,
    "KZT": 0.20,
}

class CurrencyConverter:
    def __init__(self, root):
        # 1. ГЛАВНОЕ ОКНО
        self.root = root
        self.root.title("Конвертер валют")
        self.root.geometry("540x560")
        self.root.minsize(500, 520)
        self.root.configure(padx=15, pady=15)

        self.history = []  # список кортежей (from, to, amount, result)

        # ---------- 10. КОМПОНОВКА ----------
        self.root.columnconfigure(0, weight=1)

        # 2. ТЕКСТОВЫЕ ЭЛЕМЕНТЫ
        ttk.Label(self.root, text="💱 Конвертер валют",
                  font=("Arial", 18, "bold")).grid(row=0, column=0, sticky="w")
        ttk.Label(self.root, text="Демо-курсы (не для реальных операций)",
                  foreground="#777").grid(row=1, column=0, sticky="w", pady=(0, 12))

        # 3. ПОЛЕ ВВОДА (сумма)
        frame_sum = ttk.LabelFrame(self.root, text="Сумма", padding=10)
        frame_sum.grid(row=2, column=0, sticky="ew", pady=(0, 10))
        frame_sum.columnconfigure(1, weight=1)

        ttk.Label(frame_sum, text="Сумма:").grid(row=0, column=0, padx=(0, 8))
        self.amount_var = tk.StringVar(value="100")
        self.entry_amount = ttk.Entry(frame_sum, textvariable=self.amount_var)
        self.entry_amount.grid(row=0, column=1, sticky="ew")
        # 7. ОТРАБОТКА СОБЫТИЙ: Enter — выполнить конвертацию
        self.entry_amount.bind("<Return>", lambda e: self.convert())
        # Живой пересчёт при вводе (отработка события KeyRelease)
        self.entry_amount.bind("<KeyRelease>", lambda e: self.live_preview())

        # 5. ВЫБОР ПАРАМЕТРОВ (валюты)
        frame_cur = ttk.LabelFrame(self.root, text="Валюты", padding=10)
        frame_cur.grid(row=3, column=0, sticky="ew", pady=(0, 10))
        frame_cur.columnconfigure(1, weight=1)
        frame_cur.columnconfigure(3, weight=1)

        currencies = list(RATES.keys())
        ttk.Label(frame_cur, text="Из:").grid(row=0, column=0, sticky="w")
        self.from_var = tk.StringVar(value="USD")
        self.combo_from = ttk.Combobox(frame_cur, textvariable=self.from_var,
                                       values=currencies, state="readonly", width=8)
        self.combo_from.grid(row=0, column=1, sticky="w")

        ttk.Label(frame_cur, text="→").grid(row=0, column=2, padx=6)
        ttk.Label(frame_cur, text="В:").grid(row=0, column=3, sticky="w")
        self.to_var = tk.StringVar(value="RUB")
        self.combo_to = ttk.Combobox(frame_cur, textvariable=self.to_var,
                                     values=currencies, state="readonly", width=8)
        self.combo_to.grid(row=0, column=4, sticky="w")

        # Чекбокс — округлять результат
        self.round_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(frame_cur, text="Округлять до 2 знаков",
                        variable=self.round_var,
                        command=self.live_preview
                        ).grid(row=1, column=0, columnspan=5, sticky="w", pady=(8, 0))

        # 4. КНОПКИ ОТПРАВКИ ДАННЫХ
        frame_btn = ttk.Frame(self.root)
        frame_btn.grid(row=4, column=0, sticky="ew", pady=(0, 10))
        frame_btn.columnconfigure(0, weight=1)
        frame_btn.columnconfigure(1, weight=1)

        ttk.Button(frame_btn, text="Конвертировать",
                   command=self.convert).grid(row=0, column=0, sticky="ew", padx=(0, 5))
        ttk.Button(frame_btn, text="История",
                   command=self.show_history).grid(row=0, column=1, sticky="ew", padx=(5, 0))

        # 6. ВЫВОД РЕЗУЛЬТАТОВ
        frame_res = ttk.LabelFrame(self.root, text="Результат", padding=10)
        frame_res.grid(row=5, column=0, sticky="nsew", pady=(0, 10))
        frame_res.columnconfigure(0, weight=1)
        self.root.rowconfigure(5, weight=1)

        self.result_var = tk.StringVar(value="—")
        ttk.Label(frame_res, textvariable=self.result_var,
                  font=("Arial", 20, "bold"), foreground="#1565c0"
                  ).grid(row=0, column=0, sticky="w")

        self.detail_var = tk.StringVar(value="Введите сумму и нажмите «Конвертировать»")
        ttk.Label(frame_res, textvariable=self.detail_var,
                  foreground="#666", wraplength=460, justify="left"
                  ).grid(row=1, column=0, sticky="w", pady=(6, 0))

        # Статус-бар
        self.status_var = tk.StringVar(value="Готово")
        ttk.Label(self.root, textvariable=self.status_var, relief="sunken",
                  anchor="w", padding=4).grid(row=6, column=0, sticky="ew")

    # ---------- 8. ПРОВЕРКА ДАННЫХ ----------
    def _validate(self):
        raw = self.amount_var.get().strip().replace(",", ".")
        if not raw:
            return None, "Поле суммы пустое"
        try:
            value = float(raw)
        except ValueError:
            return None, f"«{raw}» — не число"
        if value <= 0:
            return None, "Сумма должна быть больше нуля"
        if value > 1_000_000_000:
            return None, "Слишком большая сумма (макс. 1 млрд)"
        if self.from_var.get() == self.to_var.get():
            return None, "Валюты «из» и «в» совпадают"
        return value, None

    def _compute(self, amount):
        rate_from = RATES[self.from_var.get()]
        rate_to = RATES[self.to_var.get()]
        result = amount * rate_from / rate_to
        if self.round_var.get():
            result = round(result, 2)
        return result

    # ---------- 7. ОТРАБОТКА СОБЫТИЙ (живой пересчёт) ----------
    def live_preview(self):
        value, err = self._validate()
        if err:
            self.result_var.set("—")
            self.detail_var.set(err)
            return
        result = self._compute(value)
        self.result_var.set(f"{result:,.2f} {self.to_var.get()}")
        self.detail_var.set(f"{value:,.2f} {self.from_var.get()} по курсу "
                            f"1 {self.from_var.get()} = "
                            f"{RATES[self.from_var.get()]/RATES[self.to_var.get()]:.4f} "
                            f"{self.to_var.get()}")

    # ---------- 4. КНОПКА «КОНВЕРТИРОВАТЬ» ----------
    def convert(self):
        value, err = self._validate()
        if err:
            self.status_var.set(f"Ошибка: {err}")
            # 9. ДИАЛОГОВОЕ ОКНО
            messagebox.showwarning("Проверьте ввод", err)
            self.entry_amount.focus_set()
            return

        result = self._compute(value)
        self.result_var.set(f"{result:,.2f} {self.to_var.get()}")
        self.detail_var.set(f"{value:,.2f} {self.from_var.get()} → "
                            f"{result:,.2f} {self.to_var.get()}")
        self.status_var.set("Конвертация выполнена")

        # Сохраняем в историю
        self.history.append((self.from_var.get(), self.to_var.get(),
                             value, result))

    # ---------- 9. ДИАЛОГОВОЕ ОКНО (история) ----------
    def show_history(self):
        win = tk.Toplevel(self.root)
        win.title("История операций")
        win.geometry("420x320")
        win.transient(self.root)
        win.grab_set()  # модальное окно

        ttk.Label(win, text="Последние конвертации",
                  font=("Arial", 13, "bold")).pack(anchor="w", padx=10, pady=8)

        text = tk.Text(win, wrap="word", font=("Consolas", 10))
        text.pack(fill="both", expand=True, padx=10, pady=(0, 8))
        text.configure(state="normal")
        if not self.history:
            text.insert("1.0", "История пуста.\nВыполните хотя бы одну конвертацию.")
        else:
            for i, (f, t, a, r) in enumerate(self.history, 1):
                text.insert("end", f"{i:>2}. {a:,.2f} {f} → {r:,.2f} {t}\n")
        text.configure(state="disabled")

        def clear_history():
            if messagebox.askyesno("Очистка", "Удалить всю историю?",
                                   parent=win):
                self.history.clear()
                text.configure(state="normal")
                text.delete("1.0", "end")
                text.insert("1.0", "История очищена.")
                text.configure(state="disabled")

        btn_frame = ttk.Frame(win)
        btn_frame.pack(fill="x", padx=10, pady=(0, 10))
        ttk.Button(btn_frame, text="Очистить", command=clear_history).pack(side="left")
        ttk.Button(btn_frame, text="Закрыть", command=win.destroy).pack(side="right")


if __name__ == "__main__":
    root = tk.Tk()
    try:
        ttk.Style().theme_use("clam")
    except tk.TclError:
        pass
    app = CurrencyConverter(root)
    root.mainloop()