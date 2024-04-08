create table public."activities"
(
    activity_id integer not null,
    activity_name character varying(45) not null,
    last_update timestamp without time zone not null default now(),
    primary key (activity_id)
);

alter table if exists public."activities" owner to postgres;