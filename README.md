# Distributed Database System – Data Intensive Systems

This project is part of the **Data Intensive Systems** course.  
The goal of the assignment is to design and implement a simple distributed database setup and provide a graphical application to access multiple databases.

---

## Project Overview

The project simulates a distributed database system for an international e-commerce company.  
It includes **three separate SQL Server databases**, each representing a different region:

- Store_UnitedStates  
- Store_UK  
- Store_Japan  

Each database contains the same schema but with a mix of **replicated** and **fragmented** data.

A **Python GUI application** is provided to connect to these databases, display data, and update records.

---

## Database Design

### Databases
- Store_UnitedStates
- Store_UK
- Store_Japan

### Tables (same in all databases)
- Customers
- Products
- Orders
- OrderItems
- Payments

### Data Distribution
- **Replicated data**: Shared data that exists in all databases (e.g. common products and customers).
- **Fragmented data**: Region-specific data unique to each database.

This design demonstrates how distributed systems can separate global and local data.

---

## Python GUI Application

The Python application provides a simple graphical interface to:

- Select and connect to one of the databases
- Display (“print”) the top 100 rows from any table
- Update product prices in the selected database

### Technologies Used
- Python 3
- Tkinter (GUI)
- ttkbootstrap (optional styling)
- pyodbc
- Microsoft SQL Server

---

## How to Run the Project

### 1. Database Setup
- Open **SQL Server Management Studio (SSMS)**
- Run the provided SQL script to:
  - Create the databases
  - Create tables
  - Insert replicated and fragmented dummy data

### 2. Install Python Dependencies
```bash
pip install pyodbc
pip install ttkbootstrap
python gui_app.py

