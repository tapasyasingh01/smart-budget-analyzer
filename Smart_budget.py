import pandas as pd
import matplotlib.pyplot as plt
import os

class SmartBudgetAnalyser:
    def __init__(self, filename="budget_data.csv", limit_file="budget_limit.txt"):
        self.filename = filename
        self.limit_file = limit_file
        self.budget_limit = self.load_budget_limit()
        self.load_data()

    def load_budget_limit(self):
        # Saved budget limit load karna
        if os.path.exists(self.limit_file):
            try:
                with open(self.limit_file, "r") as f:
                    return float(f.read().strip())
            except Exception:
                return 0.0
        return 0.0

    def save_budget_limit(self, limit):
        self.budget_limit = float(limit)
        with open(self.limit_file, "w") as f:
            f.write(str(self.budget_limit))
        print(f"\n✅ Monthly Budget Limit successfully set to ₹{self.budget_limit}!")

    def load_data(self):
        if os.path.exists(self.filename):
            try:
                self.df = pd.read_csv(self.filename)
            except Exception as e:
                self.df = pd.DataFrame(columns=["Type", "Category", "Amount", "Description"])
        else:
            self.df = pd.DataFrame(columns=["Type", "Category", "Amount", "Description"])

    def save_data(self):
        self.df.to_csv(self.filename, index=False)

    def add_transaction(self, t_type, category, amount, description):
        new_row = {"Type": t_type, "Category": category, "Amount": float(amount), "Description": description}
        self.df = pd.concat([self.df, pd.DataFrame([new_row])], ignore_index=True)
        self.save_data()
        print(f"\n✅ Successfully added {t_type}: ₹{amount} under '{category}'!")

        # --- BUDGET LIMIT ALERT CHECK ---
        if t_type == "Expense" and self.budget_limit > 0:
            total_expense = self.df[self.df["Type"] == "Expense"]["Amount"].sum()
            
            if total_expense > self.budget_limit:
                print(f"\n🚨 **ALERT!** Aapne apna monthly budget limit cross kar liya hai!")
                print(f"⚠️ Total Expenses: ₹{total_expense} (Budget Limit: ₹{self.budget_limit}) — Over Budget by ₹{total_expense - self.budget_limit}!")
            elif total_expense >= (self.budget_limit * 0.8):
                print(f"\n⚠️ **WARNING!** Aapne apne budget ka 80% ya usse zyada use kar liya hai!")
                print(f"💡 Current Expenses: ₹{total_expense} / ₹{self.budget_limit}")

    def show_summary(self):
        if self.df.empty:
            print("\n⚠️ Abhi tak koi transaction add nahi kiya gaya hai.")
            return

        total_income = self.df[self.df["Type"] == "Income"]["Amount"].sum()
        total_expense = self.df[self.df["Type"] == "Expense"]["Amount"].sum()
        balance = total_income - total_expense

        print("\n" + "="*35)
        print("         BUDGET SUMMARY         ")
        print("="*35)
        print(f"💰 Total Income   : ₹{total_income}")
        print(f"💸 Total Expense  : ₹{total_expense}")
        print(f"💼 Net Balance    : ₹{balance}")
        
        if self.budget_limit > 0:
            print(f"🎯 Budget Limit   : ₹{self.budget_limit}")
            if total_expense > self.budget_limit:
                print(f"🚨 Status         : OVER BUDGET by ₹{total_expense - self.budget_limit}")
            else:
                print(f"✅ Status         : Safe (₹{self.budget_limit - total_expense} remaining)")
        else:
            print("⚠️ Budget Limit   : Not Set (Option 4 se set karein)")
        print("="*35)

        print("\n--- Recent Transactions ---")
        print(self.df.tail(5).to_string(index=False))

    def plot_expenses(self):
        expense_df = self.df[self.df["Type"] == "Expense"]
        if expense_df.empty:
            print("\n⚠️ Koi Expense (Kharcha) record nahi mila plot karne ke liye!")
            return

        category_expense = expense_df.groupby("Category")["Amount"].sum()

        plt.figure(figsize=(8, 5))
        category_expense.plot(kind="pie", autopct='%1.1f%%', startangle=140, cmap="Set3")
        plt.title("Expense Breakdown by Category")
        plt.ylabel("") 
        plt.tight_layout()
        plt.show()

# --- Interactive Menu Loop for Colab ---
def main():
    app = SmartBudgetAnalyser()
    
    while True:
        print("\n*** SMART BUDGET ANALYSER (WITH ALERTS) ***")
        print("1. Add Income")
        print("2. Add Expense")
        print("3. View Summary & Budget Status")
        print("4. Set / Update Monthly Budget Limit")
        print("5. Show Expense Chart")
        print("6. Exit")
        
        choice = input("Apna choice enter karein (1-6): ").strip()
        
        if choice == '1':
            category = input("Income Category (jaise Salary, Pocket Money): ").strip()
            try:
                amount = float(input("Amount enter karein (₹): "))
                desc = input("Description/Notes: ").strip()
                app.add_transaction("Income", category, amount, desc)
            except ValueError:
                print("❌ Invalid amount! Kripya sahi number enter karein.")
                
        elif choice == '2':
            category = input("Expense Category (jaise Food, Travel, Shopping): ").strip()
            try:
                amount = float(input("Amount enter karein (₹): "))
                desc = input("Description/Notes: ").strip()
                app.add_transaction("Expense", category, amount, desc)
            except ValueError:
                print("❌ Invalid amount! Kripya sahi number enter karein.")
                
        elif choice == '3':
            app.show_summary()
            
        elif choice == '4':
            try:
                limit = float(input("Apna monthly budget limit enter karein (₹): "))
                app.save_budget_limit(limit)
            except ValueError:
                print("❌ Invalid limit amount!")
                
        elif choice == '5':
            app.plot_expenses()
            
        elif choice == '6':
            print("\n🙏 Thank you for using Smart Budget Analyser! Project data saved.")
            break
        else:
            print("❌ Galat choice! Kripya 1 se 6 ke beech mein select karein.")

if __name__ == "__main__":
    main()
