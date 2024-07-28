import customtkinter as ctk
from tkinter import messagebox


class Habit:
    def __init__(self, name):
        self.name = name
        self.count = 0

    def increment(self):
        self.count += 1


class HabitTracker:
    def __init__(self):
        self.habits = {}

    def add_habit(self, habit):
        if habit not in self.habits:
            self.habits[habit] = Habit(habit)
            return True
        return False

    def remove_habit(self, habit):
        if habit in self.habits:
            del self.habits[habit]
            return True
        return False


class HabitTrackerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.tracker = HabitTracker()
        self.title("Habit Tracker")
        self.geometry("800x500")

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.create_widgets()

    def create_widgets(self):
        title = ctk.CTkLabel(self, text="Habit Tracker",
                             font=("Arial", 24, "bold"))
        title.grid(row=0, column=0, columnspan=3, pady=20)

        self.habit_entry = ctk.CTkEntry(
            self, placeholder_text="Enter habit name", width=300)
        self.habit_entry.grid(row=1, column=0, columnspan=1,
                              padx=20, pady=10, sticky="ew")
        self.habit_entry.bind("<Return>", lambda event: self.add_habit())

        add_button = ctk.CTkButton(
            self, text="Add Habit", command=self.add_habit, width=100)
        add_button.grid(row=1, column=1, padx=5, pady=10)

        remove_button = ctk.CTkButton(
            self, text="Remove Habit", command=self.remove_habit, width=100)
        remove_button.grid(row=1, column=2, padx=5, pady=10)

        self.habits_frame = ctk.CTkScrollableFrame(self, height=300)
        self.habits_frame.grid(row=2, column=0, columnspan=3,
                               padx=20, pady=10, sticky="nsew")

    def add_habit(self):
        habit = self.habit_entry.get()
        if habit:
            if self.tracker.add_habit(habit):
                messagebox.showinfo("Success", f"Habit '{
                                    habit}' added successfully.")
                self.habit_entry.delete(0, 'end')
                self.update_habits_list()
            else:
                messagebox.showerror("Error", f"Habit '{
                                     habit}' already exists.")
        else:
            messagebox.showerror("Error", "Please enter a habit name.")

    def remove_habit(self):
        habit = self.habit_entry.get()
        if habit:
            if self.tracker.remove_habit(habit):
                messagebox.showinfo("Success", f"Habit '{
                                    habit}' removed successfully.")
                self.habit_entry.delete(0, 'end')
                self.update_habits_list()
            else:
                messagebox.showerror("Error", f"Habit '{habit}' not found.")
        else:
            messagebox.showerror("Error", "Please enter a habit name.")

    def update_habits_list(self):
        for widget in self.habits_frame.winfo_children():
            widget.destroy()

        for row, (habit_name, habit) in enumerate(self.tracker.habits.items()):
            label = ctk.CTkLabel(self.habits_frame, text=f"{habit_name}\tCount: {
                                 habit.count}", anchor="w", width=300)
            label.grid(row=row, column=0, padx=5, pady=5, sticky="w")

            finished_button = ctk.CTkButton(self.habits_frame, text="Finished",
                                            command=lambda h=habit: self.mark_finished(h), width=100)
            finished_button.grid(row=row, column=1, padx=5, pady=5)

    def mark_finished(self, habit):
        habit.increment()
        self.update_habits_list()


if __name__ == "__main__":
    app = HabitTrackerApp()
    app.mainloop()
