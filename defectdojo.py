import defectdojo_api
import os

defectdojo_url = os.getenv('DEFECTDOJO_URL')
api_key = os.getenv('DEFECTDOJO_API_KEY')
engagement_id = os.getenv('DEFECTDOJO_ENGAGEMENT_ID')

# Initialize the DefectDojo API client
api = defectdojo_api.DefectDojoAPI(defectdojo_url, api_key, verify_ssl=False)

# Upload the reports to DefectDojo
report_files = {
    'dastardly-report.xml': 'Dastardly Scan',
    'gitleaks-report.json': 'Gitleaks Secret Scan',
    'results-opensource.json': 'Snyk SCA',
    'results-code.json': 'Snyk SAST',
    'results-container.json': 'Snyk Container Scan',
    'results-iac.json': 'Snyk IaC'
}

for file_path, scan_type in report_files.items():
    if os.path.exists(file_path):
        print(f"Uploading {file_path} to DefectDojo as {scan_type} scan...")
        api.upload_scan(
            engagement_id,
            scan_type,
            file_path,
            active=True,
            verified=True
        )
        print(f"{file_path} uploaded successfully.")
    else:
        print(f"{file_path} not found. Skipping upload.")
