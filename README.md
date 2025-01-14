# ManagerBeans
Office ai
5002 /ai

# Home
3000 /

# Postgres
5432

# Postgres Admin (not working)
8050 - (5432)

# Dashboard
3001 /dash

# docker
workflow

# nginx
80 ()

# authorization
5000 /auth

# Dashboard Backend
5001 /auth

# Node JS
5002 /node

# React Flow
3002 /flow

# docker visualizer
8080 ()

# temp
File storage or artifact storage



# Nginx
docker build -t nginx-balancer .
docker run -it --name nginx-container -p 81:80 --network my-network nginx-balancer

# AI
docker run -it --name webapp-ai -p 11434:11434 -v ollama:/root/.ollama --network my-network ollama/ollama

# AI Backend
docker run -it --name webapp-aiback -p 5002:5000 --network my-network webapp-aiback

# Home
docker build -t webapp-home .
docker run -it --name webapp-home -p 3000:3000 --network my-network webapp-home

# Dashboard
docker build -t webapp-dash .
docker run -it --name webapp-dash -p 3001:3000 --network my-network webapp-dash

# Postgres
docker run --name webapp-postgres --network  my-network -e POSTGRES_HOST_AUTH_METHOD=trust -v postgresdatabase:/var/lib/postgresql/data -it postgres

##
\l
\c ujwal
SELECT table_name
FROM information_schema.tables
WHERE table_type = 'BASE TABLE'
AND table_schema NOT IN ('pg_catalog', 'information_schema');


# postgres cli
docker exec -it webapp-postgres psql -U postgres

# Auth
docker build -t webapp-auth .
docker run -it --name webapp-auth -p 5000:5000 --network my-network webapp-auth

# Dashboard Backend
docker build -t webapp-dashback .
docker run -it --name webapp-dashback -p 5001:5000 --network my-network webapp-dashback

# Postgres Admin (application working)
docker run -d --name webapp-pgadmin --network my-network -p 5050:5050  thajeztah/pgadmin4

# Swarm visualizer
docker swarm init
docker run -it -d -p 8081:8080 --name vis -v /var/run/docker.sock:/var/run/docker.sock dockersamples/visualizer

$$ docker swarm join --token SWMTKN-1-5pefww4sftexv76139ucuvmt3l4nx7c2n9hl25wqqzl5vy9ebs-ddgmadny55ij4l258f56zh23f 192.168.65.3:2377
$$ current node (onld95abuc43tdomv6yy9mvpr) is now a manager.

docker network create -d overlay replication
docker network inspect replication
docker service create --name nginx-container -p 81:80 --network replication --replicas 1 nginx-balancer
docker service create --name webapp-dash -p 3001:3000 --network replication --replicas 1 webapp-dash
docker service create --name webapp-aiback -p 5002:5000 --network replication --replicas 1 webapp-aiback
docker service create --name webapp-dashback -p 5001:5000 --network replication --replicas 1 webapp-dashback
docker service create --name webapp-postgres --network replication -e POSTGRES_HOST_AUTH_METHOD=trust --replicas 1 --mount type=volume,source=postgresdatabase,target=/var/lib/postgresql/data postgres
docker service create -d --network replication -p 5000:5000 --name webapp-auth --replicas 1 webapp-auth
docker service create --name webapp-ai --network replication -p 11434:11434 -d --network replication --replicas 1 --mount type=volume,source=ollama,target=/root/.ollama --network replication ollama/ollama

$$ docker service update --replicas 7 sleep-app

docker service rm nginx-container
docker service rm webapp-dash
docker service rm webapp-postgres
docker service rm webapp-dashback
docker service rm webapp-ai

docker kill vis
docker swarm leave --force










events {
    worker_connections 1024;
}

http {
    server {
        listen 80;
        server_name localhost;

        location /auth {
            proxy_pass http://webapp-auth:5000;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        location / {
            proxy_pass http://webapp-home:3000;
        }
    }
}



events {
    worker_connections 1024;
}

http {
    server {
        listen 80;
        server_name localhost;

        location /dash/apps-chat {
            proxy_pass http://webapp-dash:3000/apps-chat.html;
        }

        location /dash/apps-projects-add {
            proxy_pass http://webapp-dash:3000/apps-projects-add.html;
        }

        location /dash/apps-projects-list {
            proxy_pass http://webapp-dash:3000/apps-projects-list;
        }

        location /dash/apps-task {
            proxy_pass http://webapp-dash:3000/apps-task.html;
        }

        location /dash/ {
            proxy_pass http://webapp-dash:3000/;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        location /dash/index {
            proxy_pass http://webapp-dash:3000/index.html;
        }
    }
}











