# MySQL Database Management Web Application

This Flask web application allows users to interact with a MySQL database through a user-friendly interface. Users can perform various database management tasks such as listing databases, viewing tables, and performing CRUD (Create, Read, Update, Delete) operations on table data.

## Features

- **Login to MySQL Server**: Users can log in to a MySQL server using their username and password.
- **View Databases**: Lists all databases available in the connected MySQL server.
- **View Tables**: Displays all tables within a selected database.
- **CRUD Operations**:
  - **View Data**: View all records from a selected table.
  - **Add Data**: Insert new rows into a table.
  - **Update Data**: Update existing rows in a table based on specific conditions.
  - **Delete Data**: Delete rows from a table based on specific conditions.

## Installation

### Prerequisites

- Python 3.x
- Flask
- MySQL server
- Required Python libraries: `mysql-connector-python`, `Flask`

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/PowerX-NOT/DBMS_WebApplication.git
   cd DBMS_WebApplication

### Install dependencies:

```bash
pip install -r requirements.txt
```

Ensure your MySQL server is running locally.

### Run the application:

```bash
python app.py
```

Open your web browser and navigate to:

```
http://127.0.0.1:5000/
```

## How It Works

1. **Login Page**  
   Users start by entering their MySQL username and password. If the credentials are valid, the application retrieves and displays all available databases.

2. **Database Selection**  
   Once logged in, users can select a database to view its tables.

3. **Table Actions**  
   After selecting a table, users can:
   - **View Data**: Fetch and display all records in the table.
   - **Add Data**: Insert new rows by filling out a form dynamically generated from the table's structure.
   - **Update Data**: Modify existing rows by specifying the column, new value, and a condition for the update.
   - **Delete Data**: Remove rows by specifying a condition for deletion.

4. **Error Handling**  
   If any error occurs (e.g., invalid credentials, incorrect SQL queries), the application displays a friendly error message and redirects users back to the appropriate page.
