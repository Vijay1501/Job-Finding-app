import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from PIL import Image, ImageTk
import time
import webbrowser
from keywords import Extractor
import csv
import requests
import threading

class JobMatchingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Job Matching App")
        self.root.geometry("430x932")
        self.root.configure(bg="#000000")
        
        # Set window icon
        try:
            icon_img = Image.open("file_icon.jpg")
            icon_img = ImageTk.PhotoImage(icon_img)
            self.root.iconphoto(True, icon_img)
        except Exception as e:
            print(f"Error loading window icon: {e}")

        self.extractor = Extractor()
        self.show_welcome_page()

    def show_welcome_page(self):
        self.clear_screen()
        
        container = tk.Frame(self.root, bg="#000000")
        container.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        self.welcome_label = tk.Label(container, text="Welcome to Job Matching App", 
                                    font=("Arial", 20, "bold"), bg="#000000", fg="#ffffff")
        self.welcome_label.pack(pady=20)
        
        self.loading_label = tk.Label(container, text="Loading...", font=("Arial", 14), 
                                    bg="#000000", fg="#ffffff")
        self.loading_label.pack()
        
        self.progress = ttk.Progressbar(container, orient=tk.HORIZONTAL, length=300, 
                                      mode='determinate', style="TProgressbar")
        self.progress.pack(pady=20)
        
        self.root.after(500, self.animate_progress, self.show_upload_page)

    def animate_progress(self, next_step):
        for i in range(0, 101, 5):
            self.progress['value'] = i
            self.root.update_idletasks()
            time.sleep(0.2)
        next_step()

    def show_upload_page(self):
        self.clear_screen()
        
        container = tk.Frame(self.root, bg="#000000")
        container.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        self.file_icon = Image.open("file_icon.jpg")
        self.file_icon = self.file_icon.resize((50, 50))
        self.file_icon = ImageTk.PhotoImage(self.file_icon)
        self.icon_label = tk.Label(container, image=self.file_icon, bg="#000000")
        self.icon_label.pack(pady=10)
        
        self.upload_label = tk.Label(container, text="Upload Your Resume", 
                                   font=("Arial", 18, "bold"), bg="#000000", fg="#ffffff")
        self.upload_label.pack(pady=10)
        
        self.upload_button = tk.Button(container, text="Select File", command=self.upload_file,
                                     font=("Arial", 14, "bold"), bg="#ffffff", fg="#000000",
                                     padx=20, pady=10, relief="flat", bd=0, width=20)
        self.upload_button.pack(pady=10)
        
        self.file_name_label = tk.Label(container, text="No file selected", 
                                      font=("Arial", 12), bg="#000000", fg="#ffffff")
        self.file_name_label.pack(pady=5)

    def upload_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), 
                                                         ("PDF files", "*.pdf"), 
                                                         ("Word files", "*.docx")])
        if file_path:
            file_name = file_path.split("/")[-1]
            self.file_name_label.config(text=file_name)
            
            self.clear_screen()
            
            container = tk.Frame(self.root, bg="#000000")
            container.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
            
            self.uploading_label = tk.Label(container, text="Uploading...", 
                                           font=("Arial", 14), bg="#000000", fg="#ffffff")
            self.uploading_label.pack()
            
            self.progress = ttk.Progressbar(container, orient=tk.HORIZONTAL, length=300,
                                           mode='determinate', style="TProgressbar")
            self.progress.pack(pady=20)
            
            self.root.after(500, self.animate_progress, lambda: self.process_resume(file_path))

    def process_resume(self, file_path):
        resume_text = self.extractor.return_resume_text(file_path)
        if resume_text:
            skills = self.extractor.extract_skills(resume_text)
            self.show_skills_page(skills)
        else:
            self.show_skills_page("Error reading the file.")

    def show_skills_page(self, skills):
        self.clear_screen()
        
        container = tk.Frame(self.root, bg="#000000")
        container.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        self.skills_label = tk.Label(container, text="Extracted Hard Skills", 
                                   font=("Arial", 18, "bold"), bg="#000000", fg="#ffffff")
        self.skills_label.pack(pady=20)
        
        self.skill_var = tk.StringVar()
        self.skill_dropdown = ttk.Combobox(container, textvariable=self.skill_var)
        self.skill_dropdown.pack(pady=10)
        
        self.load_skills_to_dropdown(skills)
        
        self.find_jobs_button = tk.Button(container, text="Find Jobs", command=self.find_jobs,
                                        font=("Arial", 14, "bold"), bg="#ffffff", fg="#000000",
                                        padx=20, pady=10, relief="flat", bd=0, width=20)
        self.find_jobs_button.pack(pady=20)

    def load_skills_to_dropdown(self, skills):
        self.skill_dropdown['values'] = skills
        if skills:
            self.skill_var.set(skills[0])

    def find_jobs(self):
        selected_skill = self.skill_var.get()
        if selected_skill:
            self.find_jobs_button.config(state=tk.DISABLED)
            self.show_loading_animation()
            
            threading.Thread(target=self.fetch_jobs_in_thread, args=(selected_skill,)).start()
        else:
            messagebox.showwarning("Warning", "Please select a skill first.")

    def fetch_jobs_in_thread(self, skill):
        try:
            ranked_jobs = self.fetch_jobs(skill)
            if ranked_jobs:
                self.root.after(0, lambda: self.show_ranked_jobs(ranked_jobs))
            else:
                self.root.after(0, lambda: messagebox.showwarning("Warning", "No jobs found."))
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Error", str(e)))
        finally:
            self.root.after(0, self.hide_loading_animation)
            self.root.after(0, lambda: self.find_jobs_button.config(state=tk.NORMAL))

    def fetch_jobs(self, skill):
        url = "https://jsearch.p.rapidapi.com/search"
        headers = {
            "X-RapidAPI-Key": "00b228b72emsh344f58e23be4ad6p17fa88jsn00ff2fd078e3",
            "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
        }
        
        querystring = {"query": skill, "page": "1", "num_pages": "10", "country": "us"}
        
        response = requests.get(url, headers=headers, params=querystring)
        if response.status_code == 200:
            data = response.json()
            if data.get('data'):
                jobs = data['data']
                
                with open('jobs.csv', 'w', newline='', encoding='utf-8') as csvfile:
                    fieldnames = ['Title', 'Company', 'Location', 'Posted', 
                                 'Apply_URL', 'Description', 'Salary', 'Job_Type']
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writeheader()
                    for job in jobs:
                        writer.writerow({
                            'Title': job.get('job_title', 'N/A'),
                            'Company': job.get('employer_name', 'N/A'),
                            'Location': f"{job.get('job_city', '')} {job.get('job_country', '')}".strip(),
                            'Posted': job.get('job_posted_at_datetime_utc', 'N/A'),
                            'Apply_URL': job.get('job_apply_link', 'N/A'),
                            'Description': job.get('job_description', ''),
                            'Salary': job.get('job_salary', 'N/A'),
                            'Job_Type': job.get('job_employment_type', 'N/A')
                        })
                
                ranked_jobs = self.analyze_and_rank_jobs('jobs.csv', 'skills.csv')
                return ranked_jobs
        return None

    def analyze_and_rank_jobs(self, jobs_csv, skills_csv):
        ranked_jobs = []
        
        with open(skills_csv, 'r', encoding='utf-8') as skills_file:
            skills_reader = csv.reader(skills_file)
            next(skills_reader)
            hard_skills = [row[0] for row in skills_reader]
        
        with open(jobs_csv, 'r', encoding='utf-8') as jobs_file:
            jobs_reader = csv.DictReader(jobs_file)
            for job in jobs_reader:
                description = job['Description']
                match_score = sum(1 for skill in hard_skills if skill.lower() in description.lower())
                ranked_jobs.append({**job, 'Match_Score': match_score})
        
        ranked_jobs.sort(key=lambda x: x['Match_Score'], reverse=True)
        return ranked_jobs

    def show_ranked_jobs(self, ranked_jobs):
        self.clear_screen()
        
        # Main container
        main_frame = tk.Frame(self.root, bg="#000000")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Canvas and Scrollbar setup
        canvas_container = tk.Frame(main_frame, bg="#000000")
        canvas_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        canvas = tk.Canvas(canvas_container, bg="#000000", highlightthickness=0)
        scrollbar = ttk.Scrollbar(canvas_container, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#000000")

        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        # Add job cards to scrollable frame
        for job in ranked_jobs:
            card = tk.Frame(scrollable_frame, bg="#1e1e1e", padx=20, pady=20, 
                           relief=tk.RAISED, bd=2)
            card.pack(fill=tk.X, pady=10, padx=10)
            
            company_label = tk.Label(card, text=job["Company"], 
                                   font=("Arial", 16, "bold"), bg="#1e1e1e", fg="#ffffff")
            company_label.pack(anchor="w", pady=(0, 5))
            
            title_label = tk.Label(card, text=job["Title"], 
                                 font=("Arial", 14), bg="#1e1e1e", fg="#ffffff")
            title_label.pack(anchor="w", pady=(0, 5))
            
            '''match_label = tk.Label(card, text=f"Match Score: {job['Match_Score']}", 
                                 font=("Arial", 12), bg="#1e1e1e", fg="#ffffff")
            match_label.pack(anchor="w", pady=(0, 10))'''
            
            apply_button = tk.Button(card, text="Apply Now", 
                                   font=("Arial", 12, "bold"), bg="#ffffff", fg="#000000",
                                   command=lambda link=job["Apply_URL"]: webbrowser.open(link))
            apply_button.pack(anchor="e")

        # Exit button at bottom
        exit_frame = tk.Frame(main_frame, bg="#000000")
        exit_frame.pack(side="bottom", fill=tk.X, pady=20)
        
        exit_button = tk.Button(exit_frame, text="Exit Program", command=self.root.destroy,
                              font=("Arial", 14, "bold"), bg="#ff4444", fg="#ffffff",
                              padx=20, pady=10, width=15)
        exit_button.pack()

    def show_loading_animation(self):
                self.loading_container = tk.Frame(self.root, bg="#000000")
                self.loading_container.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
                
                self.loading_label = tk.Label(self.loading_container, text="Finding Jobs...", 
                                            font=("Arial", 14), bg="#000000", fg="#ffffff")
                self.loading_label.pack()
                
                self.progress = ttk.Progressbar(self.loading_container, orient=tk.HORIZONTAL,
                                            length=300, mode='indeterminate', style="TProgressbar")
                self.progress.pack(pady=20)
                self.progress.start()

    def hide_loading_animation(self):
                if hasattr(self, 'loading_container'):
                    self.loading_container.destroy()
                self.progress.stop()

    def clear_screen(self):
                for widget in self.root.winfo_children():
                    widget.destroy()

if __name__ == "__main__":
            root = tk.Tk()
            style = ttk.Style()
            style.configure("TProgressbar", troughcolor="#000000", 
                        background="#ffffff", thickness=10, bordercolor="#000000")
            app = JobMatchingApp(root)
            root.mainloop()