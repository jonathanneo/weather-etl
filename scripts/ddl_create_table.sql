-- Exported from QuickDBD: https://www.quickdatabasediagrams.com/
-- NOTE! If you have used non-SQL datatypes in your design, you will have to change these here.


CREATE TABLE "suburb" (
    "suburb_id" INT   NOT NULL,
    "suburb_name" TEXT   NOT NULL,
    CONSTRAINT "pk_suburb" PRIMARY KEY (
        "suburb_id"
     )
);

CREATE TABLE "population" (
    "population_id" INT   NOT NULL,
    "suburb_id" INT   NOT NULL,
    "year" INT   NOT NULL,
    "population_count" INT   NOT NULL,
    CONSTRAINT "pk_population" PRIMARY KEY (
        "population_id"
     )
);

CREATE TABLE "crashes" (
    "crash_id" INT   NOT NULL,
    "crash_lat" DECIMAL   NOT NULL,
    "crash_lng" DECIMAL   NOT NULL,
    "suburb_id" INT   NOT NULL,
    "crash_description" TEXT   NOT NULL,
    CONSTRAINT "pk_crashes" PRIMARY KEY (
        "crash_id"
     )
);

ALTER TABLE "population" ADD CONSTRAINT "fk_population_suburb_id" FOREIGN KEY("suburb_id")
REFERENCES "suburb" ("suburb_id");

ALTER TABLE "crashes" ADD CONSTRAINT "fk_crashes_suburb_id" FOREIGN KEY("suburb_id")
REFERENCES "suburb" ("suburb_id");

