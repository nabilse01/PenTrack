import pandas as pd
import random
import faker

def generate_name():
    """Generates a list of 5000 North American names."""
    fake = faker.Faker()
    return [fake.first_name() + " " + fake.last_name() for _ in range(250)]

data = [
    (name, random.randint(100000000, 999999999), name.split()[0].lower() + "_" + name.split()[1].lower() + "@gmail.com")
    for name in generate_name()
]

df = pd.DataFrame(data, columns=["PersonName", "PersonID", "Email"])
df.to_csv("people_data3.csv", index=False)