-- Employee TABLE
CREATE TABLE Employee (
    path VARCHAR(100),
    EmployeeID SERIAL PRIMARY KEY,
    FullName VARCHAR(100),
    DateOfBirth DATE,
    Gender VARCHAR(10),
    PhoneNumber VARCHAR(20),
    Email VARCHAR(100),
    Address TEXT
);

-- Department Table
CREATE TABLE Departments (
    DepartmentID SERIAL PRIMARY KEY,
    DepartmentName VARCHAR(100),
    ParentDepartmentID INT REFERENCES Departments(DepartmentID)
);

-- Work Information Table
CREATE TABLE WorkInformation (
    EmployeeID INT PRIMARY KEY REFERENCES Employee(EmployeeID) ON DELETE CASCADE,
    JobTitle VARCHAR(100),
    DepartmentID INT REFERENCES Departments(DepartmentID),
    ManagerID INT REFERENCES Employee(EmployeeID),
    HireDate DATE,
    OfficeLocation VARCHAR(100),
    EmploymentStatus VARCHAR(20),
    Salary DECIMAL(10, 2),
    PerformanceReviews TEXT
);

-- Private Information Table
CREATE TABLE PrivateInformation (
    EmployeeID INT PRIMARY KEY REFERENCES Employee(EmployeeID) ON DELETE CASCADE,
    EmergencyContact VARCHAR(100),
    NextOfKin VARCHAR(100),
    MedicalInformation TEXT,
    BankAccount VARCHAR(100),
    TaxInformation VARCHAR(100)
);

-- Skills Table
CREATE TABLE Skills (
    SkillID SERIAL PRIMARY KEY,
    EmployeeID INT REFERENCES Employee(EmployeeID) ON DELETE CASCADE,
    SkillName VARCHAR(100),
    ProficiencyLevel VARCHAR(50)
);

-- Current Status Table
CREATE TABLE CurrentStatus (
    EmployeeID INT PRIMARY KEY REFERENCES Employee(EmployeeID) ON DELETE CASCADE,
    Status VARCHAR(20),
    LastUpdated TIMESTAMP
);

-- Contract Documents Table
CREATE TABLE ContractDocuments (
    ContractID SERIAL PRIMARY KEY,
    EmployeeID INT REFERENCES Employee(EmployeeID) ON DELETE CASCADE,
    ContractStartDate DATE,
    ContractEndDate DATE,
    TermsAndConditions TEXT,
    LegalAgreements TEXT
);

-- Projects Table
CREATE TABLE Projects (
    ProjectID SERIAL PRIMARY KEY,
    ProjectName VARCHAR(100),
    ProjectDescription TEXT,
    StartDate DATE,
    EndDate DATE,
    ProjectManagerID INT REFERENCES Employee(EmployeeID) ON DELETE SET NULL,
    Budget DECIMAL(15, 2),
    Status VARCHAR(20),
    ClientInformation TEXT,
    RelevantDocuments TEXT
);

-- Employee-Project Relationship Table
CREATE TABLE EmployeeProjectRelationship (
    EmployeeID INT REFERENCES Employee(EmployeeID) ON DELETE CASCADE,
    ProjectID INT REFERENCES Projects(ProjectID) ON DELETE CASCADE,
    PRIMARY KEY (EmployeeID, ProjectID)
);

-- Open position Table
CREATE TABLE Position (
    position_id SERIAL PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    DepartmentID INT NOT NULL REFERENCES Departments(DepartmentID)
);

-- Required Recruitment Skills Table
CREATE TABLE Recruitment_Skill (
    skill_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT
);

-- Position_Recruitment_Skill Table
CREATE TABLE Position_Recruitment_Skill (
    position_id INT NOT NULL REFERENCES Position(position_id),
    skill_id INT NOT NULL REFERENCES Recruitment_Skill(skill_id),
    PRIMARY KEY (position_id, skill_id)
);

-- Task Table
CREATE TABLE tasks (
    task_id SERIAL PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    description TEXT,
    deadline TIMESTAMP NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'Pending', -- Pending, In Progress, Completed, etc.
    assigned_to INTEGER REFERENCES Employee(EmployeeID) ON DELETE CASCADE,
    created_by INTEGER REFERENCES Employee(EmployeeID) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    -- Add other relevant fields such as priority, category, etc.
);

-- Task Category table
CREATE TABLE task_categories (
    category_id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL
);

-- Task Category Mapping table
CREATE TABLE task_category_mapping (
    task_id INT REFERENCES tasks(task_id),
    category_id INT REFERENCES task_categories(category_id),
    PRIMARY KEY (task_id, category_id)
);

-- Employee Task table
CREATE TABLE user_tasks (
    EmployeeID INT REFERENCES Employee(EmployeeID) ON DELETE CASCADE,
    task_id INTEGER REFERENCES tasks(task_id),
    PRIMARY KEY (EmployeeID, task_id)
);

