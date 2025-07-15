-- Create database and select it
CREATE DATABASE IF NOT EXISTS employee;
USE employee;
-- 1. Create department table first (referenced by empdata)
CREATE TABLE department (
    Dept_ID INT PRIMARY KEY,
    Dept_Name VARCHAR(100)
);

-- 2. Create empdata table with foreign key to department
CREATE TABLE empdata (
    Id INT PRIMARY KEY,
    Name VARCHAR(255),
    Email_Id VARCHAR(255),
    Phone_no VARCHAR(15),
    Address VARCHAR(255),
    Post VARCHAR(255),
    Salary FLOAT,
    Dept_ID INT,
    FOREIGN KEY (Dept_ID) REFERENCES department(Dept_ID)
);

-- 3. Create project table
CREATE TABLE project (
    Project_ID INT PRIMARY KEY,
    Project_Name VARCHAR(100),
    Start_Date DATE,
    End_Date DATE
);

CREATE TABLE attendance (
    Attendance_ID INT PRIMARY KEY AUTO_INCREMENT,
    Emp_ID INT,
    Date DATE,
    Status ENUM('Present', 'Absent', 'Leave'),
    FOREIGN KEY (Emp_ID) REFERENCES empdata(Id) ON DELETE CASCADE
);

CREATE TABLE employee_project (
    Emp_ID INT,
    Project_ID INT,
    Role VARCHAR(100),
    PRIMARY KEY (Emp_ID, Project_ID),
    FOREIGN KEY (Emp_ID) REFERENCES empdata(Id) ON DELETE CASCADE,
    FOREIGN KEY (Project_ID) REFERENCES project(Project_ID)
);