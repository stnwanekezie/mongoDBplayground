# MongoDB with PyMongo Tutorial

## 📘 Overview

This project demonstrates comprehensive MongoDB operations using PyMongo, including:

- CRUD operations  
- Aggregation pipelines  
- Data manipulation with `pandas` integration  

---

## 🛠 Prerequisites

- Python 3.8+
- MongoDB Community Server
- Visual Studio Code
- Git (optional)

---

## ⚙️ Setup Instructions

### 1. Install MongoDB Community Server

- Download from [MongoDB Download Center](https://www.mongodb.com/try/download/community)
- During installation:
  - Choose **Complete** installation
  - Install **MongoDB Compass** (GUI tool)
  - Check **Install MongoDB as a Service**

### 2. Download and add `mongosh` to System Variables (Windows)

1. Download the zip file from [MongoDB Download Center](https://www.mongodb.com/try/download/shell)
2. Extract the zip file contents to ```C:\Program Files\MongoDB```
3. Open **System Properties**
4. Go to **Environment Variables**
5. Under **System Variables**, select `Path` → Click **Edit** → **New**
6. Add path to PATH:  
   ```
   C:\Program Files\MongoDB\mongosh-<version>-win32-x64\bin
   ```
7. Click **OK** to save

### 3. Install VS Code Extensions

- Open VS Code
- Go to Extensions and Install MongoDB for VS Code
While this repo focuses on using pymongo, you may use the MongoDB shell (mongosh) instead. To do this,
1. Click on the MongoDB icon that is added to the explorer ribbon after MongoDB for VS Code installation, add a database and start a connection.
2. In a VS Code terminal, run
   ```bash
   mongosh
   ```
   This should start the MongoDB shell which allows you access your databases.

### 4. Python Setup

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment (Windows)
.\venv\Scripts\activate

# Install dependencies
pip install pymongo pandas faker
```

---

## 📁 Project Structure

```
mongodb/
│
├── mongodb_with_python.py     # Main script
├── helper_functions.py        # Helper functions for data generation
├── students.json              # Data export/import file
└── README.md                  # Project documentation
```

---

## ✅ Features Demonstrated

### MongoDB Basics
- Connection setup
- Document insertion, querying, updating, deletion

### Advanced Operations
- Aggregation pipelines
- Schema analysis
- Data export/import with `JSON`
- Integration with `pandas` for analysis

### Query Operators
- **Comparison**: `$gte`, `$lte`, `$in`, `$nin`
- **Logical**: `$exists`, `$and`, `$not`, `$or`
- **Array**: `$all`
- **Element**: `$type`

---

## ▶️ Usage

### Start MongoDB service (Windows)
Open Windows Powershell or CMD (as administrator) and run
```bash
net start MongoDB
```
Otherwise, click on the start icon and open Services. From the list of local services, identify MongoDB Server (MongoDB), right click and select start.

### Debug the script

```bash
mongodb_with_python.py
```

---

## 🧪 Code Examples

Check `mongodb_with_python.py` for examples of:

- Basic CRUD operations
- Complex queries and projections
- Aggregation pipelines
- Data export/import
- `pandas`-based analysis

---

## 🧬 Data Model

```json
{
  "student_id": 12345,
  "first_name": "John",
  "last_name": "Doe",
  "email": "john.doe@example.com",
  "department": "Computer Science",
  "gpa": 3.75,
  "courses": ["Math", "CS101", "Physics"],
  "address": {
    "street": "123 Main St",
    "city": "Sampleville",
    "state": "CA",
    "zip_code": "90210"
  }
}
```

---

## 🤝 Contributing

1. Fork the repository  
2. Create your feature branch  
3. Commit your changes  
4. Push to your branch  
5. Open a Pull Request

---

## 📄 License

This project is licensed under the **MIT License**.

---

## 🧯 Troubleshooting

- Ensure MongoDB service is running
- Verify the MongoDB connection string
- Check if `mongosh` is added to system `PATH`
- Confirm that PyMongo is installed correctly

---

## 📚 Additional Resources

- 🎥 [Learn MongoDB in 1 Hour (YouTube)](https://www.youtube.com/watch?v=c2M-rlkkT5o)  
- 📘 [PyMongo Documentation](https://pymongo.readthedocs.io/)  
- 🌐 [MongoDB Documentation](https://www.mongodb.com/docs/)  
- 🎓 [MongoDB University](https://university.mongodb.com/)
