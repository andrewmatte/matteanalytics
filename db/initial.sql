CREATE DATABASE mattean;
\c mattean

CREATE TABLE events (
    who varchar,
    document varchar,
    timewhen timestamp with time zone default now(),
    referrer varchar
);

CREATE TABLE accounts (
    id SERIAL,
    email varchar unique,
    salt varchar,
    hashed_salted_password varchar,
    created_time timestamp with time zone default now()
);

CREATE TABLE sessions (
    user_id bigint,
    expires_at timestamp with time zone default now() + interval '8 hours',
    access_token varchar
);

CREATE TABLE sites (
    user_id bigint,
    full_domain varchar,
    verification_token varchar,
    verified boolean
);

