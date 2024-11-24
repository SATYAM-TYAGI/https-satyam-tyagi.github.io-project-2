import tkinter as tk
from tkinter import messagebox, filedialog
import pandas as pd
import os
from PIL import Image, ImageTk

class ExpenseTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker")
        self.root.geometry("600x400")
        
        self.data = []
        self.df = pd.DataFrame(self.data, columns=['Date', 'Category', 'Description', 'Amount', 'Payment Method', 'Comments'])
        
        self.create_widgets()
    
    def create_widgets(self):
        self.canvas = tk.Canvas(self.root, width=600, height=400)
        self.canvas.pack(fill="both", expand=True)
        
        self.bg_image = ImageTk.PhotoImage(Image.open("expensetrackerbg.png"))
        self.canvas.create_image(0, 0, image=self.bg_image, anchor="nw")
        
        self.form_frame = tk.Frame(self.root, bg="lightblue", bd=5)
        self.form_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        tk.Label(self.form_frame, text="Date (YYYY-MM-DD):", bg="lightblue").grid(row=0, column=0, padx=10, pady=5)
        self.date_entry = tk.Entry(self.form_frame)
        self.date_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(self.form_frame, text="Category:", bg="lightblue").grid(row=1, column=0, padx=10, pady=5)
        self.category_entry = tk.Entry(self.form_frame)
        self.category_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(self.form_frame, text="Description:", bg="lightblue").grid(row=2, column=0, padx=10, pady=5)
        self.description_entry = tk.Entry(self.form_frame)
        self.description_entry.grid(row=2, column=1, padx=10, pady=5)

        tk.Label(self.form_frame, text="Amount:", bg="lightblue").grid(row=3, column=0, padx=10, pady=5)
        self.amount_entry = tk.Entry(self.form_frame)
        self.amount_entry.grid(row=3, column=1, padx=10, pady=5)
        
        tk.Label(self.form_frame, text="Payment Method:", bg="lightblue").grid(row=4, column=0, padx=10, pady=5)
        self.payment_method_entry = tk.Entry(self.form_frame)
        self.payment_method_entry.grid(row=4, column=1, padx=10, pady=5)
        
        tk.Label(self.form_frame, text="Comments:", bg="lightblue").grid(row=5, column=0, padx=10, pady=5)
        self.comments_entry = tk.Entry(self.form_frame)
        self.comments_entry.grid(row=5, column=1, padx=10, pady=5)

        tk.Button(self.form_frame, text="Add Expense", command=self.add_expense, bg="green", fg="white").grid(row=6, column=0, columnspan=2, pady=10)
        tk.Button(self.form_frame, text="Generate Report", command=self.generate_report, bg="blue", fg="white").grid(row=7, column=0, columnspan=2, pady=10)
        tk.Button(self.form_frame, text="Save", command=self.save_to_file, bg="orange", fg="white").grid(row=8, column=0, columnspan=2, pady=10)
        tk.Button(self.form_frame, text="Load", command=self.load_from_file, bg="purple", fg="white").grid(row=9, column=0, columnspan=2, pady=10)
        tk.Button(self.form_frame, text="View by Category", command=self.view_by_category, bg="darkred", fg="white").grid(row=10, column=0, columnspan=2, pady=10)
        
    def add_expense(self):
        date = self.date_entry.get()
        category = self.category_entry.get()
        description = self.description_entry.get()
        amount = self.amount_entry.get()
        payment_method = self.payment_method_entry.get()
        comments = self.comments_entry.get()
        
        if date and category and description and amount and payment_method:
            try:
                amount = float(amount)
                new_expense = pd.DataFrame({
                    'Date': [date], 
                    'Category': [category], 
                    'Description': [description], 
                    'Amount': [amount],
                    'Payment Method': [payment_method],
                    'Comments': [comments]
                })
                if not new_expense.empty and new_expense.notna().all().all():
                    self.df = pd.concat([self.df, new_expense], ignore_index=True)
                    messagebox.showinfo("Success", "Expense added successfully!")
                    self.clear_entries()
                else:
                    messagebox.showerror("Error", "Invalid data.")
            except ValueError:
                messagebox.showerror("Error", "Amount should be a number.")
        else:
            messagebox.showerror("Error", "All fields except comments are required.")
    
    def generate_report(self):
        report_window = tk.Toplevel(self.root)
        report_window.title("Expense Report")
        
        text = tk.Text(report_window)
        text.pack()
        
        if not self.df.empty:
            report = self.df.groupby('Category')['Amount'].sum().reset_index()
            report_text = report.to_string(index=False)
            text.insert(tk.END, report_text)
        else:
            text.insert(tk.END, "No expenses recorded.")
        
    def view_by_category(self):
        category_window = tk.Toplevel(self.root)
        category_window.title("Expenses by Category")
        
        text = tk.Text(category_window)
        text.pack()
        
        if not self.df.empty:
            for category, group in self.df.groupby('Category'):
                text.insert(tk.END, f"\nCategory: {category}\n")
                text.insert(tk.END, group.to_string(index=False))
                text.insert(tk.END, "\n\n")
        else:
            text.insert(tk.END, "No expenses recorded.")
    
    def save_to_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if file_path:
            self.df.to_csv(file_path, index=False)
            messagebox.showinfo("Success", "Data saved successfully!")
    
    def load_from_file(self):
        file_path = filedialog.askopenfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if file_path and os.path.exists(file_path):
            self.df = pd.read_csv(file_path)
            messagebox.showinfo("Success", "Data loaded successfully!")
    
    def clear_entries(self):
        self.date_entry.delete(0, tk.END)
        self.category_entry.delete(0, tk.END)
        self.description_entry.delete(0, tk.END)
        self.amount_entry.delete(0, tk.END)
        self.payment_method_entry.delete(0, tk.END)
        self.comments_entry.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTracker(root)
    root.mainloop()