-- Workload table
CREATE TABLE workload (
    EmployeeID INT REFERENCES Employee(EmployeeID) ON DELETE CASCADE,
    date DATE NOT NULL,
    tasks_count INTEGER NOT NULL DEFAULT 0,
    PRIMARY KEY (EmployeeID, date)
    -- Add other relevant workload metrics such as hours worked, tasks completed, etc.
);

-- overwork_log table
CREATE TABLE overwork_log (
    log_id SERIAL PRIMARY KEY,
    EmployeeID INT REFERENCES Employee(EmployeeID) ON DELETE CASCADE,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    -- Add other relevant fields such as severity, resolution status, etc.
);

-- Interviewers table to store information about interviewers
CREATE TABLE interviewers (
    id SERIAL PRIMARY KEY,
    EmployeeID INT REFERENCES Employee(EmployeeID) ON DELETE CASCADE,
    DepartmentID INT REFERENCES Departments(DepartmentID)
);

-- Topics table to store information about interview topics
CREATE TABLE IF NOT EXISTS topics (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT
);

-- Interview Types table to store types of interviews
CREATE TABLE IF NOT EXISTS interview_types (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT
);

-- Hiring Flows table to store information about the overall hiring process
CREATE TABLE IF NOT EXISTS hiring_flows (
    id SERIAL PRIMARY KEY,
    DepartmentID INT REFERENCES Departments(DepartmentID),
    name VARCHAR(100) NOT NULL,
    description TEXT,
    start_date DATE,
    end_date DATE
);

-- Rounds table to store information about different rounds in the hiring process
CREATE TABLE IF NOT EXISTS rounds (
    id SERIAL PRIMARY KEY,
    hiring_flow_id INT REFERENCES hiring_flows(id),
    round_number INT,
    topic_id INT REFERENCES topics(id),
    interviewer_id INT REFERENCES interviewers(id),
    interview_type_id INT REFERENCES interview_types(id),
    evaluation_process TEXT,
    start_time TIMESTAMP,
    end_time TIMESTAMP
);

-- Candidates table to store information about candidates
CREATE TABLE IF NOT EXISTS candidates (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(100),
    phone VARCHAR(20),
    resume_url VARCHAR(255),
    applied_date DATE
);

-- Applications table to store information about candidate applications
CREATE TABLE IF NOT EXISTS applications (
    id SERIAL PRIMARY KEY,
    candidate_id INT REFERENCES candidates(id),
    hiring_flow_id INT REFERENCES hiring_flows(id),
    status VARCHAR(50),
    applied_date DATE,
    current_round_number INT,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);











-- Employee Table
INSERT INTO Employee (path, FullName, DateOfBirth, Gender, PhoneNumber, Email, Address)
VALUES ('/assets/images/users/avatar-1.jpg', 'John Doe', '1990-05-15', 'Male', '123-456-7890', 'john.doe@example.com', '123 Main St, City, Country'),
       ('/assets/images/users/avatar-2.jpg', 'Jane Smith', '1985-09-20', 'Female', '987-654-3210', 'jane.smith@example.com', '456 Elm St, City, Country'),
       ('/assets/images/users/avatar-3.jpg', 'Michael Johnson', '1982-03-10', 'Male', '555-555-5555', 'michael.johnson@example.com', '789 Oak St, City, Country'),
       ('/assets/images/users/avatar-4.jpg', 'Emily Brown', '1995-12-28', 'Female', '777-777-7777', 'emily.brown@example.com', '321 Pine St, City, Country'),
       ('/assets/images/users/avatar-5.jpg', 'David Lee', '1988-07-02', 'Male', '999-999-9999', 'david.lee@example.com', '654 Maple St, City, Country');
       
       -- Department Table
INSERT INTO Departments (DepartmentName, ParentDepartmentID) VALUES
    ('Management', NULL), -- Top-level department
    ('R & D', NULL), -- Top-level department
    ('Sales', NULL), -- Top-level department
    ('Administration', 1), -- Sub-department of Management
    ('Professional Services', 1), -- Sub-department of Management
    ('Research and Development USA', 2), -- Sub-department of R & D
    ('Research and Development India', 2); -- Sub-department of R & D

-- Work Information Table
INSERT INTO WorkInformation (EmployeeID, JobTitle, DepartmentID, ManagerID, HireDate, OfficeLocation, EmploymentStatus, Salary, PerformanceReviews)
VALUES (1, 'Software Engineer', 1, 3, '2018-01-15', 'HQ Building', 'Full-time', 90000.00, 'Excellent performer, consistently meets deadlines.'),
       (2, 'Data Scientist', 2, 4, '2016-05-20', 'Tech Park', 'Full-time', 100000.00, 'Highly skilled in data analysis and visualization.'),
       (3, 'Product Manager', 3, 5, '2014-09-10', 'Main Office', 'Full-time', 120000.00, 'Effective leader with strong communication skills.'),
       (4, 'UI/UX Designer', 4, 2, '2020-03-01', 'Downtown Office', 'Full-time', 85000.00, 'Creative thinker with an eye for detail.'),
       (5, 'Network Administrator', 5, 1, '2017-07-15', 'Tech Campus', 'Full-time', 95000.00, 'Skilled in network infrastructure management.');

