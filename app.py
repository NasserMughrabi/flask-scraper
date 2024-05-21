from flask import Flask, jsonify
import threading
from scraper import find_utah_jobs
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

jobs_data = {
    'jobs': [],
    'updated': False
}

def update_jobs():
    jobs_data['jobs'] = find_utah_jobs()
    jobs_data['updated'] = True

@app.route('/start-job-search', methods=['GET'])
def start_job_search():
    if not jobs_data['updated']:
        thread = threading.Thread(target=update_jobs)
        thread.start()
        thread.join()
    return jsonify(jobs_data['jobs']), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)
