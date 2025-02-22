import openai
import tkinter as tk
from tkinter import filedialog, scrolledtext
import PyPDF2
import docx

class JobMatchingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Job Matching App")
        self.root.geometry("500x600")

        self.upload_button = tk.Button(root, text="Upload Resume", command=self.upload_file, font=("Arial", 14))
        self.upload_button.pack(pady=20)

        self.result_box = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=60, height=20, fg="white", bg="black")
        self.result_box.pack(pady=10)

        # Initialize Extractor
        self.extractor = Extractor()

    def upload_file(self):
        """Handles file upload and extracts skills."""
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("PDF files", "*.pdf"), ("Word files", "*.docx")])
        if file_path:
            resume_text = self.extractor.return_resume_text(file_path)
            if resume_text:
                print(f"Extracted Resume Text:\n{resume_text[:500]}...")  # ✅ Debugging
                skills = self.extractor.extract_skills(resume_text)  # ✅ Ensure this method exists
                self.result_box.delete("1.0", tk.END)
                self.result_box.insert(tk.END, skills)
            else:
                self.result_box.insert(tk.END, "Error reading the file.")

class Extractor:
    def __init__(self):
        """Initializes OpenAI API client with the API key."""
        self.api_key = self.get_api_key()
        if self.api_key:
            self.client = openai.OpenAI(api_key=self.api_key)  # ✅ Correct way to set API key
        else:
            self.client = None  # Prevents API calls if key is missing

    def get_api_key(self):
        """Fetches OpenAI API key from a file."""
        try:
            with open("api_key.txt", "r") as file:
                return file.read().strip()
        except Exception as e:
            print(f"Error reading API key file: {e}")
            return None

    def return_resume_text(self, file_path):
        """Extracts text from a resume file."""
        if file_path.endswith(".pdf"):
            return self.extract_pdf_text(file_path)
        elif file_path.endswith(".docx"):
            return self.extract_docx_text(file_path)
        elif file_path.endswith(".txt"):
            return self.extract_txt_text(file_path)
        else:
            return None

    def extract_pdf_text(self, file_path):
        """Extracts text from a PDF file."""
        try:
            text = ""
            with open(file_path, "rb") as pdf_file:
                reader = PyPDF2.PdfReader(pdf_file)
                for page in reader.pages:
                    extracted_text = page.extract_text()
                    if extracted_text:
                        text += extracted_text + "\n"
            return text if text else None
        except Exception as e:
            print(f"Error extracting text from PDF: {e}")
            return None

    def extract_docx_text(self, file_path):
        """Extracts text from a DOCX file."""
        try:
            doc = docx.Document(file_path)
            return "\n".join([para.text for para in doc.paragraphs]) or None
        except Exception as e:
            print(f"Error extracting text from DOCX: {e}")
            return None

    def extract_txt_text(self, file_path):
        """Reads text from a TXT file."""
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                return file.read()
        except Exception as e:
            print(f"Error reading TXT file: {e}")
            return None

    def extract_skills(self, resume_text):
        """Sends resume text to OpenAI API to extract hard and soft skills."""
        if not self.client:
            return "API key missing or invalid."

        prompt = f"""
        Extract key hard skills (technical skills) and soft skills (interpersonal skills) from the following resume.
        Format the response as follows:

        Hard Skills:
        - Skill 1
        - Skill 2
        - Skill 3

        Soft Skills:
        - Skill 1
        - Skill 2
        - Skill 3

        Resume Text:
        {resume_text}
        """

        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}]
            )
            print(f"OpenAI Response:\n{response}")  # ✅ Debugging
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error calling OpenAI API: {e}")
            return f"Error calling OpenAI API: {e}"

# Run the Tkinter app
if __name__ == "__main__":
    root = tk.Tk()
    app = JobMatchingApp(root)
    root.mainloop()
