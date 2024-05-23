from flask import Flask, jsonify
import threading
from scraper import find_utah_jobs, find_linkedin_jobs
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

jobs_data = {
    'utahJobs': [],
    'linkedinJobs': [],
    'utahJobsUpdated': False,
    'linkedinJobsUpdated': False
}

def update_utah_jobs():
    try:
        jobs_data['utahJobs'] = find_utah_jobs()
        jobs_data['utahJobsUpdated'] = True
    except Exception as e:
        jobs_data['utahJobs'] = []
        jobs_data['utahJobsUpdated'] = False
        print(f"Error updating jobs: {e}")

def update_linkedin_jobs():
    try:
        jobs_data['linkedinJobs'] = find_linkedin_jobs()
        jobs_data['linkedinJobsUpdated'] = True
    except Exception as e:
        jobs_data['linkedinJobs'] = []
        jobs_data['linkedinJobsUpdated'] = False
        print(f"Error updating jobs: {e}")

@app.route('/search-utah-jobs', methods=['GET'])
def search_utah_jobs():
    if not jobs_data['utahJobsUpdated']:
        thread = threading.Thread(target=update_utah_jobs)
        thread.start()
        thread.join()
    return jsonify(jobs_data['utahJobs']), 200

@app.route('/search-linkedin-jobs', methods=['GET'])
def search_linkedin_jobs():
    if not jobs_data['linkedinJobsUpdated']:
        thread = threading.Thread(target=update_linkedin_jobs)
        thread.start()
        thread.join()
    return jsonify(jobs_data['linkedinJobs']), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)
