CREATE TABLE "plannedLesson" (
  "id" int,
  "name" varchar,
  "timestart" datetime,
  "timeend" datetime,
  "student_id" int,
  "teacher_id" int,
  "event_id" int,
  "location_id" int
);

CREATE TABLE "location" (
  "id" int,
  "building" varchar,
  "room" varchar
);

CREATE TABLE "event" (
  "id" int,
  "type" varchar
);

CREATE TABLE "student" (
  "id" int,
  "firstname" varchar,
  "lastname" varchar,
  "age" int,
  "gender" char,
  "group_id" int
);

CREATE TABLE "groupstudent" (
  "id" int,
  "name" varchar
);

CREATE TABLE "teacher" (
  "id" int,
  "firstname" varchar,
  "lastname" varchar,
  "age" int,
  "gender" char,
  "subject_id" int
);

CREATE TABLE "subject" (
  "id" int,
  "name" varchar,
  "topics" list
);

ALTER TABLE "plannedLesson" ADD FOREIGN KEY ("student_id") REFERENCES "student" ("id");

ALTER TABLE "plannedLesson" ADD FOREIGN KEY ("teacher_id") REFERENCES "teacher" ("id");

ALTER TABLE "plannedLesson" ADD FOREIGN KEY ("event_id") REFERENCES "event" ("id");

ALTER TABLE "plannedLesson" ADD FOREIGN KEY ("location_id") REFERENCES "location" ("id");

ALTER TABLE "student" ADD FOREIGN KEY ("group_id") REFERENCES "groupstudent" ("id");

ALTER TABLE "teacher" ADD FOREIGN KEY ("subject_id") REFERENCES "subject" ("id");
