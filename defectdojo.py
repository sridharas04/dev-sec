import os
from defectdojo_api import defectdojo

# DefectDojo connection parameters
DEFECTDOJO_URL = os.getenv('DEFECTDOJO_URL')
DEFECTDOJO_API_KEY = os.getenv('DEFECTDOJO_API_KEY')
ENGAGEMENT_ID = os.getenv('DEFECTDOJO_ENGAGEMENT_ID')

# Connect to DefectDojo
dojo = defectdojo.DefectDojoAPIv2(url=DEFECTDOJO_URL, api_token=DEFECTDOJO_API_KEY, verify_ssl=False)

# Upload reports
reports = [
    ('gitleaks', 'gitleaks-report.json', 'GitLeaks Scan'),
    ('snyk', 'results-opensource.json', 'Snyk Open Source Scan'),
    ('snyk', 'results-code.json', 'Snyk Code Scan'),
    ('snyk', 'results-container.json', 'Snyk Container Scan'),
    ('snyk', 'results-iac.json', 'Snyk IaC Scan'),
    ('burp', 'dastardly-report.xml', 'Dastardly DAST Scan')
]

for tool_type, file_path, title in reports:
    if os.path.exists(file_path):
        response = dojo.upload_scan(
            engagement_id=ENGAGEMENT_ID,
            scan_type=tool_type,
            file=file_path,
            scan_date=None,
            minimum_severity='Info',
            active=True,
            verified=False,
            close_old_findings=False,
            push_to_jira=False,
            environment=None,
            service=None,
            tags=None,
            close_old_findings_on_upload=False,
            title=title
        )
        if response.success:
            print(f'Successfully uploaded {title} report to DefectDojo.')
        else:
            print(f'Failed to upload {title} report to DefectDojo. Error: {response.message}')
