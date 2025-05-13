pip install psycopg2 flask
#CREATE DATABASE attendance_system;
CREATE TABLE attendance (
    id SERIAL PRIMARY KEY,
    user_id TEXT,
    name TEXT,
    branch TEXT,
    degree TEXT,
    timestamp TIMESTAMP
);#