# 5G-Attendance-System

steps for setting up the DB part:
1. install the docker in the device
2. run this in the terminal -> docker pull postgres
3. then run this in terminal to setup the DB Container in the docker -> docker run --name attendance-db -e POSTGRES_USER=admin -e POSTGRES_PASSWORD=admin123 -e POSTGRES_DB=attendance -p 5432:5432 -d postgres 
these username and password are only for testing purpose you can do this using the yml file also, already provided in the code
4. then run this in the terminal to enter into the attendance db container -> docker exec -it attendance-db psql -U admin -d attendance 
5. then create those tables using the standard sql format for creating the table
6. try inserting sample values through terminal itself -> INSERT INTO users (name, fingerprint_hash, role)
VALUES ('Arpit', 'fgh12sdf8234kjsdf', 'student');
7. this time for another table -> INSERT INTO attendance_logs (user_id, purpose)
VALUES (1, 'Class attendance');
8. then try running the follwoing commands 1 by 1 to check the logs of your docker

    \dt

    SELECT * FROM users;

    SELECT * FROM attendance_logs;

9. now run the test_db.py file in the desired python enviroment
