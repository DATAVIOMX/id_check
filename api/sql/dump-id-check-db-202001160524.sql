--
-- PostgreSQL database dump
--

-- Dumped from database version 12.1
-- Dumped by pg_dump version 12.1

-- Started on 2020-01-16 05:24:46 CST

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 3 (class 2615 OID 2200)
-- Name: public; Type: SCHEMA; Schema: -; Owner: ohh
--

CREATE SCHEMA public;


ALTER SCHEMA public OWNER TO ohh;

--
-- TOC entry 3203 (class 0 OID 0)
-- Dependencies: 3
-- Name: SCHEMA public; Type: COMMENT; Schema: -; Owner: ohh
--

COMMENT ON SCHEMA public IS 'standard public schema';


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 204 (class 1259 OID 18607)
-- Name: api_calls; Type: TABLE; Schema: public; Owner: ohh
--

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


ALTER TABLE public.api_calls OWNER TO ohh;

--
-- TOC entry 203 (class 1259 OID 18605)
-- Name: api_calls_callid_seq; Type: SEQUENCE; Schema: public; Owner: ohh
--

CREATE SEQUENCE public.api_calls_callid_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.api_calls_callid_seq OWNER TO ohh;

--
-- TOC entry 3204 (class 0 OID 0)
-- Dependencies: 203
-- Name: api_calls_callid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: ohh
--

ALTER SEQUENCE public.api_calls_callid_seq OWNED BY public.api_calls.callid;


--
-- TOC entry 202 (class 1259 OID 18597)
-- Name: users; Type: TABLE; Schema: public; Owner: ohh
--

CREATE TABLE public.users (
    userid uuid NOT NULL,
    creation_date timestamp without time zone,
    update_date timestamp without time zone,
    status integer,
    api_key text,
    api_key_exp_date timestamp without time zone,
    calls_remaining integer
);


ALTER TABLE public.users OWNER TO ohh;

--
-- TOC entry 3063 (class 2604 OID 18610)
-- Name: api_calls callid; Type: DEFAULT; Schema: public; Owner: ohh
--

ALTER TABLE ONLY public.api_calls ALTER COLUMN callid SET DEFAULT nextval('public.api_calls_callid_seq'::regclass);


--
-- TOC entry 3197 (class 0 OID 18607)
-- Dependencies: 204
-- Data for Name: api_calls; Type: TABLE DATA; Schema: public; Owner: ohh
--

COPY public.api_calls (callid, userid, api_key, call_date, call_point, status_code, call_text, response) FROM stdin;
\.


--
-- TOC entry 3195 (class 0 OID 18597)
-- Dependencies: 202
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: ohh
--

COPY public.users (userid, creation_date, update_date, status, api_key, api_key_exp_date, calls_remaining) FROM stdin;
\.


--
-- TOC entry 3205 (class 0 OID 0)
-- Dependencies: 203
-- Name: api_calls_callid_seq; Type: SEQUENCE SET; Schema: public; Owner: ohh
--

SELECT pg_catalog.setval('public.api_calls_callid_seq', 1, false);


--
-- TOC entry 3067 (class 2606 OID 18615)
-- Name: api_calls api_calls_pkey; Type: CONSTRAINT; Schema: public; Owner: ohh
--

ALTER TABLE ONLY public.api_calls
    ADD CONSTRAINT api_calls_pkey PRIMARY KEY (callid);


--
-- TOC entry 3065 (class 2606 OID 18604)
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: ohh
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (userid);


--
-- TOC entry 3068 (class 2606 OID 18616)
-- Name: api_calls api_calls_userid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: ohh
--

ALTER TABLE ONLY public.api_calls
    ADD CONSTRAINT api_calls_userid_fkey FOREIGN KEY (userid) REFERENCES public.users(userid);


-- Completed on 2020-01-16 05:24:46 CST

--
-- PostgreSQL database dump complete
--