-- Private Information Table
INSERT INTO PrivateInformation (EmployeeID, EmergencyContact, NextOfKin, MedicalInformation, BankAccount, TaxInformation)
VALUES (1, 'Mary Doe (sister)', 'Alice Doe (mother)', 'No medical conditions', '1234567890', '123-45-6789'),
       (2, 'John Smith (brother)', 'Jane Smith (sister)', 'Allergies: None', '9876543210', '987-65-4321'),
       (3, 'Peter Johnson (brother)', 'Sarah Johnson (sister)', 'Blood Type: O+', '5555555555', '555-55-5555'),
       (4, 'Emma Brown (sister)', 'Mark Brown (brother)', 'Medications: None', '7777777777', '777-77-7777'),
       (5, 'Lisa Lee (sister)', 'Chris Lee (brother)', 'No medical conditions', '9999999999', '999-99-9999');

-- Skills Table
INSERT INTO Skills (EmployeeID, SkillName, ProficiencyLevel)
VALUES (1, 'Java', 'Beginner'),
       (1, 'SQL', 'Intermediate'),
       (2, 'Python', 'Expert'),
       (2, 'Machine Learning', 'Beginner'),
       (3, 'Product Management', 'Expert'),
       (3, 'Agile Methodologies', 'Beginner'),
       (4, 'UI Design', 'Intermediate'),
       (4, 'Adobe XD', 'Intermediate'),
       (5, 'Network Security', 'Expert'),
       (5, 'Cisco Networking', 'Beginner');

-- Current Status Table
INSERT INTO CurrentStatus (EmployeeID, Status, LastUpdated)
VALUES (1, 'Working', CURRENT_TIMESTAMP),
       (2, 'Working', CURRENT_TIMESTAMP),
       (3, 'Working', CURRENT_TIMESTAMP),
       (4, 'Working', CURRENT_TIMESTAMP),
       (5, 'Working', CURRENT_TIMESTAMP);

-- Contract Documents Table
INSERT INTO ContractDocuments (EmployeeID, ContractStartDate, ContractEndDate, TermsAndConditions, LegalAgreements)
VALUES (1, '2018-01-15', '2023-01-14', 'Terms and conditions apply.', 'Agreement signed on 2018-01-15.'),
       (2, '2016-05-20', '2021-05-19', 'Terms and conditions apply.', 'Agreement signed on 2016-05-20.'),
       (3, '2014-09-10', '2022-09-09', 'Terms and conditions apply.', 'Agreement signed on 2014-09-10.'),
       (4, '2020-03-01', '2025-03-01', 'Terms and conditions apply.', 'Agreement signed on 2020-03-01.'),
       (5, '2017-07-15', '2022-07-14', 'Terms and conditions apply.', 'Agreement signed on 2017-07-15.');

-- Projects Table
INSERT INTO Projects (ProjectName, ProjectDescription, StartDate, EndDate, ProjectManagerID, Budget, Status, ClientInformation, RelevantDocuments)
VALUES ('E-commerce Platform Development', 'Developing an online marketplace for various products.', '2021-01-01', '2022-06-30', 1, 1000000.00, 'Ongoing', 'Client: XYZ Corporation', 'Project plan, requirements document'),
       ('Data Analytics Dashboard Implementation', 'Building a dashboard for analyzing sales data.', '2020-07-01', '2021-12-31', 2, 500000.00, 'Completed', 'Client: ABC Company', 'Data analysis report, user feedback'),
       ('New Product Launch', 'Launching a new software product into the market.', '2022-03-01', '2023-09-30', 3, 1500000.00, 'Planning', 'Client: LMN Enterprises', 'Market research report, product roadmap'),
       ('Website Redesign', 'Redesigning the company website for better user experience.', '2021-04-01', '2022-02-28', 4, 300000.00, 'In Progress', 'Internal Project', 'Wireframes, design mockups'),
       ('Network Infrastructure Upgrade', 'Upgrading network infrastructure for improved performance.', '2022-01-01', '2022-12-31', 5, 800000.00, 'Ongoing', 'Internal Project', 'Network architecture plan, equipment list');

-- Insert values into EmployeeProjectRelationship table
INSERT INTO EmployeeProjectRelationship (EmployeeID, ProjectID)
VALUES (1, 1), -- Employee 1 assigned to Project 1001
       (2, 1), -- Employee 2 assigned to Project 1001
       (3, 2), -- Employee 3 assigned to Project 1002
       (4, 3), -- Employee 4 assigned to Project 1003
       (5, 3); -- Employee 5 assigned to Project 1003

