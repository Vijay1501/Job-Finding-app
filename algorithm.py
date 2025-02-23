import csv
from datetime import datetime

def read_skills(filename='tech_skills.csv'):
    """Read skills from CSV file"""
    with open(filename, 'r') as f:
        return [skill.strip().lower() for row in csv.reader(f) for skill in row if skill.strip()]

def read_jobs(filename='jobs.csv'):
    """Read jobs from CSV file"""
    with open(filename, 'r') as f:
        return list(csv.DictReader(f))

def calculate_scores(jobs, skills):
    """Calculate match scores with whole-word matching"""
    total_skills = len(skills)
    skill_set = set(skills)
    
    for job in jobs:
        job['_numeric_score'] = 0.0
        if total_skills == 0:
            continue
            
        # Create word boundaries for exact matching
        description = ' ' + job['Description'].lower().replace(',', ' ') + ' '
        matches = 0
        
        for skill in skill_set:
            if f' {skill} ' in description:
                matches += 1
                
        job['_numeric_score'] = matches / total_skills
        job['Match Score'] = f"{matches}/{total_skills} ({job['_numeric_score']:.0%})"
    
    return sorted(jobs, key=lambda x: x['_numeric_score'], reverse=True)

def display_results(ranked_jobs):
    """Display formatted results in terminal"""
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    CYAN = "\033[96m"
    END = "\033[0m"
    
    print(f"\n{CYAN}=== JOB MATCHING RESULTS ==={END}")
    
    for idx, job in enumerate(ranked_jobs, 1):
        try:
            # Date handling
            due_date = datetime.strptime(job['Due Date'], '%Y-%m-%d')
            days_left = (due_date - datetime.now()).days
            date_color = GREEN if days_left >= 30 else YELLOW if days_left >= 7 else RED
            
            # Print job details
            print(f"\n{RED}Rank #{idx}{END}")
            print(f"{GREEN}Position:{END} {job['Position']}")
            print(f"{YELLOW}Company:{END} {job['Company Name']}")
            print(f"{YELLOW}Match Score:{END} {job['Match Score']}")
            print(f"{YELLOW}Apply By:{END} {date_color}{job['Due Date']} ({days_left} days remaining){END}")
            print(f"{YELLOW}Description:{END} {job['Description'][:100]}...")
            print(f"{GREEN}Apply Here:{END} {job['Link to Apply']}")
            print("-" * 60)
        except Exception as e:
            print(f"{RED}Error displaying job #{idx}: {str(e)}{END}")
            continue

def main():
    skills = read_skills()
    jobs = read_jobs()
    
    if not skills:
        print("\033[91mError: No skills found in skills.csv\033[0m")
        return
    
    if not jobs:
        print("\033[91mError: No jobs found in jobs.csv\033[0m")
        return
    
    ranked_jobs = calculate_scores(jobs, skills)
    display_results(ranked_jobs)

if __name__ == "__main__":
    main()