/*
PURPOSE: Tables for production in PostgreSQL this changes the integer IDs for
UUIDs and the format for the dates.
AUTHOR: Otto Hahn
*/

/* Extensions */
create extension pgcrypto;
create extension chkpass;

/* Table definitions */

CREATE TABLE users (
    userid uuid primary key,
    creation_date timestamp without time zone,
    update_date timestamp without time zone,
    status integer,
    api_key chkpass,
    api_key_exp_date timestamp without time zone,
    calls_remaining integer
);

CREATE TABLE api_calls (
    callid integer NOT NULL,
    userid uuid references users(userid),
    call_date timestamp without time zone,
    call_point text,
    status_code text,
    call_text bytea,
    response bytea
    
);


