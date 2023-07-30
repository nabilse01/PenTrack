import csv
import random

tags = []
for i in range(1, 20001):
    tag_name = f" Minew Plus Tag {i}"
    mac_parts = [random.randint(0, 255) for _ in range(6)]  # Generate six random integers between 0 and 255
    mac_address = ":".join(f"{part:02X}" for part in mac_parts)  # Convert the integers to hexadecimal strings with leading zeros
    label = f"Label {i}"
    tags.append([tag_name, mac_address, label])

# Writing data to a CSV file
with open('tags_data.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Tag Name", "Mac Address", "Label"])  # Write headers
    writer.writerows(tags)  # Write rows of data
