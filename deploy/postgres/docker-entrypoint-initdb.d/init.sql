CREATE USER logulifeuser WITH PASSWORD 'somestrongdbpassword';

CREATE DATABASE logulife_web;

GRANT ALL PRIVILEGES ON DATABASE logulife_web to logulifeuser;

ALTER USER logulifeuser CREATEDB;
