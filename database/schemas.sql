CREATE DATABASE
employee_intelligence_system;
USE employee_intelligence_system;
CREATE TABLE departments (
    department_id INT AUTO_INCREMENT PRIMARY KEY,
    department_name VARCHAR(100) NOT NULL,
    description TEXT
);
CREATE TABLE employees (
    employee_id VARCHAR(10) PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50),
    email VARCHAR(100) UNIQUE,
    phone VARCHAR(15),
    gender ENUM('Male','Female','Other'),
    dob DATE,
    joining_date DATE,
    department_id INT,
    designation VARCHAR(100),
    education VARCHAR(100),
    skills TEXT,
    base_salary DECIMAL(10,2),
    manager_rating DECIMAL(2,1),
    attendance_percentage DECIMAL(5,2),
    leave_balance INT,
    status ENUM('Active','Resigned') DEFAULT 'Active',

    FOREIGN KEY (department_id)
    REFERENCES departments(department_id)
);

CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role ENUM('Admin','HR','Employee') NOT NULL,
    employee_id VARCHAR(10),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP NULL,
    status ENUM('Active','Inactive') DEFAULT 'Active',

    FOREIGN KEY (employee_id)
    REFERENCES employees(employee_id)
);

CREATE TABLE attendance (
    attendance_id INT AUTO_INCREMENT PRIMARY KEY,
    employee_id VARCHAR(10),
    attendance_date DATE,
    check_in TIME,
    check_out TIME,
    status ENUM('Present','Absent','Leave'),

    FOREIGN KEY (employee_id)
    REFERENCES employees(employee_id)
);

CREATE TABLE leave_requests (
    leave_id INT AUTO_INCREMENT PRIMARY KEY,
    employee_id VARCHAR(10),
    from_date DATE,
    to_date DATE,
    reason TEXT,
    status ENUM('Pending','Approved','Rejected') DEFAULT 'Pending',
    applied_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (employee_id)
    REFERENCES employees(employee_id)
);

CREATE TABLE predictions (
    prediction_id INT AUTO_INCREMENT PRIMARY KEY,
    employee_id VARCHAR(10),
    predicted_salary DECIMAL(10,2),
    promotion_prediction ENUM('Yes','No'),
    attrition_prediction ENUM('Low','Medium','High'),
    prediction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (employee_id)
    REFERENCES employees(employee_id)
);


INSERT INTO departments (department_name, description)
VALUES
('IT', 'Information Technology'),
('HR', 'Human Resources'),
('Finance', 'Finance Department'),
('Sales', 'Sales Department'),
('Marketing', 'Marketing Department');

INSERT INTO users
(username, password_hash, role)
VALUES
(
'admin',
'hashed_password_here',
'Admin'
);

INSERT INTO users
(username, password_hash, role)
VALUES
(
'hr001',
'hashed_password_here',
'HR'
);