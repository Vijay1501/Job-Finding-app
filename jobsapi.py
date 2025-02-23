import requests
import csv

url = "https://jsearch.p.rapidapi.com/search"
headers = {
    "X-RapidAPI-Key": "00b228b72emsh344f58e23be4ad6p17fa88jsn00ff2fd078e3",
    "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
}

# Initialize variables
total_jobs_needed = 2
jobs_collected = []
current_page = 1


while len(jobs_collected) < total_jobs_needed:
    querystring = {
        "query": "software",
        "page": str(current_page),
        "num_pages": "10",  # Fetch 10 pages per request (API maximum may vary)
        "country": "us"
    }
    
    response = requests.get(url, headers=headers, params=querystring)
    
    if response.status_code == 200:
        data = response.json()
        if data.get('data'):
            jobs_collected.extend(data['data'])
            print(f"Collected {len(data['data'])} jobs from page {current_page}")
            current_page += 1
        else:
            print("No more jobs available")
            break
    else:
        print(f"Error: {response.status_code}")
        break

    # Prevent infinite loop safety check
    if current_page > 20:  # Max 20 pages * 10 per page = 200 jobs max attempt
        break

# Save to CSV
if jobs_collected:
    with open('jobs.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = [
            'Title', 'Company', 'Location', 'Posted', 
            'Apply_URL', 'Description', 'Salary', 'Job_Type'
        ]
        
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for job in jobs_collected[:total_jobs_needed]:  # Ensure exactly 100 jobs
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
    
    print(f"\nSuccessfully saved {len(jobs_collected[:total_jobs_needed])} jobs to jobs.csv")
else:
    print("No jobs to save")