-- Inserting data into the Position table
INSERT INTO Position (title, DepartmentID) VALUES
    ('HR Manager', 1),
    ('Recruiter', 1),
    ('Marketing Specialist', 2),
    ('Software Engineer', 3),
    ('QA Engineer', 3),
    ('Financial Analyst', 4),
    ('Accountant', 4),
    ('Sales Manager', 5),
    ('Sales Representative', 5);

-- Inserting data into the Recruitment_Skill table
INSERT INTO Recruitment_Skill (name, description) VALUES
    ('Recruitment Strategy', 'Developing effective recruitment strategies'),
    ('Interviewing', 'Conducting interviews and evaluating candidates'),
    ('Marketing Campaigns', 'Planning and executing marketing campaigns'),
    ('Programming', 'Software development using various programming languages'),
    ('Testing', 'Quality assurance testing of software products'),
    ('Financial Analysis', 'Analyzing financial data and preparing reports'),
    ('Accounting Principles', 'Applying accounting principles and standards'),
    ('Sales Strategy', 'Developing and implementing sales strategies'),
    ('Customer Relationship Management', 'Managing customer relationships and interactions'),
    ('Negotiation', 'Negotiating deals and contracts');

-- Inserting data into the Position_Recruitment_Skill table
INSERT INTO Position_Recruitment_Skill (position_id, skill_id) VALUES
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
    (5, 5),
    (6, 6),
    (7, 7),
    (8, 8),
    (9, 9);

-- Insert Tasks
INSERT INTO tasks (title, description, deadline, status, assigned_to, created_by) VALUES
    ('Review Job Applications', 'Review job applications for new positions.', '2024-03-15 09:00:00', 'Pending', 1, 1),
    ('Employee Training', 'Schedule training sessions for new hires.', '2024-03-10 14:00:00', 'In Progress', 1, 1),
    ('Performance Appraisals', 'Conduct performance appraisals for employees.', '2024-03-20 12:00:00', 'Pending', 1, 1),
    ('Prepare Monthly Report', 'Compile HR department"s monthly report.', '2024-03-31 17:00:00', 'Pending', 1, 1),
    ('Submit Expense Report', 'Submit expense report for reimbursement.', '2024-03-05 10:00:00', 'Completed', 2, 2);

-- Insert task categories
INSERT INTO task_categories (name) VALUES
    ('Administrative'),
    ('Technical'),
    ('HR'),
    ('Finance');

-- Insert task-category mappings
-- For example, associating task with task_id = 1 with Administrative and HR categories
INSERT INTO task_category_mapping (task_id, category_id) VALUES
    (1, 1),  -- Task 1 belongs to Administrative category
    (1, 3);  -- Task 1 belongs to HR category

-- Inserting task 2 into Technical and Finance categories
INSERT INTO task_category_mapping (task_id, category_id) VALUES
    (2, 2),  -- Task 2 belongs to Technical category
    (2, 4);  -- Task 2 belongs to Finance category

-- Inserting task 3 into HR category
INSERT INTO task_category_mapping (task_id, category_id) VALUES
    (3, 3);  -- Task 3 belongs to HR category

-- Insert User Tasks
INSERT INTO user_tasks (EmployeeID, task_id) VALUES
    (1, 1),
    (1, 2),
    (1, 3),
    (1, 4),
    (2, 5);

-- Insert Workload Data (Assuming tasks count for each user for a specific date):
INSERT INTO workload (EmployeeID, date, tasks_count) VALUES
    (1, '2024-03-01', 4),
    (1, '2024-03-02', 5),
    (1, '2024-03-03', 4),
    (2, '2024-03-01', 1),
    (2, '2024-03-02', 2),
    (2, '2024-03-03', 2);

-- Insert sample interviewers
INSERT INTO interviewers (EmployeeID, DepartmentID) VALUES 
    (1, 1),
    (1, 2);

-- Insert sample topics
INSERT INTO topics (name, description) VALUES 
    ('Technical Skills', 'Assessment of technical skills and knowledge'),
    ('Behavioral Competencies', 'Assessment of soft skills and behavioral competencies');

-- Insert sample interview types
INSERT INTO interview_types (name, description) VALUES 
    ('Technical Interview', 'Evaluation of technical skills and knowledge'),
    ('Behavioral Interview', 'Evaluation of soft skills and behavioral competencies');

-- Insert sample hiring flows
INSERT INTO hiring_flows (DepartmentID, name, description, start_date, end_date) VALUES 
    (1, 'Software Engineer Hiring Flow', 'Hiring flow for software engineering positions', '2024-03-01', '2024-03-31'),
    (2, 'Marketing Specialist Hiring Flow', 'Hiring flow for marketing specialist positions', '2024-03-01', '2024-03-31');

