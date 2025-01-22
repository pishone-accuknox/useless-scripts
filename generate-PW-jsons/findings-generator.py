import json
import random
from datetime import datetime, timedelta
import uuid
from tqdm import tqdm

def generate_random_text(length=10):
    return ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ', k=length))

def generate_unmapped():
    frameworks = ["CIS", "NIST", "ISO", "SOC", "HIPAA", "PCI", "GDPR", "AWS"]
    sections = [str(random.randint(1, 20)) + "." + str(random.randint(1, 10)) for _ in range(3)]
    
    compliance = {}
    for _ in range(random.randint(3, 8)):
        framework = random.choice(frameworks) + "-" + str(random.randint(1, 5))
        compliance[framework] = [f"{random.randint(1, 10)}.{random.randint(1, 10)}" for _ in range(random.randint(2, 5))]
    
    return {
        "related_url": f"https://{generate_random_text()}.com/{generate_random_text()}" if random.choice([True, False]) else "",
        "categories": [],
        "depends_on": [],
        "related_to": [],
        "notes": "",
        "compliance": compliance
    }

def generate_resource():
    services = ["iam", "s3", "ec2", "rds", "lambda", "cloudwatch", "sns", "sqs"]
    regions = ["us-east-1", "us-east-2", "us-west-1", "us-west-2", "eu-west-1", "ap-south-1"]
    
    service = random.choice(services)
    region = random.choice(regions)
    resource_id = f"{service}-{uuid.uuid4().hex[:8]}"
    
    return {
        "cloud_partition": "aws",
        "region": region,
        "data": {"details": ""},
        "group": {"name": service},
        "labels": [],
        "name": resource_id,
        "type": "Other",
        "uid": f"arn:aws:{service}:{region}:{random.randint(100000000000, 999999999999)}:{resource_id}"
    }

def generate_finding(resource, account_id):
    current_time = int(datetime.now().timestamp())
    current_time_dt = datetime.now().isoformat()
    
    finding_title = f"Check if {generate_random_text(20)}"
    event_code = f"{generate_random_text(10)}_{generate_random_text(5)}"
    
    return {
        "message": f"{generate_random_text(30)}",
        "metadata": {
            "event_code": event_code,
            "product": {
                "name": "Prowler",
                "uid": "prowler",
                "vendor_name": "Prowler",
                "version": "5.0.0"
            },
            "profiles": ["cloud", "datetime"],
            "tenant_uid": "",
            "version": "1.3.0"
        },
        "severity_id": random.randint(1, 4),
        "severity": random.choice(["Critical", "High", "Medium", "Low"]),
        "status": random.choice(["New", "In Progress", "Resolved"]),
        "status_code": random.choice(["FAIL", "PASS", "MANUAL"]),
        "status_detail": generate_random_text(50),
        "status_id": random.randint(1, 5),
        "unmapped": generate_unmapped(),
        "activity_name": "Create",
        "activity_id": random.randint(1, 100),
        "finding_info": {
            "created_time": current_time,
            "created_time_dt": current_time_dt,
            "desc": finding_title,
            "product_uid": "prowler",
            "title": finding_title,
            "types": [random.choice(["IAM", "Network", "Storage", "Compute", "Database"])],
            "uid": f"prowler-aws-{event_code}-{uuid.uuid4().hex}"
        },
        "resources": [resource],
        "category_name": "Findings",
        "category_uid": random.randint(1, 10),
        "class_name": "Detection Finding",
        "class_uid": random.randint(2000, 3000),
        "cloud": {
            "account": {
                "name": "",
                "type": "AWS Account",
                "type_id": 10,
                "uid": str(account_id),
                "labels": []
            },
            "org": {
                "name": "",
                "uid": ""
            },
            "provider": "aws",
            "region": resource["region"]
        },
        "remediation": {
            "desc": generate_random_text(100),
            "references": [
                f"aws {generate_random_text(10)} --{generate_random_text(8)} {generate_random_text(12)}",
                f"https://{generate_random_text()}.com/{generate_random_text()}"
            ]
        },
        "risk_details": generate_random_text(200),
        "time": current_time,
        "time_dt": current_time_dt,
        "type_uid": random.randint(200000, 300000),
        "type_name": f"Detection Finding: {generate_random_text(10)}"
    }

def generate_account_findings(account_id, num_assets, findings_per_asset):
    findings = []
    
    for _ in tqdm(range(num_assets), desc=f"Generating findings for account {account_id}"):
        resource = generate_resource()
        for _ in range(findings_per_asset):
            finding = generate_finding(resource, account_id)
            findings.append(finding)
    
    return findings

def main(num_files=3, assets_per_file=80000, findings_per_asset=3):
    account_ids = [str(random.randint(100000000000, 999999999999)) for _ in range(num_files)]
    
    print(f"Generating {num_files} files with {assets_per_file} assets each")
    print(f"Each asset will have {findings_per_asset} findings")
    
    for account_id in account_ids:
        findings = generate_account_findings(account_id, assets_per_file, findings_per_asset)
        filename = f"prowler-output-{account_id}.ocsf.json"
        
        print(f"\nWriting {len(findings)} findings to {filename}")
        with open(filename, 'w') as f:
            json.dump(findings, f, indent=2)

if __name__ == "__main__":

    main(num_files=2, assets_per_file=10000, findings_per_asset=1)
