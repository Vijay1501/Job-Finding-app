import tkinter as tk
from tkinter import filedialog, ttk
from PIL import Image, ImageTk
import time
import webbrowser
from keywords import Extractor  # Import the Extractor class from keywords.py

class JobMatchingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Job Matching App")
        self.root.geometry("430x932")  # iPhone 15 Pro size
        self.root.configure(bg="#000000")  # Black background
        
        self.extractor = Extractor()  # Initialize the Extractor
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
            
            self.root.after(500, self.animate_progress, lambda: self.process_resume(file_path))
    
    def process_resume(self, file_path):
        """Processes the uploaded resume and extracts skills."""
        resume_text = self.extractor.return_resume_text(file_path)
        if resume_text:
            skills = self.extractor.extract_skills(resume_text)
            self.show_skills_page(skills)
        else:
            self.show_skills_page("Error reading the file.")
    
    def show_skills_page(self, skills):
        """Displays the extracted skills."""
        self.clear_screen()
        
        container = tk.Frame(self.root, bg="#000000")
        container.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        self.skills_label = tk.Label(container, text="Extracted Skills", font=("Arial", 18, "bold"), bg="#000000", fg="#ffffff")
        self.skills_label.pack(pady=20)
        
        self.skills_text = tk.Text(container, wrap=tk.WORD, width=40, height=10, font=("Arial", 12), bg="#000000", fg="#ffffff")
        self.skills_text.insert(tk.END, skills)
        self.skills_text.pack(pady=20)
        
        self.find_jobs_button = tk.Button(container, text="Find Jobs", command=self.show_find_jobs_page, font=("Arial", 14, "bold"), bg="#ffffff", fg="#000000", padx=20, pady=10, relief="flat", bd=0, width=20)
        self.find_jobs_button.pack(pady=20)
    
    def show_find_jobs_page(self):
        """Displays the job search results in a card layout."""
        self.clear_screen()
        
        # Define the container for the job cards
        container = tk.Frame(self.root, bg="#000000")
        container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Job data
        jobs = [
            {"company": "Google", "title": "Software Engineer", "due_date": "March 5, 2025", "link": "https://google.com/jobs"},
            {"company": "Microsoft", "title": "Python Developer", "due_date": "March 10, 2025", "link": "https://microsoft.com/careers"},
            {"company": "Amazon", "title": "Data Scientist", "due_date": "March 15, 2025", "link": "https://amazon.jobs"},
        ]
        
        # Create a card for each job
        for job in jobs:
            card = tk.Frame(container, bg="#1e1e1e", padx=20, pady=20, relief=tk.RAISED, bd=2)
            card.pack(fill=tk.X, pady=10, padx=10)
            
            # Company Name
            company_label = tk.Label(card, text=job["company"], font=("Arial", 16, "bold"), bg="#1e1e1e", fg="#ffffff")
            company_label.pack(anchor="w", pady=(0, 5))
            
            # Job Title
            title_label = tk.Label(card, text=job["title"], font=("Arial", 14), bg="#1e1e1e", fg="#ffffff")
            title_label.pack(anchor="w", pady=(0, 5))
            
            # Due Date
            due_date_label = tk.Label(card, text=f"Due Date: {job['due_date']}", font=("Arial", 12), bg="#1e1e1e", fg="#ffffff")
            due_date_label.pack(anchor="w", pady=(0, 10))
            
            # Apply Button
            apply_button = tk.Button(card, text="Apply Now", font=("Arial", 12, "bold"), bg="#ffffff", fg="#000000", 
                                    command=lambda link=job["link"]: webbrowser.open(link))
            apply_button.pack(anchor="e")
    
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