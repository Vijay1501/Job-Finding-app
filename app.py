import csv
from datetime import datetime

def display_results():
    """Display ranked jobs with proper sorting"""
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    END = "\033[0m"
    
    try:
        with open('jobsRanked.csv', 'r') as f:
            jobs = list(csv.DictReader(f))
            
        print(f"\n{GREEN}=== MATCHING JOBS ({len(jobs)} FOUND) ===")
        
        for idx, job in enumerate(jobs, 1):
            try:
                due_date = datetime.strptime(job['Due Date'], '%Y-%m-%d')
                days_left = (due_date - datetime.now()).days
                date_color = GREEN if days_left >= 30 else YELLOW if days_left >=7 else RED
                
                print(f"\n{RED}#{idx}{END} {GREEN}{job['Position']}{END}")
                print(f"{YELLOW}Company:{END} {job['Company Name']}")
                print(f"{YELLOW}Match:{END} {job['Match Score']}")
                print(f"{YELLOW}Apply By:{END} {date_color}{job['Due Date']} ({days_left} days){END}")
                print(f"{YELLOW}Link:{END} {job['Link to Apply']}")
            except:
                continue
                
    except FileNotFoundError:
        print(f"{RED}Error: Run algorithm.py first to generate rankings{END}")

if __name__ == "__main__":
    display_results()