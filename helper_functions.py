import random
import pymongo
from faker import Faker

fake = Faker()


def add_documents(
    collection: pymongo.synchronous.collection.Collection, number: float
) -> None:
    """
    Add a document to the MongoDB collection.
    """
    students = []
    departments = [
        "Computer Science",
        "Engineering",
        "Mathematics",
        "Physics",
        "Business",
    ]
    grade_levels = ["Freshman", "Sophomore", "Junior", "Senior"]
    for _ in range(number):
        student = {
            "student_id": fake.unique.random_number(digits=8),
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "email": fake.email(),
            "department": random.choice(departments),
            "grade_level": random.choice(grade_levels),
            "gpa": round(random.uniform(2.0, 4.0), 2),
            "date_of_birth": fake.date_of_birth(
                minimum_age=18, maximum_age=25
            ).strftime("%Y-%m-%d"),
            "address": {
                "street": fake.street_address(),
                "city": fake.city(),
                "state": fake.state(),
                "zip_code": fake.zipcode(),
            },
            "courses": random.sample(
                [
                    "Calculus",
                    "Physics",
                    "Programming",
                    "Database Systems",
                    "Data Structures",
                    "Statistics",
                    "Machine Learning",
                    "Web Development",
                ],
                k=random.randint(3, 6),
            ),
            "enrolled_date": fake.date_between(
                start_date="-4y", end_date="today"
            ).strftime("%Y-%m-%d"),
            "is_active": random.choice([True, False]),
            "phone_number": fake.phone_number(),
        }
        students.append(student)

    result = collection.insert_many(students)
    print(f"Inserted {len(result.inserted_ids)} documents")