-- Insert sample candidates
INSERT INTO candidates (first_name, last_name, email, phone, resume_url, applied_date) VALUES 
    ('Alice', 'Johnson', 'alice.johnson@example.com', '+1234567890', '', '2024-03-05'),
    ('Bob', 'Smith', 'bob.smith@example.com', '+1987654321', '', '2024-03-07');

-- Insert sample applications with current round numbers
INSERT INTO applications (candidate_id, hiring_flow_id, status, applied_date, current_round_number) VALUES 
    (1, 1, 'Submitted', '2024-03-05', 1),
    (2, 2, 'In Review', '2024-03-07', 1);

-- Insert sample rounds with start and end times
INSERT INTO rounds (hiring_flow_id, round_number, topic_id, interviewer_id, interview_type_id, evaluation_process, start_time, end_time) VALUES 
    (1, 1, 1, 1, 1, 'Technical interview assessing coding skills and problem-solving abilities', '2024-03-10 09:00:00', '2024-03-10 10:00:00'),
    (1, 2, 2, 2, 2, 'Behavioral interview evaluating teamwork and communication skills', '2024-03-15 09:00:00', '2024-03-15 10:00:00'),
    (2, 1, 2, 1, 2, 'Behavioral interview assessing marketing strategy and analytical skills', '2024-03-12 09:00:00', '2024-03-12 10:00:00');











-- Update Employee Table
UPDATE Employee
SET FullName = 'Updated Name',
    DateOfBirth = '1990-01-01',
    Gender = 'Male',
    PhoneNumber = '555-555-5555',
    Email = 'updated.email@example.com',
    Address = '123 Updated St, City, Country'
WHERE EmployeeID = 1;

-- Update Work Information Table
UPDATE WorkInformation
SET JobTitle = 'Updated Job Title',
    DepartmentID = 2,
    ManagerID = 4,
    HireDate = '2015-01-01',
    OfficeLocation = 'Updated Office Location',
    EmploymentStatus = 'Part-time',
    Salary = 80000.00,
    PerformanceReviews = 'Updated performance reviews.'
WHERE EmployeeID = 1;

-- Update Private Information Table
UPDATE PrivateInformation
SET EmergencyContact = 'Updated Emergency Contact',
    NextOfKin = 'Updated Next of Kin',
    MedicalInformation = 'Updated medical information',
    BankAccount = '9876543210',
    TaxInformation = '987-65-4321'
WHERE EmployeeID = 1;

-- Update Skills Table (if applicable)
-- Assuming you are updating all skills of the employee with EmployeeID 1
UPDATE Skills
SET ProficiencyLevel = 'Advanced'
WHERE EmployeeID = 1;

-- Update Current Status Table
UPDATE CurrentStatus
SET Status = 'Away',
    LastUpdated = CURRENT_TIMESTAMP
WHERE EmployeeID = 1;

-- Update Contract Documents Table (if applicable)
-- Assuming you are updating all contracts of the employee with EmployeeID 1
UPDATE ContractDocuments
SET ContractStartDate = '2019-01-01',
    ContractEndDate = '2023-01-01',
    TermsAndConditions = 'Updated terms and conditions',
    LegalAgreements = 'Updated legal agreements'
WHERE EmployeeID = 1;

-- Update Projects Table (if applicable)
-- Assuming you are updating all projects where the employee with EmployeeID 1 is involved
UPDATE Projects
SET ProjectManagerID = 2
WHERE ProjectManagerID = 1;

-- Update Department Name
UPDATE Departments
SET DepartmentName = 'New Department Name'
WHERE DepartmentID = 1; -- Replace '1' with the ID of the department you want to update

-- Update Parent Department
UPDATE Departments
SET ParentDepartmentID = 2
WHERE DepartmentID = 4; -- Replace '4' with the ID of the department you want to update

-- Update the project assigned to an employee
UPDATE EmployeeProjectRelationship
SET ProjectID = 1002 -- Replace '1002' with the new ProjectID
WHERE EmployeeID = 1; -- Replace '1' with the EmployeeID

-- Update Position table
UPDATE Position
SET title = 'HR Director'
WHERE position_id = 1;

-- Update Recruitment_Skill table
UPDATE Recruitment_Skill
SET description = 'Developing and implementing recruitment strategies'
WHERE skill_id = 1;

Certainly! Here are some sample update statements to modify data in the tables:

1. **Update Tasks Status**:
   
```sql
-- Update the status of a specific task to 'Completed'
UPDATE tasks
SET status = 'Completed'
WHERE task_id = 1;
```

2. **Update Task Deadline**:

```sql
-- Update the deadline of a specific task
UPDATE tasks
SET deadline = '2024-03-25 09:00:00'
WHERE task_id = 2;
```

3. **Update User Role**:

