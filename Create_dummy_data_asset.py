import csv
import random
import string

# Generate a random MAC address (eg: AA:BB:CC:DD:EE:11)
def generate_mac_address():
    mac = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(12))
    return ':'.join(mac[i:i+2] for i in range(0, 12, 2))

# Generate a random department
def generate_department():
    departments = ['R&D', 'Finance', 'HR', 'Sales', 'Marketing']
    return random.choice(departments)

# Generate a random asset type
def generate_asset_type():
    asset_types = ['Devices', 'Furniture', 'Software']
    return random.choice(asset_types)

# Generate a random asset status
def generate_asset_status():
    asset_statuses = ['Available', 'In Use', 'Out of Service']
    return random.choice(asset_statuses)

# Generate a CSV file with random asset data
def generate_asset_csv(file_path, num_assets):
    with open(file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        # Write header row
        writer.writerow(['Asset label', 'Serial Number', 'Tag Mac Address', 'Department', 'Type', 'Status'])
        
        # Generate random data for each asset
        for i in range(num_assets):
            asset_label = f"asset{i}"
            serial_number = ''.join(random.choices(string.ascii_uppercase + string.digits, k=7)) # Random upper-case letters and digits
            tag_mac_address = generate_mac_address()
            department = generate_department()
            asset_type = generate_asset_type()
            status = generate_asset_status()
            
            writer.writerow([asset_label, serial_number, tag_mac_address, department, asset_type, status])

# Generate the CSV file with 10,000 assets
generate_asset_csv('assets.csv', 10000)
