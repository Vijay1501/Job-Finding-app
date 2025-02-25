# ResuMate - Your Resume’s Perfect Career Match  

## About the Project  

### Inspiration  
As students, we often found ourselves overwhelmed by the sheer number of job portals and the time-consuming process of searching for roles that truly matched our resumes. After hours of scrolling through listings, we’d often feel too exhausted to even apply. This frustration inspired us to create **ResuMate**, a tool that automates the job search process, making it faster, smarter, and less tiring.  

### What It Does  
ResuMate is an AI-powered desktop app that:  
1. **Analyzes Resumes**: Extracts hard skills from uploaded resumes using OpenAI.  
2. **Fetches Jobs**: Pulls real-time job listings from top portals using the JSearch API.  
3. **Ranks Opportunities**: Matches and ranks jobs based on skill relevance, helping users find the best-fit roles quickly.  
4. **Simplifies Applications**: Displays ranked jobs with direct links to apply, saving users time and effort.  

### How We Built It  
We built ResuMate using:  
- **Tkinter**: For the user-friendly GUI.  
- **OpenAI API**: To extract hard skills from resumes.  
- **JSearch API**: To fetch real-time job listings.  
- **CSV Files**: For temporary storage of skills and job data.  
- **Threading**: To handle API calls without freezing the interface.  

The app follows a simple workflow:  
1. Users upload their resume.  
2. The app extracts hard skills using AI.  
3. It matches and ranks jobs, displaying the best opportunities in a clean, scrollable interface.  

### Challenges We Ran Into  
- **API Key Security**: Initially, we hardcoded API keys, which posed a security risk. We learned to use environment variables for safer key management.  
- **Threading Issues**: Direct GUI updates from threads caused crashes. We resolved this by using `root.after()` for thread-safe updates.  
- **Data Matching**: Ranking jobs based on skill relevance required careful algorithm design and testing.  
- **File Conflicts**: Both `app.py` and `jobsapi.py` wrote to `jobs.csv`, leading to data corruption. We consolidated the logic into one file.  

### Accomplishments We’re Proud Of  
- Creating a **fully functional desktop app** that simplifies job hunting.  
- Successfully integrating **AI** and **APIs** to automate resume analysis and job matching.  
- Designing a **clean and intuitive UI** that enhances user experience.  
- Overcoming threading and data-matching challenges to deliver a seamless product.  

### What We Learned  
- How to integrate **AI** and **APIs** into a real-world application.  
- The importance of **threading** for responsive GUI applications.  
- The challenges of **data matching** and ranking algorithms.  
- The value of **error handling** and **secure key management** in software development.  

### What’s Next for ResuMate  
- **Expand Job Sources**: Integrate more job portals for broader opportunities.  
- **Add Skill Development Tips**: Suggest courses or resources to bridge skill gaps.  
- **Mobile App Version**: Develop a mobile-friendly version for on-the-go job hunting.  
- **Enhanced AI**: Improve skill extraction accuracy with advanced NLP models.  
- **User Accounts**: Allow users to save profiles and track application progress.  

---

## How to Run the Project  
1. Clone the repository:  
   ```bash  
   git clone https://github.com/Vijay1501/Job-Finding-app

2. Install dependencies:
   pip install -r requirements.txt
  
3. Set up API keys:
  Create a .env file in the project root.
  Add your OpenAI and JSearch API keys:
      OPENAI_API_KEY=your_openai_key  
      JSEARCH_API_KEY=your_jsearch_key  
   
4. Run the app:
     python app.py


🧩 Challenges We Faced

API Key Security: Transitioned from hardcoded keys to environment variables.
Threading Issues: Fixed GUI freezes with root.after() for thread-safe updates.
Data Matching: Developed a custom algorithm for skill-based job ranking.
File Conflicts: Consolidated logic to avoid CSV corruption.


🏆 Accomplishments

Built a fully functional desktop app to simplify job hunting.
Integrated AI and APIs for automated resume analysis and job matching.
Designed an intuitive UI with Tkinter.
Overcame threading and data-matching challenges.

📚 What We Learned

Integrating AI/APIs into real-world apps.
Importance of threading for responsive GUIs.
Challenges of data matching and ranking algorithms.
Secure key management and error handling.


🔜 Future Roadmap

Expand Job Sources: Integrate LinkedIn, Indeed, etc.
Skill Development Tips: Suggest courses to bridge skill gaps.
Mobile App: Develop a cross-platform version.
Enhanced AI: Use NLP for better skill extraction.
User Accounts: Track application progress.


👥 Contributors

Aditya Pawar
Om Lala
Vijaysimha Naidu
Phanindra Vadali












   
