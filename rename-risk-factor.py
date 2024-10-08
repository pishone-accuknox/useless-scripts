def convert_risk_factors(file_path):
    with open(file_path, 'r') as file:
        content = file.read()

    import re
    content = re.sub(r'<risk_factor>(.*?)</risk_factor>', lambda m: f'<risk_factor>{m.group(1).lower()}</risk_factor>', content)

    with open('modified_' + file_path, 'w') as file:
        file.write(content)

convert_risk_factors('nessus-NS-1728372816.3800337.nessus')