```sql
-- Update the role of a specific user
UPDATE users
SET role = 'Manager'
WHERE user_id = 1;
```

4. **Update Workload Information**:

```sql
-- Update the number of tasks for a user on a specific date
UPDATE workload
SET tasks_count = 6
WHERE user_id = 1 AND date = '2024-03-01';
```

5. **Update Task Description**:

```sql
-- Update the description of a specific task
UPDATE tasks
SET description = 'Conduct interviews for shortlisted candidates.'
WHERE task_id = 1;
```

6. **Update Task Assigned User**:

```sql
-- Update the assigned user of a specific task
UPDATE tasks
SET assigned_to = 2
WHERE task_id = 3;
```

These update statements demonstrate how to modify data in the tables, such as updating task status, user roles, task deadlines, workload information, and task descriptions. Adjust the statements as needed to reflect the changes you want to make in your database. Let me know if you need further assistance or additional examples!









SELECT 
    e.EmployeeID,
    e.FullName,
    e.DateOfBirth,
    e.Gender,
    e.PhoneNumber,
    e.Email,
    e.Address,
    wi.JobTitle,
    wi.DepartmentID,
    wi.ManagerID,
    wi.HireDate,
    wi.OfficeLocation,
    wi.EmploymentStatus,
    wi.Salary,
    wi.PerformanceReviews,
    pi.EmergencyContact,
    pi.NextOfKin,
    pi.MedicalInformation,
    pi.BankAccount,
    pi.TaxInformation,
    s.SkillID,
    s.SkillName,
    s.ProficiencyLevel,
    cs.Status,
    cs.LastUpdated,
    cd.ContractID,
    cd.ContractStartDate,
    cd.ContractEndDate,
    cd.TermsAndConditions,
    cd.LegalAgreements,
    p.ProjectID,
    p.ProjectName,
    p.ProjectDescription,
    p.StartDate AS ProjectStartDate,
    p.EndDate AS ProjectEndDate,
    p.ProjectManagerID AS ProjectManagerID,
    p.Budget,
    p.Status AS ProjectStatus,
    p.ClientInformation,
    p.RelevantDocuments,
    d.DepartmentName,
    d.DepartmentDescription
FROM Employee e
LEFT JOIN WorkInformation wi ON e.EmployeeID = wi.EmployeeID
LEFT JOIN PrivateInformation pi ON e.EmployeeID = pi.EmployeeID
LEFT JOIN Skills s ON e.EmployeeID = s.EmployeeID
LEFT JOIN CurrentStatus cs ON e.EmployeeID = cs.EmployeeID
LEFT JOIN ContractDocuments cd ON e.EmployeeID = cd.EmployeeID
LEFT JOIN EmployeeProjectRelationship epr ON e.EmployeeID = epr.EmployeeID
LEFT JOIN Projects p ON epr.ProjectID = p.ProjectID
LEFT JOIN Department d ON wi.DepartmentID = d.DepartmentID
WHERE e.EmployeeID = 1; -- Replace '1' with the desired EmployeeID


-- Delete a Department and its Sub-departments
DELETE FROM Departments
WHERE DepartmentID = 1; -- Replace '1' with the ID of the department you want to delete

-- Delete a specific employee-project relationship
DELETE FROM EmployeeProjectRelationship
WHERE EmployeeID = 1 AND ProjectID = 1001; -- Replace '1' and '1001' with the EmployeeID and ProjectID

-- Delete Employee Record
DELETE FROM Employee
WHERE EmployeeID = 1; -- Replace '1' with the ID of the employee you want to delete

-- Delete Project Record
DELETE FROM Projects
WHERE ProjectID = 1001; -- Replace '1001' with the ID of the project you want to delete

-- Delete a position from the Position table
DELETE FROM Position
WHERE position_id = 10; -- Delete position with position_id = 10

-- Delete a skill from the Recruitment_Skill table
DELETE FROM Recruitment_Skill
WHERE skill_id = 10; -- Delete skill with skill_id = 10

Certainly! Here are some sample delete statements to remove data from the tables:

1. **Delete Tasks**:

```sql
-- Delete a specific task by its ID
DELETE FROM tasks
WHERE task_id = 1;
```

2. **Delete Users**:

```sql
-- Delete a specific user by their ID
DELETE FROM users
WHERE user_id = 2;
```

3. **Delete Task Categories**:

```sql
-- Delete a specific task category by its ID
DELETE FROM task_categories
WHERE category_id = 3;
```

4. **Delete User Tasks**:

```sql
-- Delete all tasks associated with a specific user
DELETE FROM user_tasks
WHERE user_id = 1;
```

5. **Delete Workload Information**:

```sql
-- Delete workload information for a specific user and date
DELETE FROM workload
WHERE user_id = 1 AND date = '2024-03-01';
```

