import tkinter as tk
from tkinter import ttk, messagebox


class CoffeeShopApp:
    def __init__(self, root):
        self.root = root
        self.root.title("MyКофейня — Учёт заказов")
        self.root.geometry("940x620")
        self.root.minsize(850, 550)

        self.colors = {
            "bg": "#FAF6F0",
            "card": "#FFFFFF",
            "header": "#3E2723",
            "header_text": "#FFF8E7",
            "accent": "#6D4C41",
            "accent_hover": "#5D4037",
            "success": "#2E7D32",
            "success_hover": "#1B5E20",
            "danger": "#C62828",
            "danger_hover": "#B71C1C",
            "border": "#D7CCC8",
            "text": "#2C1E1A",
            "muted": "#795548",
            "row_prep": "#FFF8E1",
            "row_done": "#E8F5E9",
        }

        self.root.configure(bg=self.colors["bg"])

        self.menu_prices = {
            "Эспрессо": 150,
            "Американо": 180,
            "Капучино": 220,
            "Латте": 240,
            "Раф": 270,
            "Матча Латте": 260,
            "Какао": 200
        }

        self.orders = []
        self.next_id = 1

        self.setup_styles()
        self.setup_ui()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")

        font_main = ("Segoe UI", 10)
        font_bold = ("Segoe UI", 10, "bold")
        font_title = ("Segoe UI", 14, "bold")

        style.configure("App.TFrame", background=self.colors["bg"])
        style.configure("Card.TFrame", background=self.colors["card"])

        style.configure(
            "Card.TLabelframe",
            background=self.colors["card"],
            bordercolor=self.colors["border"],
            relief="solid",
            borderwidth=1
        )
        style.configure(
            "Card.TLabelframe.Label",
            background=self.colors["card"],
            foreground=self.colors["header"],
            font=font_bold
        )

        style.configure(
            "Card.TLabel",
            background=self.colors["card"],
            foreground=self.colors["text"],
            font=font_main
        )
        style.configure(
            "Hint.TLabel",
            background=self.colors["card"],
            foreground=self.colors["muted"],
            font=("Segoe UI", 9)
        )

        style.configure("TEntry", fieldbackground="#FFFFFF", foreground=self.colors["text"], padding=4)
        style.configure("TCombobox", fieldbackground="#FFFFFF", foreground=self.colors["text"], padding=4)

        style.configure(
            "TButton",
            font=font_main,
            padding=(10, 6),
            background="#EFE6DD",
            foreground=self.colors["text"],
            borderwidth=0
        )
        style.map("TButton", background=[("active", "#E0D3C5")])

        style.configure(
            "Primary.TButton",
            font=font_bold,
            padding=(12, 6),
            background=self.colors["accent"],
            foreground="#FFFFFF",
            borderwidth=0
        )
        style.map("Primary.TButton", background=[("active", self.colors["accent_hover"])])

        style.configure(
            "Success.TButton",
            font=font_bold,
            padding=(12, 6),
            background=self.colors["success"],
            foreground="#FFFFFF",
            borderwidth=0
        )
        style.map("Success.TButton", background=[("active", self.colors["success_hover"])])

        style.configure(
            "Danger.TButton",
            font=font_main,
            padding=(10, 6),
            background=self.colors["danger"],
            foreground="#FFFFFF",
            borderwidth=0
        )
        style.map("Danger.TButton", background=[("active", self.colors["danger_hover"])])

        style.configure(
            "Treeview",
            background="#FFFFFF",
            foreground=self.colors["text"],
            rowheight=28,
            fieldbackground="#FFFFFF",
            font=font_main,
            borderwidth=0
        )
        style.configure(
            "Treeview.Heading",
            background="#EFE6DD",
            foreground=self.colors["header"],
            font=font_bold,
            padding=(6, 6),
            relief="flat"
        )
        style.map(
            "Treeview",
            background=[("selected", self.colors["accent"])],
            foreground=[("selected", "#FFFFFF")]
        )

        self.font_title = font_title

    def setup_ui(self):
        header_bar = tk.Frame(self.root, bg=self.colors["header"], height=56)
        header_bar.pack(fill="x")
        header_bar.pack_propagate(False)

        tk.Label(
            header_bar,
            text="☕  MyКофейня — Рабочее место бариста",
            bg=self.colors["header"],
            fg=self.colors["header_text"],
            font=self.font_title
        ).pack(side="left", padx=18)

        self.stats_var = tk.StringVar(value="Заказов: 0  |  Готовится: 0  |  Выручка: 0 ₽")
        tk.Label(
            header_bar,
            textvariable=self.stats_var,
            bg=self.colors["header"],
            fg="#D7CCC8",
            font=("Segoe UI", 10)
        ).pack(side="right", padx=18)

        main_container = ttk.Frame(self.root, style="App.TFrame", padding=12)
        main_container.pack(fill="both", expand=True)

        form_frame = ttk.LabelFrame(main_container, text=" Оформление и редактирование заказа ", style="Card.TLabelframe", padding=12)
        form_frame.pack(fill="x", pady=(0, 10))

        ttk.Label(form_frame, text="Номер заказа:", style="Card.TLabel").grid(row=0, column=0, sticky="w", padx=6, pady=6)
        self.id_var = tk.StringVar(value="Авто")
        self.id_entry = ttk.Entry(form_frame, textvariable=self.id_var, state="readonly", width=10)
        self.id_entry.grid(row=0, column=1, sticky="w", padx=6, pady=6)

        ttk.Label(form_frame, text="Напиток:", style="Card.TLabel").grid(row=0, column=2, sticky="w", padx=6, pady=6)
        self.drink_var = tk.StringVar(value="Капучино")
        self.drink_combo = ttk.Combobox(
            form_frame, textvariable=self.drink_var, values=list(self.menu_prices.keys()), state="readonly", width=18
        )
        self.drink_combo.grid(row=0, column=3, sticky="w", padx=6, pady=6)
        self.drink_combo.bind("<<ComboboxSelected>>", self.calculate_total)

        ttk.Label(form_frame, text="Количество:", style="Card.TLabel").grid(row=0, column=4, sticky="w", padx=6, pady=6)
        self.qty_var = tk.StringVar(value="1")
        self.qty_entry = ttk.Entry(form_frame, textvariable=self.qty_var, width=8)
        self.qty_entry.grid(row=0, column=5, sticky="w", padx=6, pady=6)
        self.qty_entry.bind("<KeyRelease>", self.calculate_total)

        ttk.Label(form_frame, text="Итого (₽):", style="Card.TLabel").grid(row=1, column=0, sticky="w", padx=6, pady=6)
        self.total_var = tk.StringVar(value="220")
        self.total_entry = ttk.Entry(form_frame, textvariable=self.total_var, state="readonly", width=10)
        self.total_entry.grid(row=1, column=1, sticky="w", padx=6, pady=6)

        ttk.Label(form_frame, text="Комментарий / добавки:", style="Card.TLabel").grid(row=1, column=2, sticky="w", padx=6, pady=6)
        self.comment_var = tk.StringVar()
        self.comment_entry = ttk.Entry(form_frame, textvariable=self.comment_var, width=28)
        self.comment_entry.grid(row=1, column=3, sticky="w", padx=6, pady=6)

        ttk.Label(form_frame, text="Статус:", style="Card.TLabel").grid(row=1, column=4, sticky="w", padx=6, pady=6)
        self.status_var = tk.StringVar(value="Готовится")
        self.status_combo = ttk.Combobox(
            form_frame, textvariable=self.status_var, values=["Готовится", "Выдан"], state="readonly", width=12
        )
        self.status_combo.grid(row=1, column=5, sticky="w", padx=6, pady=6)

        prices_text = "Меню: " + "  •  ".join(f"{k} — {v} ₽" for k, v in self.menu_prices.items())
        ttk.Label(form_frame, text=prices_text, style="Hint.TLabel").grid(
            row=2, column=0, columnspan=6, sticky="w", padx=6, pady=(4, 2)
        )

        btn_frame = ttk.Frame(form_frame, style="Card.TFrame")
        btn_frame.grid(row=3, column=0, columnspan=6, pady=(8, 2), sticky="we")

        ttk.Button(btn_frame, text="Создать заказ", style="Primary.TButton", command=self.add_order).pack(side="left", padx=(4, 6))
        ttk.Button(btn_frame, text="Сохранить изменения", command=self.update_order).pack(side="left", padx=6)
        ttk.Button(btn_frame, text="Отметить «Выдан»", style="Success.TButton", command=self.mark_issued).pack(side="left", padx=6)
        ttk.Button(btn_frame, text="Очистить форму", command=self.clear_form).pack(side="left", padx=6)
        ttk.Button(btn_frame, text="Удалить заказ", style="Danger.TButton", command=self.delete_order).pack(side="right", padx=4)

        filter_frame = ttk.LabelFrame(main_container, text=" Поиск и фильтрация очереди ", style="Card.TLabelframe", padding=10)
        filter_frame.pack(fill="x", pady=(0, 10))

        ttk.Label(filter_frame, text="Поиск по номеру:", style="Card.TLabel").pack(side="left", padx=6)
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(filter_frame, textvariable=self.search_var, width=14)
        search_entry.pack(side="left", padx=6)
        search_entry.bind("<Return>", lambda e: self.refresh_table())

        ttk.Button(filter_frame, text="Найти", command=self.refresh_table).pack(side="left", padx=4)

        ttk.Label(filter_frame, text="Фильтр по статусу:", style="Card.TLabel").pack(side="left", padx=(18, 6))
        self.filter_status_var = tk.StringVar(value="Все")
        filter_combo = ttk.Combobox(
            filter_frame, textvariable=self.filter_status_var, values=["Все", "Готовится", "Выдан"], state="readonly", width=14
        )
        filter_combo.pack(side="left", padx=6)
        filter_combo.bind("<<ComboboxSelected>>", lambda e: self.refresh_table())

        ttk.Button(filter_frame, text="Сбросить фильтры", command=self.reset_filters).pack(side="left", padx=10)

        table_card = ttk.LabelFrame(main_container, text=" Список заказов текущей смены ", style="Card.TLabelframe", padding=8)
        table_card.pack(fill="both", expand=True)

        columns = ("id", "drink", "qty", "total", "comment", "status")
        self.tree = ttk.Treeview(table_card, columns=columns, show="headings")
        self.tree.heading("id", text="№")
        self.tree.heading("drink", text="Напиток")
        self.tree.heading("qty", text="Кол-во")
        self.tree.heading("total", text="Сумма (₽)")
        self.tree.heading("comment", text="Состав / Комментарий")
        self.tree.heading("status", text="Статус")

        self.tree.column("id", width=55, anchor="center")
        self.tree.column("drink", width=150)
        self.tree.column("qty", width=75, anchor="center")
        self.tree.column("total", width=100, anchor="center")
        self.tree.column("comment", width=310)
        self.tree.column("status", width=120, anchor="center")

        self.tree.tag_configure("prep", background=self.colors["row_prep"])
        self.tree.tag_configure("done", background=self.colors["row_done"])

        scrollbar = ttk.Scrollbar(table_card, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.tree.bind("<<TreeviewSelect>>", self.on_select_order)

    def calculate_total(self, event=None):
        drink = self.drink_var.get()
        price = self.menu_prices.get(drink, 0)
        try:
            qty = int(self.qty_var.get())
            if qty < 1:
                raise ValueError
            self.total_var.set(str(price * qty))
        except ValueError:
            self.total_var.set("Ошибка")

    def validate_input(self):
        drink = self.drink_var.get().strip()
        if not drink or drink not in self.menu_prices:
            messagebox.showerror("Ошибка ввода", "Выберите напиток из списка.")
            return None
        try:
            qty = int(self.qty_var.get().strip())
            if qty <= 0 or qty > 100:
                raise ValueError
        except ValueError:
            messagebox.showerror("Ошибка ввода", "Количество должно быть целым числом от 1 до 100.")
            return None
        total = self.menu_prices[drink] * qty
        comment = self.comment_var.get().strip()
        status = self.status_var.get()
        return drink, qty, total, comment, status

    def add_order(self):
        data = self.validate_input()
        if not data:
            return
        drink, qty, total, comment, _ = data
        order = {
            "id": self.next_id,
            "drink": drink,
            "qty": qty,
            "total": total,
            "comment": comment,
            "status": "Готовится"
        }
        self.orders.append(order)
        self.next_id += 1
        self.clear_form()
        self.refresh_table()

    def on_select_order(self, event):
        selected = self.tree.selection()
        if not selected:
            return
        item_values = self.tree.item(selected[0], "values")
        order_id = int(item_values[0])
        for order in self.orders:
            if order["id"] == order_id:
                self.id_var.set(str(order["id"]))
                self.drink_var.set(order["drink"])
                self.qty_var.set(str(order["qty"]))
                self.total_var.set(str(order["total"]))
                self.comment_var.set(order["comment"])
                self.status_var.set(order["status"])
                break

    def update_order(self):
        if self.id_var.get() == "Авто":
            messagebox.showwarning("Внимание", "Сначала выберите заказ из списка для изменения.")
            return
        data = self.validate_input()
        if not data:
            return
        order_id = int(self.id_var.get())
        drink, qty, total, comment, new_status = data
        for order in self.orders:
            if order["id"] == order_id:
                if order["status"] == "Выдан" and new_status == "Готовится":
                    messagebox.showerror("Ошибка статуса", "Нельзя вернуть выданный заказ обратно в работу.")
                    return
                order["drink"] = drink
                order["qty"] = qty
                order["total"] = total
                order["comment"] = comment
                order["status"] = new_status
                break
        self.refresh_table()
        messagebox.showinfo("Успех", f"Заказ №{order_id} обновлён.")

    def mark_issued(self):
        if self.id_var.get() == "Авто":
            messagebox.showwarning("Внимание", "Выберите заказ из списка.")
            return
        order_id = int(self.id_var.get())
        for order in self.orders:
            if order["id"] == order_id:
                if order["status"] == "Выдан":
                    messagebox.showinfo("Информация", "Заказ уже имеет статус «Выдан».")
                    return
                order["status"] = "Выдан"
                self.status_var.set("Выдан")
                break
        self.refresh_table()

    def delete_order(self):
        if self.id_var.get() == "Авто":
            messagebox.showwarning("Внимание", "Выберите заказ из списка для удаления.")
            return
        order_id = int(self.id_var.get())
        confirm = messagebox.askyesno("Подтверждение удаления", f"Вы уверены, что хотите удалить заказ №{order_id}?")
        if confirm:
            self.orders = [o for o in self.orders if o["id"] != order_id]
            self.clear_form()
            self.refresh_table()

    def clear_form(self):
        self.id_var.set("Авто")
        self.drink_var.set("Капучино")
        self.qty_var.set("1")
        self.total_var.set("220")
        self.comment_var.set("")
        self.status_var.set("Готовится")
        for item in self.tree.selection():
            self.tree.selection_remove(item)

    def reset_filters(self):
        self.search_var.set("")
        self.filter_status_var.set("Все")
        self.refresh_table()

    def update_stats(self):
        total_orders = len(self.orders)
        preparing = sum(1 for o in self.orders if o["status"] == "Готовится")
        revenue = sum(o["total"] for o in self.orders)
        self.stats_var.set(f"Заказов: {total_orders}  |  Готовится: {preparing}  |  Выручка: {revenue} ₽")

    def refresh_table(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        search_query = self.search_var.get().strip()
        status_filter = self.filter_status_var.get()

        for order in self.orders:
            if search_query and str(order["id"]) != search_query:
                continue
            if status_filter != "Все" and order["status"] != status_filter:
                continue
            tag = "done" if order["status"] == "Выдан" else "prep"
            self.tree.insert(
                "",
                "end",
                values=(order["id"], order["drink"], order["qty"], order["total"], order["comment"], order["status"]),
                tags=(tag,)
            )

        self.update_stats()


if __name__ == "__main__":
    root = tk.Tk()
    app = CoffeeShopApp(root)
    root.mainloop()
