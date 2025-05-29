import json
import pandas as pd
from datetime import datetime
from pymongo import MongoClient
from bson.objectid import ObjectId
from helper_functions import add_documents

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")

# Create or switch to a database
db = client["school"]

# Create or switch to a collection
collection = db["students"]
add_to_collection = False
number_to_add = 1000 if add_to_collection else 0

if add_to_collection or (not collection.count_documents({})):
    add_documents(collection, number_to_add)

# Get document schema using aggregation
schema = list(
    collection.aggregate(
        [
            {"$sample": {"size": 1}},  # Get a sample document
            {"$project": {"fields": {"$objectToArray": "$$ROOT"}}},
            {
                "$project": {
                    "fields": {
                        "$map": {
                            "input": "$fields",
                            "as": "field",
                            "in": {"name": "$$field.k", "type": {"$type": "$$field.v"}},
                        }
                    }
                }
            },
        ]
    )
)

# Counting docs in the collection with criteria
dob_cnt_btw_dates = collection.count_documents(
    {
        "date_of_birth": {
            "$gte": datetime(2003, 1, 1).strftime(r"%Y-%m-%d"),
            "$lte": datetime(2007, 12, 31).strftime(r"%Y-%m-%d"),
        }
    }
)

# Perform aggregation: average GPA of students born between 2003 and 2007 by department
avg_by_dept = list(
    collection.aggregate(
        [
            {
                "$match": {
                    "date_of_birth": {
                        "$gte": datetime(2003, 1, 1).strftime(r"%Y-%m-%d"),
                        "$lte": datetime(2007, 12, 31).strftime(r"%Y-%m-%d"),
                    }
                }
            },
            {"$group": {"_id": "$department", "avgGPA": {"$avg": "$gpa"}}},
        ]
    )
)

# Updating a document - use update_many for multiple updates
record = list(
    collection.find(
        {"_id": ObjectId("68332eb9da0b77ec6b8d1476")},
        {"_id": False, "first_name": True, "department": True},
    )
)  # Check existing records and excluding _id from output
print(
    f"Department of {record[0]['first_name']} in record:",
    record[0]["department"] if record else "Not found",
)

# Change the department in record to 'Finance'. (Use unset to remove a field)
collection.update_one({"first_name": "Jennifer"}, {"$set": {"department": "Finance"}})
record = list(collection.find({"first_name": "Jennifer"}, {"_id": False}))
print(
    f"New department of {record[0]['first_name']} in record",
    record[0]["department"] if record else "Not found",
)

# list of existing depts
unique_departments = collection.distinct("department")
print("Unique departments in the collection:", unique_departments)

# Using update_many
unset_reset = False
if unset_reset:
    collection.update_many(
        {"department": "Financial Services"}, {"$unset": {"department": ""}}
    )
    collection.update_many(
        {"department": {"$exists": False}},
        {"$set": {"department": "Financial Services"}},
    )
else:
    # Rename current 'Finance' department to 'Financial Services'
    collection.update_many(
        {"department": "Finance"}, {"$set": {"department": "Financial Services"}}
    )

# count documents with a specific department
count_financial_services = collection.count_documents({"department": "Business"})

# count of documents by department
count_by_department = list(
    collection.aggregate(
        [
            {
                "$group": {"_id": "$department", "count": {"$sum": 1}}
            },  # add one per document
            {"$sort": {"count": 1}},
        ]  # sort by count ascending. Use -1 for descending.
    )
)

# Export as JSON file
with open("students.json", "w") as f:
    # Convert ObjectId to string for JSON serialization
    json.dump(list(collection.find()), f, default=str, indent=4, ensure_ascii=False)
    # Clear the collection after export
    collection.delete_many({})

# Import from JSON file
with open("students.json", "r") as f:
    data = json.load(f)
    # Convert string _id back to ObjectId
    for document in data:
        if "_id" in document:
            document["_id"] = ObjectId(document["_id"])
    collection.insert_many(data)

# See sample output
tmp = list(
    collection.find(
        {}, {"_id": False, "first_name": True, "last_name": True, "email": True}
    ).limit(5)
)

# Export to csv, update email addresses, re-insert into collection
df = pd.DataFrame(list(collection.find()))
df.email = df.first_name.str.lower() + "." + df.last_name.str.lower() + "@uniofstn.edu"
collection.delete_many({})
collection.insert_many(df.to_dict(orient="records"))

# See sample output
tmp = list(
    collection.find(
        {}, {"_id": False, "first_name": True, "last_name": True, "email": True}
    ).limit(5)
)

# Comparison operators. See use of $gte, $lte above. Others are $ne, $in, $nin, $all
comp_oprs = list(
    collection.find(
        {
            "gpa": {"$gte": 3.5, "$lte": 4.0},
            "department": {
                "$nin": ["Engineering"]
            },  # or "department": {"$ne": "Engineering"},
            "courses": {"$all": ["Statistics", "Machine Learning"]},
            "address.state": {"$in": ["Alaska", "Indiana", "Washington"]},
        },
        {"_id": False, "first_name": True, "last_name": True, "gpa": True},
    )
)

# Example combining multiple logical operators
logical_oprs = list(
    collection.find(
        {
            "$and": [
                # Must be either CS or Engineering
                {
                    "$or": [
                        {"department": "Computer Science"},
                        {"department": "Engineering"},
                    ]
                },
                # Must have good GPA and specific courses
                {"gpa": {"$gte": 3.5}},
                {"courses": {"$all": ["Programming", "Database Systems"]}},
                # Must not be from these states
                {"$nor": [{"address.state": "Alaska"}, {"address.state": "Hawaii"}]},
            ]
        },
        {
            "_id": False,
            "first_name": True,
            "last_name": True,
            "department": True,
            "gpa": True,
        },
    )
)

print()
