CREATE USER logulifeuser WITH PASSWORD 'somestrongdbpassword';

CREATE DATABASE logulife_app;

GRANT ALL PRIVILEGES ON DATABASE logulife_app to logulifeuser;

ALTER USER logulifeuser CREATEDB;
