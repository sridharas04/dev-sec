import requests
import os
import json
from datetime import datetime

def create_engagement(defectdojo_url, defectdojo_api_key, product_id):
    url = f"{defectdojo_url}/api/v2/engagements/"
    headers = {
        'Authorization': f"Token {defectdojo_api_key}",
        'Content-Type': 'application/json'
    }
    data = {
        "product": product_id,
        "name": "CI/CD Engagement",
        "status": "In Progress",
        "target_start": "2024-01-01",
        "target_end": "2024-12-31"
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))
    response.raise_for_status()
    engagement = response.json()
    print(f"Engagement created with ID: {engagement['id']}")
    return engagement['id']

def import_scan_results(defectdojo_url, defectdojo_api_key, engagement_id, file_path, scan_type):
    url = f"{defectdojo_url}/api/v2/import-scan/"
    headers = {
        'Authorization': f"Token {defectdojo_api_key}"
    }
    data = {
        "scan_type": scan_type,
        "engagement": engagement_id,
        "verified": "true",
        "active": "true",
        "scan_date": datetime.now().strftime("%Y-%m-%d")
    }

    if file_path.endswith('.json'):
        content_type = 'application/json'
    elif file_path.endswith('.xml'):
        content_type = 'application/xml'
    elif file_path.endswith('.sarif'):
        content_type = 'application/sarif+json'
    else:
        raise ValueError("Unsupported file format")

    files = {
        'file': (file_path, open(file_path, 'rb'), content_type)
    }

    response = requests.post(url, headers=headers, data=data, files=files)
    
    if response.status_code != 200:
        print(f"Error importing scan results from {file_path}: {response.status_code} - {response.text}")
        response.raise_for_status()

    print(f"Scan results from {file_path} imported successfully as {scan_type} scan.")

if __name__ == "__main__":
    defectdojo_url = os.getenv('DEFECTDOJO_URL')
    defectdojo_api_key = os.getenv('DEFECTDOJO_API_KEY')
    product_id = int(os.getenv('DEFECTDOJO_PRODUCT_ID'))

    print(defectdojo_url,defectdojo_api_key,product_id)

    engagement_id = create_engagement(defectdojo_url, defectdojo_api_key, product_id)

    report_files = {
        'dastardly-report.xml': 'Burp Dastardly Scan',
        'gitleaks-report.sarif': 'Gitleaks Scan',
        'results-opensource.json': 'Snyk Scan',
        'results-code.json': 'Snyk Code Scan',
        'results-container.json': 'Snyk Scan',
        'results-iac.json': 'Snyk Scan'
    }

    for file_path, scan_type in report_files.items():
        if os.path.exists(file_path):
            import_scan_results(defectdojo_url, defectdojo_api_key, engagement_id, file_path, scan_type)
        else:
            print(f"{file_path} not found. Skipping upload.")
