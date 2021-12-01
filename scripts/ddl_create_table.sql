-- Exported from QuickDBD: https://www.quickdatabasediagrams.com/
-- NOTE! If you have used non-SQL datatypes in your design, you will have to change these here.


CREATE TABLE "city" (
    "city_id" INT   NOT NULL,
    "name" TEXT   NOT NULL,
    "coord_lon" TEXT   NOT NULL,
    "coord_lat" TEXT   NOT NULL,
    CONSTRAINT "pk_city" PRIMARY KEY (
        "city_id"
     )
);

CREATE TABLE "temperature" (
    "temperature_id" SERIAL   NOT NULL,
    "city_id" INT   NOT NULL,
    "datetime" TEXT   NOT NULL,
    "main_temp" DECIMAL   NOT NULL,
    "main_feels_like" DECIMAL   NOT NULL,
    "main_temp_min" DECIMAL   NOT NULL,
    "main_temp_max" DECIMAL   NOT NULL,
    CONSTRAINT "pk_temperature" PRIMARY KEY (
        "temperature_id"
     )
);

CREATE TABLE "atmosphere" (
    "atmosphere_id" SERIAL   NOT NULL,
    "city_id" INT   NOT NULL,
    "datetime" TEXT   NOT NULL,
    "main_pressure" DECIMAL   NOT NULL,
    "main_humidity" DECIMAL   NOT NULL,
    "wind_deg" INT   NOT NULL,
    "clouds_all" INT   NOT NULL,
    "wind_gust" DECIMAL   NOT NULL,
    CONSTRAINT "pk_atmosphere" PRIMARY KEY (
        "atmosphere_id"
     )
);

ALTER TABLE "temperature" ADD CONSTRAINT "fk_temperature_city_id" FOREIGN KEY("city_id")
REFERENCES "city" ("city_id");

ALTER TABLE "atmosphere" ADD CONSTRAINT "fk_atmosphere_city_id" FOREIGN KEY("city_id")
REFERENCES "city" ("city_id");

