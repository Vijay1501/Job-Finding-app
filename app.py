import tkinter as tk
from tkinter import filedialog, ttk
from PIL import Image, ImageTk
import time
import webbrowser

class JobMatchingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Job Matching App")
        self.root.geometry("430x932")  # iPhone 15 Pro size
        self.root.configure(bg="#000000")  # Black background
        
        self.show_welcome_page()
    
    def show_welcome_page(self):
        """Displays the welcome page centered with a stylish animated loading screen."""
        self.clear_screen()
        
        container = tk.Frame(self.root, bg="#000000")
        container.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        self.welcome_label = tk.Label(container, text="Welcome to Job Matching App", font=("Arial", 20, "bold"), bg="#000000", fg="#ffffff")
        self.welcome_label.pack(pady=20)
        
        self.loading_label = tk.Label(container, text="Loading...", font=("Arial", 14), bg="#000000", fg="#ffffff")
        self.loading_label.pack()
        
        self.progress = ttk.Progressbar(container, orient=tk.HORIZONTAL, length=300, mode='determinate', style="TProgressbar")
        self.progress.pack(pady=20)
        
        self.root.after(500, self.animate_progress, self.show_upload_page)
    
    def animate_progress(self, next_step):
        """Animates the progress bar dynamically."""
        for i in range(0, 101, 5):
            self.progress['value'] = i
            self.root.update_idletasks()
            time.sleep(0.2)
        next_step()
    
    def show_upload_page(self):
        """Displays the page asking for resume upload."""
        self.clear_screen()
        
        container = tk.Frame(self.root, bg="#000000")
        container.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        self.file_icon = Image.open("file_icon.jpg")  # Placeholder for file icon
        self.file_icon = self.file_icon.resize((50, 50))
        self.file_icon = ImageTk.PhotoImage(self.file_icon)
        self.icon_label = tk.Label(container, image=self.file_icon, bg="#000000")
        self.icon_label.pack(pady=10)
        
        self.upload_label = tk.Label(container, text="Upload Your Resume", font=("Arial", 18, "bold"), bg="#000000", fg="#ffffff")
        self.upload_label.pack(pady=10)
        
        self.upload_button = tk.Button(container, text="Select File", command=self.upload_file, font=("Arial", 14, "bold"), bg="#ffffff", fg="#000000", padx=20, pady=10, relief="flat", bd=0, width=20)
        self.upload_button.pack(pady=10)
        
        self.file_name_label = tk.Label(container, text="No file selected", font=("Arial", 12), bg="#000000", fg="#ffffff")
        self.file_name_label.pack(pady=5)
    
    def upload_file(self):
        """Handles file upload with animation and transitions to find jobs page."""
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("PDF files", "*.pdf"), ("Word files", "*.docx")])
        if file_path:
            file_name = file_path.split("/")[-1]
            self.file_name_label.config(text=file_name)
            
            self.clear_screen()
            
            container = tk.Frame(self.root, bg="#000000")
            container.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
            
            self.uploading_label = tk.Label(container, text="Uploading...", font=("Arial", 14), bg="#000000", fg="#ffffff")
            self.uploading_label.pack()
            
            self.progress = ttk.Progressbar(container, orient=tk.HORIZONTAL, length=300, mode='determinate', style="TProgressbar")
            self.progress.pack(pady=20)
            
            self.root.after(500, self.animate_progress, self.show_find_jobs_page)
    
    def show_find_jobs_page(self):
        """Displays a page with a button to find jobs."""
        self.clear_screen()
        
        container = tk.Frame(self.root, bg="#000000")
        container.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        self.find_jobs_label = tk.Label(container, text="Ready to Find Jobs?", font=("Arial", 18, "bold"), bg="#000000", fg="#ffffff")
        self.find_jobs_label.pack(pady=20)
        
        self.find_jobs_button = tk.Button(container, text="Find Jobs", command=self.show_job_search_page, font=("Arial", 14, "bold"), bg="#ffffff", fg="#000000", padx=20, pady=10, relief="flat", bd=0, width=20)
        self.find_jobs_button.pack(pady=20)
    
    def show_job_search_page(self):
        """Displays the job search results in table format."""
        self.clear_screen()
        
        container = tk.Frame(self.root, bg="#000000")
        container.pack(fill=tk.BOTH, expand=True)
        
        columns = ("S.No", "Company", "Job Title", "Due Date", "Link")
        self.tree = ttk.Treeview(container, columns=columns, show="headings")
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center", width=100)
        
        jobs = [(1, "Google", "Software Engineer", "March 5, 2025", "https://google.com/jobs"),
                (2, "Microsoft", "Python Developer", "March 10, 2025", "https://microsoft.com/careers"),
                (3, "Amazon", "Data Scientist", "March 15, 2025", "https://amazon.jobs")]
        
        for job in jobs:
            self.tree.insert("", tk.END, values=job)
        
        self.tree.pack(pady=20)
        self.tree.bind("<Double-1>", self.open_link)
    
    def open_link(self, event):
        selected_item = self.tree.selection()[0]
        link = self.tree.item(selected_item, "values")[4]
        webbrowser.open(link)
    
    def clear_screen(self):
        """Removes all widgets from the window."""
        for widget in self.root.winfo_children():
            widget.destroy()
        
if __name__ == "__main__":
    root = tk.Tk()
    style = ttk.Style()
    style.configure("TProgressbar", troughcolor="#ffffff", background="#ffffff", thickness=10)
    app = JobMatchingApp(root)
    root.mainloop()