6. **Delete Overwork Logs**:

```sql
-- Delete overwork logs older than a specific date
DELETE FROM overwork_log
WHERE start_date < '2024-01-01';
```

These delete statements demonstrate how to remove data from the tables, such as deleting tasks, users, task categories, user-task associations, workload information, and overwork logs. Adjust the statements as needed to reflect the deletions you want to perform in your database. Let me know if you need further assistance or additional examples!






SELECT *
FROM Employee
WHERE EmployeeID = 1; -- Replace '1' with the ID of the employee you want to retrieve information for

SELECT *
FROM WorkInformation
WHERE EmployeeID = 1; -- Replace '1' with the EmployeeID you want to retrieve work information for

SELECT *
FROM PrivateInformation
WHERE EmployeeID = 1; -- Replace '1' with the EmployeeID you want to retrieve private information for

SELECT *
FROM PrivateInformation
WHERE EmployeeID = 1; -- Replace '1' with the EmployeeID you want to retrieve private information for

SELECT *
FROM Skills
WHERE EmployeeID = 1; -- Replace '1' with the EmployeeID you want to retrieve skills for

SELECT *
FROM CurrentStatus
WHERE EmployeeID = 1; -- Replace '1' with the EmployeeID you want to retrieve current status for

SELECT *
FROM ContractDocuments
WHERE EmployeeID = 1; -- Replace '1' with the EmployeeID you want to retrieve contract documents for

SELECT *
FROM Projects
WHERE ProjectID = 1001; -- Replace '1001' with the ID of the project you want to retrieve information for

SELECT *
FROM Department;

SELECT *
FROM EmployeeProjectRelationship
WHERE EmployeeID = 1; -- Replace '1' with the ID of the employee you want to retrieve project relationships for

Certainly! Here are some example `SELECT` statements to retrieve data from the tables:

1. Retrieve all departments:
```sql
SELECT * FROM Department;
```

2. Retrieve all positions:
```sql
SELECT * FROM Position;
```

3. Retrieve all recruitment skills:
```sql
SELECT * FROM Recruitment_Skill;
```

4. Retrieve all projects:
```sql
SELECT * FROM Project;
```

5. Retrieve positions along with their associated department names:
```sql
SELECT Position.title, Department.name AS department_name
FROM Position
JOIN Department ON Position.department_id = Department.department_id;
```

6. Retrieve projects along with their associated department names:
```sql
SELECT Project.name, Department.name AS department_name
FROM Project
JOIN Department ON Project.department_id = Department.department_id;
```

7. Retrieve positions along with the skills required for each position:
```sql
SELECT Position.title, Recruitment_Skill.name AS required_skill
FROM Position
JOIN Position_Recruitment_Skill ON Position.position_id = Position_Recruitment_Skill.position_id
JOIN Recruitment_Skill ON Position_Recruitment_Skill.skill_id = Recruitment_Skill.skill_id;
```

These are just some examples of `SELECT` statements. You can customize them or combine them as needed to retrieve the specific data you're interested in from your tables.

Certainly! Here are some sample select statements to retrieve data from the tables:

1. **Select All Users**:

```sql
SELECT * FROM users;
```

2. **Select All Tasks**:

```sql
SELECT * FROM tasks;
```

3. **Select Tasks with Assigned Users**:

```sql
SELECT t.*, u.username AS assigned_to_username
FROM tasks t
LEFT JOIN users u ON t.assigned_to = u.user_id;
```

4. **Select Tasks Count by Status**:

```sql
SELECT status, COUNT(*) AS task_count
FROM tasks
GROUP BY status;
```

5. **Select Users with Overworked Tasks**:

```sql
SELECT u.*, w.date, w.tasks_count
FROM users u
JOIN workload w ON u.user_id = w.user_id
WHERE w.tasks_count > 5;
```

6. **Select Tasks Due Today**:

```sql
SELECT *
FROM tasks
WHERE deadline::date = CURRENT_DATE;
```

7. **Select Overwork Logs**:

```sql
SELECT *
FROM overwork_log;
```

8. **Select Task Categories with Task Count**:

```sql
SELECT c.*, COUNT(t.task_id) AS task_count
FROM task_categories c
LEFT JOIN tasks t ON c.category_id = t.category_id
GROUP BY c.category_id, c.name;
```

These select statements demonstrate how to retrieve data from the tables, including users, tasks, task categories, workload information, and overwork logs. You can adjust the queries as needed to filter, aggregate, or join the data based on your specific requirements. Let me know if you need further assistance or additional examples!

SELECT 
    t.task_id,
    t.title AS task_title,
    t.description AS task_description,
    t.deadline AS task_deadline,
    t.status AS task_status,
    u.username AS assigned_to_username
FROM 
    tasks t
LEFT JOIN 
    users u ON t.assigned_to = u.user_id;
