-- CDC set up script on PostgreSQL (run the queries against the database where the respective tables are stored).

-- 1: ensure logical replication has been turned on
select name, setting from pg_settings where name in ('wal_level', 'rds.logical_replication');

-- 2: create replication slot for db
select pg_create_logical_replication_slot('airbyte_slot', 'pgoutput');

-- 3: ensure replication slot has been created
select * from pg_replication_slots;

-- 4: check publication tables in db (should be empty)
select * from pg_publication_tables;

-- 5: add the replication identity for each table in db
alter table users replica identity default;
alter table activities replica identity default;

-- 6. create the postgres publication for all tables in db
create publication airbyte_publication for table users, activities;

-- 7: check again the publication tables in db (should have 15 rows)
select * from pg_publication_tables;