CREATE USER logulifeuser WITH PASSWORD 'somestrongdbpassword';

CREATE DATABASE logulife;

GRANT ALL PRIVILEGES ON DATABASE logulife to logulifeuser;

ALTER USER logulifeuser CREATEDB;
