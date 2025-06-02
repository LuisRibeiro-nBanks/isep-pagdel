-- DROP DATABASE AT THE START --
DROP TABLE IF EXISTS Fact_Measurements;
DROP TABLE IF EXISTS Location;
DROP TABLE IF EXISTS Datetime;
DROP TABLE IF EXISTS Parameter;


-- CREATE TABLES FOR THE DATABASE --
CREATE TABLE Location(
    location_id INTEGER PRIMARY KEY,
    name VARCHAR(68),
    latitude FLOAT,
    longitude FLOAT,
    sensor_type VARCHAR(68)
);


CREATE TABLE Datetime(
    datetime_id INTEGER PRIMARY KEY,
    datetime TIMESTAMP,
    hour SMALLINT,
    day SMALLINT,
    month SMALLINT,
    year SMALLINT,
    is_weekend BOOLEAN
);


CREATE TABLE Parameter(
    parameter_id INTEGER PRIMARY KEY,
    parameter_name VARCHAR(68),
    type VARCHAR(68),
    unit VARCHAR(68)
);


CREATE TABLE Fact_Measurements(
    datetime_id INTEGER,
    location_id INTEGER,
    parameter_id INTEGER,
    value FLOAT,
    unit VARCHAR(68),

    PRIMARY KEY (datetime_id, location_id, parameter_id),
    FOREIGN KEY (datetime_id) REFERENCES datetime(datetime_id) ON DELETE CASCADE,
    FOREIGN KEY (location_id) REFERENCES location(location_id) ON DELETE CASCADE,
    FOREIGN KEY (parameter_id) REFERENCES parameter(parameter_id) ON DELETE CASCADE
);


