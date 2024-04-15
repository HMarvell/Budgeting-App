import tkinter as tk

class BudgetApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Budget App")

        # Dictionary to store incomes and expenses
        self.incomes = {}
        self.expenses = {}
        self.expense_categories = {}

        # Initialize budget values
        self.budget = 0.0
        self.total_expenses = 0.0

        # Frame for income input
        self.income_frame = tk.Frame(self.root)
        self.income_frame.pack(pady=10)

        # Frame for expense input
        self.expense_frame = tk.Frame(self.root)
        self.expense_frame.pack(pady=10)

        # Frame for budget tracking
        self.budget_frame = tk.Frame(self.root)
        self.budget_frame.pack(pady=10)

        # Labels and entries for income input
        self.income_label = tk.Label(self.income_frame, text="Income:")
        self.income_label.grid(row=0, column=0)

        self.income_entry = tk.Entry(self.income_frame)
        self.income_entry.grid(row=0, column=1)

        self.add_income_button = tk.Button(self.income_frame, text="Add Income", command=self.add_income)
        self.add_income_button.grid(row=0, column=2)

        # Labels and entries for expense input
        self.expense_label = tk.Label(self.expense_frame, text="Expense:")
        self.expense_label.grid(row=0, column=0)

        self.expense_entry = tk.Entry(self.expense_frame)
        self.expense_entry.grid(row=0, column=1)

        self.expense_category_label = tk.Label(self.expense_frame, text="Category:")
        self.expense_category_label.grid(row=0, column=2)

        self.expense_category_entry = tk.Entry(self.expense_frame)
        self.expense_category_entry.grid(row=0, column=3)

        self.add_expense_button = tk.Button(self.expense_frame, text="Add Expense", command=self.add_expense)
        self.add_expense_button.grid(row=0, column=4)

        # Listbox for displaying incomes
        self.income_listbox = tk.Listbox(self.root, width=40)
        self.income_listbox.pack(pady=10)
        self.income_listbox.bind("<<ListboxSelect>>", self.select_income)

        # Listbox for displaying expenses
        self.expense_listbox = tk.Listbox(self.root, width=40)
        self.expense_listbox.pack(pady=10)
        self.expense_listbox.bind("<<ListboxSelect>>", self.select_expense)

        # Labels for budget tracking
        self.expense_total_label = tk.Label(self.budget_frame, text="Total Expenses: $0.00")
        self.expense_total_label.grid(row=0, column=0, padx=10)

        self.expected_remainder_label = tk.Label(self.budget_frame, text="Expected Remainder: $0.00")
        self.expected_remainder_label.grid(row=0, column=1, padx=10)

        self.budget_balance_label = tk.Label(self.budget_frame, text="Budget Balance: $0.00")
        self.budget_balance_label.grid(row=0, column=2, padx=10)

        # Button for deleting selected income or expense
        self.delete_button = tk.Button(self.root, text="Delete Selected", command=self.delete_selected)
        self.delete_button.pack(pady=5)

    def add_income(self):
        income = self.income_entry.get()
        if income:
            self.incomes[len(self.incomes) + 1] = float(income)
            self.income_entry.delete(0, tk.END)
            self.update_income_listbox()
            self.calculate_budget()
        else:
            print("Please enter a valid income amount.")

    def add_expense(self):
        expense = self.expense_entry.get()
        category = self.expense_category_entry.get()
        if expense and category:
            self.expenses[len(self.expenses) + 1] = float(expense)
            self.expense_categories[len(self.expenses)] = category
            self.expense_entry.delete(0, tk.END)
            self.expense_category_entry.delete(0, tk.END)
            self.update_expense_listbox()
            self.calculate_budget()
        else:
            print("Please enter a valid expense amount and category.")

    def update_income_listbox(self):
        self.income_listbox.delete(0, tk.END)
        for index, income in self.incomes.items():
            self.income_listbox.insert(tk.END, f"Income {index}: ${income:.2f}")

    def update_expense_listbox(self):
        self.expense_listbox.delete(0, tk.END)
        for index, expense in self.expenses.items():
            category = self.expense_categories[index]
            self.expense_listbox.insert(tk.END, f"Expense {index}: ${expense:.2f} ({category})")

    def select_income(self, event):
        selection = self.income_listbox.curselection()
        if selection:
            selected_index = selection[0] + 1
            income = self.incomes[selected_index]
            self.income_entry.delete(0, tk.END)
            self.income_entry.insert(tk.END, income)

    def select_expense(self, event):
        selection = self.expense_listbox.curselection()
        if selection:
            selected_index = selection[0] + 1
            expense = self.expenses[selected_index]
            category = self.expense_categories[selected_index]
            self.expense_entry.delete(0, tk.END)
            self.expense_entry.insert(tk.END, expense)
            self.expense_category_entry.delete(0, tk.END)
            self.expense_category_entry.insert(tk.END, category)

    def delete_selected(self):
        income_selection = self.income_listbox.curselection()
        if income_selection:
            selected_index = income_selection[0] + 1
            del self.incomes[selected_index]
            self.update_income_listbox()
            self.calculate_budget()
            return

        expense_selection = self.expense_listbox.curselection()
        if expense_selection:
            selected_index = expense_selection[0] + 1
            del self.expenses[selected_index]
            del self.expense_categories[selected_index]
            self.update_expense_listbox()
            self.calculate_budget()

    def calculate_budget(self):
        self.total_expenses = sum(self.expenses.values())
        total_income = sum(self.incomes.values())
        self.budget = total_income - self.total_expenses
        self.update_display()

    def update_display(self):
        self.expense_total_label.config(text="Total Expenses: ${:.2f}".format(self.total_expenses))
        self.expected_remainder_label.config(text="Expected Remainder: ${:.2f}".format(self.budget))
        self.budget_balance_label.config(text="Budget Balance: ${:.2f}".format(self.budget))


if __name__ == "__main__":
    root = tk.Tk()
    app = BudgetApp(root)
    root.mainloop()
