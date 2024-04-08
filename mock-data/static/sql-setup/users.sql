create table public.users
(
    user_id integer not null,
    first_name character varying not null,
    last_name character varying not null,
    date_of_birth integer not null,
    sex character varying(1),
    height smallint,
    weight smallint,
    blood_type character varying(3),
    race character varying(1),
    origin_country_code character varying(2),
    origin_country_name character varying(45),
    address character varying(100) not null,
    address_country_code character varying(2) not null,
    address_country_name character varying(45) not null,
    last_update timestamp without time zone not null default now(),
    primary key (user_id)
);

alter table if exists public.users owner to postgres;