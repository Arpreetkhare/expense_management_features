# Expense Management Features

## Overview
This is a FastAPI-based application that provides a platform for managing expenses and user groups. Features include user registration,
OTP-based authentication, group creation, expense tracking, and reporting.
## Features
- **User Authentication:**  Register users with OTP-based authentication.Generate and verify OTPs.Access token for secure user operations.
- **Expense Tracking:** Add and view expenses with categories like Food, Transport, Entertainment, and Shopping.
- **Group Management:** Collaborate with others by creating and joining expense groups.
- **Role-Based Access:** Users have specific roles (admin, member) with assigned permissions.
- **Secure Authentication:** Uses JWT for secure user login and role verification.
- **Analytics:** Visualize spending trends and get detailed expense reports.

## Tech Stack
- **Backend:** Python, FastAPI/SQLAlchemy
- **Database:** MySQL (async)
- **Authentication:** JWT

## **API Endpoints**

### **User Authentication**
| **Method** | **Endpoint**      | **Description**                 |
|------------|-------------------|---------------------------------|
| POST       | `/register`       | Register a new user             |
| POST       | `/otp`            | Generate an OTP for the user    |
| POST       | `/verify-otp`     | Verify OTP and get JWT          |

### **Expense Management**
| **Method** | **Endpoint**        | **Description**                |
|------------|---------------------|--------------------------------|
| POST       | `/add`              | Add a new expense              |
| GET        | `/get_expense`      | Get a list of expenses         |
| PUT        | `/update_expense/<id>` | Edit an expense               |
| DELETE     | `/delete_expense/<id>` | Delete an expense            |

### **Group Management**
| **Method** | **Endpoint**         | **Description**                |
|------------|----------------------|--------------------------------|
| POST       | `/create_group`      | Create a new group             |
| POST       | `/add_member/<group_id>` | Add a member to a group     |
| GET        | `/get_groups`        | Get a list of user groups      |
| GET        | `/get_groupmember/<group_id>` | Get members of a group |

 

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Arpreetkhare/expense_management_features.git
   cd your-repository

2. **Set up a virtual environment:**
     ```bash
     python3 -m venv env
     source .venv/bin/activate
   
4. **Install dependencies:**
     ```bash
     pip install -r requirements.txt

5. **Run the application:**
      ```bash
      uvicorn main:app --reload
6. **Access the app:** 
   http://127.0.0.1:8000

## Author 
  Arpreet Khare
 

   
