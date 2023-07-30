import csv

# Read data from the existing CSV file
with open('People-Tag_3.csv', 'r') as file:
    reader = csv.DictReader(file)
    people_data = list(reader)

# Create a dictionary to store department IDs
department_ids = {}

# Generate unique department IDs for each department
for person in people_data:
    department = person['Department']
    if department not in department_ids:
        department_id = len(department_ids) + 1  # Generate a unique ID
        department_ids[department] = department_id
    person['DepartmentID'] = department_ids[department]

# Write the updated data to a new CSV file
fieldnames = ['PersonName', 'PersonID', 'Email', 'Department', 'DepartmentID']
with open('people_with_department_id.csv', 'w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(people_data)
