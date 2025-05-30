import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from tkinter.font import Font
from datetime import datetime
import csv
import os

class FloralTaskManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Floral Task Manager")
        self.root.geometry("1000x700")
        self.root.minsize(800, 600)
        
        # Floral Dark Theme Colors
        self.bg_color = "#1a1a2e"
        self.card_color = "#16213e"
        self.text_color = "#e6e6e6"
        self.accent_color = "#4a6baf"
        self.danger_color = "#d9534f"
        self.success_color = "#5cb85c"
        self.completed_color = "#4CAF50"
        
        # Initialize CSV Data
        self.csv_file = "tasks.csv"
        self.tasks = []
        self.load_tasks()
        
        # Load floral background
        self.load_background()
        
        # Configure Styles
        self.configure_styles()
        
        # Create UI
        self.create_widgets()
        
        # Track currently edited task
        self.current_edit_id = None
    
    def load_background(self):
        """Create a floral background effect"""
        try:
            # Create gradient background with floral pattern
            self.bg_canvas = tk.Canvas(self.root, bg=self.bg_color, highlightthickness=0)
            self.bg_canvas.pack(fill="both", expand=True)
            
            # Floral pattern overlay (simulated with circles)
            for i in range(0, 1000, 100):
                for j in range(0, 700, 100):
                    self.bg_canvas.create_oval(
                        i+10, j+10, i+30, j+30,
                        fill="#4a6baf", outline="", alpha=0.1
                    )
                    self.bg_canvas.create_oval(
                        i+30, j+30, i+50, j+50,
                        fill="#d9534f", outline="", alpha=0.1
                    )
        except:
            # Fallback if floral pattern fails
            self.root.configure(bg=self.bg_color)
    
    def configure_styles(self):

        """Set up modern dark theme with floral accents"""
        self.style = ttk.Style()
        self.style.theme_use("clam")
        
        # Base Styles
        self.style.configure(".", background=self.bg_color, foreground=self.text_color)
        self.style.configure("TFrame", background=self.bg_color)
        self.style.configure("TLabel", background=self.bg_color, foreground=self.text_color)
        self.style.configure("TButton", 
                            background=self.accent_color,
                            foreground=self.text_color,
                            borderwidth=0,
                            padding=8,
                            font=("Helvetica", 10))
        self.style.map("TButton",
                      background=[("active", "#3a5a9f"), ("pressed", "#2a4a8f")])
        self.style.configure("TEntry",
                            fieldbackground=self.card_color,
                            foreground=self.text_color,
                            insertcolor=self.text_color,
                            borderwidth=0,
                            padding=8)
        self.style.configure("TCombobox",
                            fieldbackground=self.card_color,
                            foreground=self.text_color)
        self.style.configure("TNotebook", background=self.bg_color, borderwidth=0)
        self.style.configure("TNotebook.Tab",
                            background=self.bg_color,
                            foreground=self.text_color,
                            padding=[15, 5],
                            font=("Helvetica", 10, "bold"))
        self.style.map("TNotebook.Tab",
                      background=[("selected", self.card_color)])
        
        # Custom Styles
        self.style.configure("Card.TFrame", 
                           background=self.card_color,
                           relief="flat",
                           borderwidth=2,
                           bordercolor="#4a6baf",
                           padding=10)
        self.style.configure("Danger.TButton", background=self.danger_color)
        self.style.configure("Success.TButton", background=self.success_color)
        self.style.configure("Completed.TLabel", 
                           foreground=self.completed_color,
                           font=("Helvetica", 10, "overstrike"))
    
    def create_widgets(self):
        """Build the UI with all functionality"""
        # Main container (on top of background)
        self.main_frame = ttk.Frame(self.bg_canvas)
        self.main_frame.place(relx=0.5, rely=0.5, anchor="center", width=950, height=650)
        
        # Notebook (Tabs)
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Create Tabs
        self.create_add_tab()
        self.create_show_tab()
        self.create_edit_tab()
        self.create_delete_tab()
        self.create_filter_tab()
    
    def create_add_tab(self):
        """Tab for adding new tasks"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="🌸 Add Task")
        
        # Header
        ttk.Label(tab, 
                 text="Add New Task", 
                 font=("Helvetica", 16, "bold")).pack(pady=15)
        
        # Task Input Form
        form_frame = ttk.Frame(tab)
        form_frame.pack(fill="x", padx=20, pady=10)
        
        # Title
        ttk.Label(form_frame, text="Title:").grid(row=0, column=0, sticky="w", pady=5)
        self.title_entry = ttk.Entry(form_frame, font=("Helvetica", 12))
        self.title_entry.grid(row=0, column=1, sticky="ew", pady=5, padx=(0, 10))
        
        # Description
        ttk.Label(form_frame, text="Description:").grid(row=1, column=0, sticky="w", pady=5)
        self.desc_entry = ttk.Entry(form_frame, font=("Helvetica", 12))
        self.desc_entry.grid(row=1, column=1, sticky="ew", pady=5, padx=(0, 10))
        
        # Due Date
        ttk.Label(form_frame, text="Due Date (YYYY-MM-DD):").grid(row=2, column=0, sticky="w", pady=5)
        self.date_entry = ttk.Entry(form_frame, font=("Helvetica", 12))
        self.date_entry.grid(row=2, column=1, sticky="ew", pady=5, padx=(0, 10))
        
        # Status
        ttk.Label(form_frame, text="Status:").grid(row=3, column=0, sticky="w", pady=5)
        self.status_var = tk.StringVar(value="Not Done")
        status_menu = ttk.Combobox(form_frame, 
                                  textvariable=self.status_var,
                                  values=["Not Done", "Done"],
                                  state="readonly")
        status_menu.grid(row=3, column=1, sticky="ew", pady=5, padx=(0, 10))
        
        # Add Button
        btn_frame = ttk.Frame(tab)
        btn_frame.pack(fill="x", padx=20, pady=10)
        
        ttk.Button(btn_frame, 
                  text="Add Task", 
                  style="Success.TButton", 
                  command=self.add_task).pack(side="right")
        
        # Bind Enter key to add task
        self.date_entry.bind("<Return>", lambda e: self.add_task())
    
    def create_show_tab(self):
        """Tab for displaying all tasks"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="📜 Show Tasks")
        
        # Header
        ttk.Label(tab, 
                 text="Your Tasks", 
                 font=("Helvetica", 16, "bold")).pack(pady=15)
        
        # Task List Container
        container = ttk.Frame(tab)
        container.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Canvas & Scrollbar
        self.canvas = tk.Canvas(container, bg=self.bg_color, highlightthickness=0)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Refresh Button
        btn_frame = ttk.Frame(tab)
        btn_frame.pack(fill="x", padx=20, pady=10)
        
        ttk.Button(btn_frame, 
                  text="🔄 Refresh", 
                  command=self.refresh_tasks).pack(side="right")
        
        # Initial Load
        self.refresh_tasks()
    
    def create_edit_tab(self):
        """Tab for editing existing tasks"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="✏️ Edit Task")
        
        # Header
        ttk.Label(tab, 
                 text="Edit Task", 
                 font=("Helvetica", 16, "bold")).pack(pady=15)
        
        # Task Selection
        selection_frame = ttk.Frame(tab)
        selection_frame.pack(fill="x", padx=20, pady=10)
        
        ttk.Label(selection_frame, text="Select Task:").pack(anchor="w")
        self.edit_combobox = ttk.Combobox(selection_frame, state="readonly", font=("Helvetica", 11))
        self.edit_combobox.pack(fill="x", pady=5)
        self.edit_combobox.bind("<<ComboboxSelected>>", self.load_task_for_edit)
        
        # Edit Form
        form_frame = ttk.Frame(tab)
        form_frame.pack(fill="x", padx=20, pady=10)
        
        # Title
        ttk.Label(form_frame, text="Title:").grid(row=0, column=0, sticky="w", pady=5)
        self.edit_title_entry = ttk.Entry(form_frame, font=("Helvetica", 12))
        self.edit_title_entry.grid(row=0, column=1, sticky="ew", pady=5, padx=(0, 10))
        
        # Description
        ttk.Label(form_frame, text="Description:").grid(row=1, column=0, sticky="w", pady=5)
        self.edit_desc_entry = ttk.Entry(form_frame, font=("Helvetica", 12))
        self.edit_desc_entry.grid(row=1, column=1, sticky="ew", pady=5, padx=(0, 10))
        
        # Due Date
        ttk.Label(form_frame, text="Due Date:").grid(row=2, column=0, sticky="w", pady=5)
        self.edit_date_entry = ttk.Entry(form_frame, font=("Helvetica", 12))
        self.edit_date_entry.grid(row=2, column=1, sticky="ew", pady=5, padx=(0, 10))
        
        # Status
        ttk.Label(form_frame, text="Status:").grid(row=3, column=0, sticky="w", pady=5)
        self.edit_status_var = tk.StringVar()
        edit_status_menu = ttk.Combobox(form_frame, 
                                      textvariable=self.edit_status_var,
                                      values=["Not Done", "Done"],
                                      state="readonly")
        edit_status_menu.grid(row=3, column=1, sticky="ew", pady=5, padx=(0, 10))
        
        # Update Button
        btn_frame = ttk.Frame(tab)
        btn_frame.pack(fill="x", padx=20, pady=10)
        
        ttk.Button(btn_frame, 
                  text="Update Task", 
                  style="Success.TButton", 
                  command=self.update_task).pack(side="right")
        
        # Refresh Combobox
        self.refresh_edit_combobox()
    
    def create_delete_tab(self):
        """Tab for deleting tasks"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="🗑️ Delete Task")
        
        # Header
        ttk.Label(tab, 
                 text="Delete Task", 
                 font=("Helvetica", 16, "bold")).pack(pady=15)
        
        # Task Selection
        selection_frame = ttk.Frame(tab)
        selection_frame.pack(fill="x", padx=20, pady=10)
        
        ttk.Label(selection_frame, text="Select Task:").pack(anchor="w")
        self.delete_combobox = ttk.Combobox(selection_frame, state="readonly", font=("Helvetica", 11))
        self.delete_combobox.pack(fill="x", pady=5)
        
        # Delete Button
        btn_frame = ttk.Frame(tab)
        btn_frame.pack(fill="x", padx=20, pady=10)
        
        ttk.Button(btn_frame, 
                  text="Delete Task", 
                  style="Danger.TButton", 
                  command=self.delete_task).pack(side="right")
        
        # Refresh Combobox
        self.refresh_delete_combobox()
    
    def create_filter_tab(self):

        """Tab for filtering and searching tasks"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="🔍 Filter Tasks")
        
        # Header
        ttk.Label(tab, 
                 text="Filter Tasks", 
                 font=("Helvetica", 16, "bold")).pack(pady=15)
        
        # Filter Options
        filter_frame = ttk.Frame(tab)
        filter_frame.pack(fill="x", padx=20, pady=10)
        
        # Status Filter
        ttk.Label(filter_frame, text="Filter by Status:").grid(row=0, column=0, sticky="w", pady=5)
        self.filter_status_var = tk.StringVar(value="All")
        status_filter = ttk.Combobox(filter_frame, 
                                   textvariable=self.filter_status_var,
                                   values=["All", "Done", "Not Done"],
                                   state="readonly")
        status_filter.grid(row=0, column=1, sticky="ew", pady=5, padx=(0, 10))
        
        # Date Filter
        ttk.Label(filter_frame, text="Filter by Date (YYYY-MM-DD):").grid(row=1, column=0, sticky="w", pady=5)
        self.filter_date_entry = ttk.Entry(filter_frame, font=("Helvetica", 12))
        self.filter_date_entry.grid(row=1, column=1, sticky="ew", pady=5, padx=(0, 10))
        
        # Search
        ttk.Label(filter_frame, text="Search by Title:").grid(row=2, column=0, sticky="w", pady=5)
        self.search_entry = ttk.Entry(filter_frame, font=("Helvetica", 12))
        self.search_entry.grid(row=2, column=1, sticky="ew", pady=5, padx=(0, 10))
        
        # Filter Button
        btn_frame = ttk.Frame(tab)
        btn_frame.pack(fill="x", padx=20, pady=10)
        
        ttk.Button(btn_frame, 
                  text="Apply Filters", 
                  style="Primary.TButton", 
                  command=self.apply_filters).pack(side="right")
        
        # Results Container
        self.filter_results_frame = ttk.Frame(tab)
        self.filter_results_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Initial load
        self.apply_filters()
    
    # ====== CRUD Operations ======
    def add_task(self):

        """Add a new task to CSV"""
        title = self.title_entry.get().strip()
        description = self.desc_entry.get().strip()
        due_date = self.date_entry.get().strip()
        status = self.status_var.get()
        
        if not title:
            messagebox.showwarning("⚠️ Warning", "Title cannot be empty!")
            return
        
        try:
            if due_date:  # Validate date format if provided
                datetime.strptime(due_date, "%Y-%m-%d")
        except ValueError:
            messagebox.showwarning("⚠️ Warning", "Please enter date in YYYY-MM-DD format!")
            return
        
        task_id = len(self.tasks) + 1
        new_task = {
            "id": task_id,
            "title": title,
            "description": description,
            "due_date": due_date,
            "status": status
        }
        
        self.tasks.append(new_task)
        self.save_tasks()
        
        # Clear form
        self.title_entry.delete(0, tk.END)
        self.desc_entry.delete(0, tk.END)
        self.date_entry.delete(0, tk.END)
        self.status_var.set("Not Done")
        
        messagebox.showinfo("✅ Success", "Task added successfully!")
        self.refresh_all()
    
    def update_task(self):

        """Update an existing task"""
        if not self.current_edit_id:
            messagebox.showwarning("⚠️ Warning", "Please select a task to edit!")
            return
        
        title = self.edit_title_entry.get().strip()
        description = self.edit_desc_entry.get().strip()
        due_date = self.edit_date_entry.get().strip()
        status = self.edit_status_var.get()
        
        if not title:
            messagebox.showwarning("⚠️ Warning", "Title cannot be empty!")
            return
        
        try:
            if due_date:  # Validate date format if provided
                datetime.strptime(due_date, "%Y-%m-%d")
        except ValueError:
            messagebox.showwarning("⚠️ Warning", "Please enter date in YYYY-MM-DD format!")
            return
        
        for task in self.tasks:
            if task["id"] == self.current_edit_id:
                task.update({
                    "title": title,
                    "description": description,
                    "due_date": due_date,
                    "status": status
                })
                break
        
        self.save_tasks()
        messagebox.showinfo("✅ Success", "Task updated successfully!")
        self.refresh_all()
    
    def delete_task(self):

        """Delete a task from CSV"""
        selection = self.delete_combobox.get()
        if not selection:
            messagebox.showwarning("⚠️ Warning", "Please select a task to delete!")
            return
        
        task_id = int(selection.split("#")[1].split(":")[0])
        
        if messagebox.askyesno("⚠️ Confirm", "Are you sure you want to delete this task?"):
            self.tasks = [task for task in self.tasks if task["id"] != task_id]
            self.save_tasks()
            messagebox.showinfo("✅ Success", "Task deleted successfully!")
            self.refresh_all()
    
    def toggle_task_status(self, task_id):

        """Toggle task status between Done/Not Done"""
        for task in self.tasks:
            if task["id"] == task_id:
                task["status"] = "Done" if task["status"] == "Not Done" else "Not Done"
                break
        
        self.save_tasks()
        self.refresh_tasks()
        self.refresh_filter_results()
    
    def load_task_for_edit(self, event=None):

        """Load task data into edit form"""
        selection = self.edit_combobox.get()
        if selection:
            task_id = int(selection.split("#")[1].split(":")[0])
            self.current_edit_id = task_id
            task = next((t for t in self.tasks if t["id"] == task_id), None)
            if task:
                self.edit_title_entry.delete(0, tk.END)
                self.edit_title_entry.insert(0, task["title"])
                
                self.edit_desc_entry.delete(0, tk.END)
                self.edit_desc_entry.insert(0, task["description"])
                
                self.edit_date_entry.delete(0, tk.END)
                self.edit_date_entry.insert(0, task["due_date"])
                
                self.edit_status_var.set(task["status"])
    
    def refresh_tasks(self):
        
        """Reload tasks in the Show tab"""
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        if not self.tasks:
            ttk.Label(self.scrollable_frame, text="No tasks found.").pack(pady=20)
            return
        
        for task in self.tasks:
            card = ttk.Frame(self.scrollable_frame, style="Card.TFrame")
            card.pack(fill="x", pady=5, padx=5)
            
            # Task info
            info_frame = ttk.Frame(card)
            info_frame.pack(fill="x", padx=5, pady=5)
            
            # Status checkbox
            status_btn = ttk.Checkbutton(
                info_frame,
                command=lambda tid=task["id"]: self.toggle_task_status(tid)
            )
            status_btn.pack(side="left", padx=(0, 10))
            status_btn.state(["!alternate"])
            if task["status"] == "Done":
                status_btn.state(["selected"])
            
            # Task details
            detail_frame = ttk.Frame(info_frame)
            detail_frame.pack(fill="x", expand=True)
            
            # Title with different style if completed
            title_style = "Completed.TLabel" if task["status"] == "Done" else "TLabel"
            ttk.Label(detail_frame, 
                     text=f"#{task['id']}: {task['title']}", 
                     style=title_style,
                     font=("Helvetica", 11, "bold")).pack(anchor="w")
            
            # Description
            if task["description"]:
                ttk.Label(detail_frame, 
                         text=task["description"],
                         style=title_style).pack(anchor="w")
            
            # Due date
            if task["due_date"]:
                date_label = ttk.Label(detail_frame, 
                                     text=f"📅 Due: {task['due_date']}",
                                     style=title_style)
                date_label.pack(anchor="w")
    
    def refresh_edit_combobox(self):
        """Update task list in Edit tab"""
        values = [f"#{task['id']}: {task['title']}" for task in self.tasks]
        self.edit_combobox["values"] = values
        if values:
            self.edit_combobox.current(0)
            self.load_task_for_edit()
    
    def refresh_delete_combobox(self):
        """Update task list in Delete tab"""
        values = [f"#{task['id']}: {task['title']}" for task in self.tasks]
        self.delete_combobox["values"] = values
        if values:
            self.delete_combobox.current(0)
    
    def apply_filters(self):
        """Apply filters and show results"""
        status_filter = self.filter_status_var.get()
        date_filter = self.filter_date_entry.get().strip()
        search_text = self.search_entry.get().lower().strip()
        
        filtered_tasks = self.tasks.copy()
        
        # Apply status filter
        if status_filter != "All":
            filtered_tasks = [t for t in filtered_tasks if t["status"] == status_filter]
        
        # Apply date filter
        if date_filter:
            try:
                datetime.strptime(date_filter, "%Y-%m-%d")
                filtered_tasks = [t for t in filtered_tasks if t["due_date"] == date_filter]
            except ValueError:
                messagebox.showwarning("⚠️ Warning", "Please enter date in YYYY-MM-DD format!")
                return
        
        # Apply search filter
        if search_text:
            filtered_tasks = [t for t in filtered_tasks if search_text in t["title"].lower()]
        
        # Display results
        self.refresh_filter_results(filtered_tasks)
    
    def refresh_filter_results(self, tasks=None):
        """Refresh the filtered tasks display"""
        if tasks is None:
            tasks = self.tasks
        
        for widget in self.filter_results_frame.winfo_children():
            widget.destroy()
        
        if not tasks:
            ttk.Label(self.filter_results_frame, text="No tasks match your filters.").pack(pady=20)
            return
        
        # Create a canvas for scrollable results
        canvas = tk.Canvas(self.filter_results_frame, bg=self.bg_color, highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.filter_results_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Display filtered tasks
        for task in tasks:
            card = ttk.Frame(scrollable_frame, style="Card.TFrame")
            card.pack(fill="x", pady=5, padx=5)
            
            # Task info
            info_frame = ttk.Frame(card)
            info_frame.pack(fill="x", padx=5, pady=5)
            
            # Status indicator
            status_color = self.completed_color if task["status"] == "Done" else self.accent_color
            status_circle = tk.Canvas(info_frame, width=20, height=20, bg=self.card_color, highlightthickness=0)
            status_circle.create_oval(2, 2, 18, 18, fill=status_color, outline="")
            status_circle.pack(side="left", padx=(0, 10))
            
            # Task details
            detail_frame = ttk.Frame(info_frame)
            detail_frame.pack(fill="x", expand=True)
            
            # Title with different style if completed
            title_style = "Completed.TLabel" if task["status"] == "Done" else "TLabel"
            ttk.Label(detail_frame, 
                     text=f"#{task['id']}: {task['title']}", 
                     style=title_style,
                     font=("Helvetica", 11, "bold")).pack(anchor="w")
            
            # Description
            if task["description"]:
                ttk.Label(detail_frame, 
                         text=task["description"],
                         style=title_style).pack(anchor="w")
            
            # Due date
            if task["due_date"]:
                date_label = ttk.Label(detail_frame, 
                                     text=f"📅 Due: {task['due_date']}",
                                     style=title_style)
                date_label.pack(anchor="w")
    
    def refresh_all(self):
        """Refresh all UI components"""
        self.refresh_tasks()
        self.refresh_edit_combobox()
        self.refresh_delete_combobox()
        self.apply_filters()
    
    # ====== CSV Operations ======
    def load_tasks(self):
        """Load tasks from CSV file"""
        if os.path.exists(self.csv_file):
            try:
                with open(self.csv_file, mode="r", newline="") as file:
                    reader = csv.DictReader(file)
                    self.tasks = []
                    for row in reader:
                        self.tasks.append({
                            "id": int(row["id"]),
                            "title": row["title"],
                            "description": row["description"],
                            "due_date": row["due_date"],
                            "status": row["status"]
                        })
            except Exception as e:
                messagebox.showerror("❌ Error", f"Failed to load tasks: {e}")
                self.tasks = []
        else:
            self.tasks = []
    
    def save_tasks(self):
        """Save tasks to CSV file"""
        try:
            with open(self.csv_file, mode="w", newline="") as file:
                writer = csv.DictWriter(file, fieldnames=["id", "title", "description", "due_date", "status"])
                writer.writeheader()
                writer.writerows(self.tasks)
        except Exception as e:
            messagebox.showerror("❌ Error", f"Failed to save tasks: {e}")

# ====== Run the App ======
if __name__ == "__main__":
    root = tk.Tk()
    app = FloralTaskManager(root)
    root.mainloop()