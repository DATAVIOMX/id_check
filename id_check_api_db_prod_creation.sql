/*
PURPOSE: Tables for production in PostgreSQL this changes the integer IDs for
UUIDs and the format for the dates.
AUTHOR: Otto Hahn
*/


CREATE TABLE public.users (
    userid uuid NOT NULL,
    creation_date timestamp without time zone,
    update_date timestamp without time zone,
    status integer,
    api_key text,
    api_key_exp_date timestamp without time zone,
    calls_remaining integer
);

CREATE TABLE public.api_calls (
    callid integer NOT NULL,
    userid uuid,
    api_key text,
    call_date timestamp without time zone,
    call_point text,
    status_code text,
    call_text json,
    response json
);


