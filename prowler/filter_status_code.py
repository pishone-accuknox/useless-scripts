# Script to extract list of findings and assets in separate files 

import json

with open('prowler-output.ocsf.json', 'r') as file:
    data = json.load(file)

status_counts = {"FAIL": 0, "MANUAL": 0, "PASS": 0}
all_findings = []
all_assets= set()

for finding in data:
    status_code = finding.get("status_code")
    if status_code in status_counts:
        status_counts[status_code] += 1
    
    finding_title = finding.get("finding_info", {}).get("title", "Unknown Finding")
    all_findings.append(finding_title)
    
    for resource in finding.get("resources", []):
        asset_name = resource.get("name", "Unknown Asset")
        all_assets.add(asset_name)
        
print("Status Code Counts:")
for status, count in status_counts.items():
    print(f"{status}: {count}")

with open('findings.txt', 'w') as findings_file:
    findings_file.write("\n".join(all_findings))
    
with open('assets.txt', 'w') as assets_file:
    assets_file.write("\n".join(all_assets))
