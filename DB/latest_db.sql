--
-- PostgreSQL database dump
--

-- Dumped from database version 14.3
-- Dumped by pg_dump version 14.3

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
-- Name: autotest; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA autotest;


ALTER SCHEMA autotest OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: tests_registration; Type: TABLE; Schema: autotest; Owner: postgres
--

CREATE TABLE autotest.tests_registration (
    id integer NOT NULL,
    start_timestamp timestamp with time zone NOT NULL,
    end_timestamp timestamp with time zone NOT NULL,
    status smallint NOT NULL,
    author character varying(250) NOT NULL
);


ALTER TABLE autotest.tests_registration OWNER TO postgres;

--
-- Name: tests_registration_id_seq; Type: SEQUENCE; Schema: autotest; Owner: postgres
--

CREATE SEQUENCE autotest.tests_registration_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE autotest.tests_registration_id_seq OWNER TO postgres;

--
-- Name: tests_registration_id_seq; Type: SEQUENCE OWNED BY; Schema: autotest; Owner: postgres
--

ALTER SEQUENCE autotest.tests_registration_id_seq OWNED BY autotest.tests_registration.id;


--
-- Name: user_info; Type: TABLE; Schema: autotest; Owner: postgres
--

CREATE TABLE autotest.user_info (
    id integer NOT NULL,
    username character varying(250) NOT NULL,
    role character varying(20) NOT NULL
);


ALTER TABLE autotest.user_info OWNER TO postgres;

--
-- Name: user_info_id_seq; Type: SEQUENCE; Schema: autotest; Owner: postgres
--

CREATE SEQUENCE autotest.user_info_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE autotest.user_info_id_seq OWNER TO postgres;

--
-- Name: user_info_id_seq; Type: SEQUENCE OWNED BY; Schema: autotest; Owner: postgres
--

ALTER SEQUENCE autotest.user_info_id_seq OWNED BY autotest.user_info.id;


--
-- Name: tests_registration id; Type: DEFAULT; Schema: autotest; Owner: postgres
--

ALTER TABLE ONLY autotest.tests_registration ALTER COLUMN id SET DEFAULT nextval('autotest.tests_registration_id_seq'::regclass);


--
-- Name: user_info id; Type: DEFAULT; Schema: autotest; Owner: postgres
--

ALTER TABLE ONLY autotest.user_info ALTER COLUMN id SET DEFAULT nextval('autotest.user_info_id_seq'::regclass);


--
-- Data for Name: tests_registration; Type: TABLE DATA; Schema: autotest; Owner: postgres
--

COPY autotest.tests_registration (id, start_timestamp, end_timestamp, status, author) FROM stdin;
14	2022-07-14 11:02:00+07	2022-07-15 11:02:00+07	1	huynq
12	2022-07-07 10:58:00+07	2022-07-08 10:58:00+07	0	huynq
15	2022-07-19 11:08:00+07	2022-07-20 11:08:00+07	1	hungle
16	2022-07-06 11:12:00+07	2022-07-07 11:12:00+07	1	hungle
13	2022-07-12 11:00:00+07	2022-07-13 11:00:00+07	0	huynq
18	2022-07-09 14:27:00+07	2022-07-10 14:27:00+07	0	hungle
17	2022-07-07 11:13:00+07	2022-07-08 11:13:00+07	1	huynq
19	2022-07-21 15:04:00+07	2022-07-22 15:04:00+07	1	huynq
20	2022-07-09 16:43:00+07	2022-07-10 16:43:00+07	1	huynq
\.


--
-- Data for Name: user_info; Type: TABLE DATA; Schema: autotest; Owner: postgres
--

COPY autotest.user_info (id, username, role) FROM stdin;
\.


--
-- Name: tests_registration_id_seq; Type: SEQUENCE SET; Schema: autotest; Owner: postgres
--

SELECT pg_catalog.setval('autotest.tests_registration_id_seq', 20, true);


--
-- Name: user_info_id_seq; Type: SEQUENCE SET; Schema: autotest; Owner: postgres
--

SELECT pg_catalog.setval('autotest.user_info_id_seq', 1, false);


--
-- Name: tests_registration tests_registration_pkey; Type: CONSTRAINT; Schema: autotest; Owner: postgres
--

ALTER TABLE ONLY autotest.tests_registration
    ADD CONSTRAINT tests_registration_pkey PRIMARY KEY (id);


--
-- Name: user_info user_info_pkey; Type: CONSTRAINT; Schema: autotest; Owner: postgres
--

ALTER TABLE ONLY autotest.user_info
    ADD CONSTRAINT user_info_pkey PRIMARY KEY (id);


--
-- Name: user_info user_info_username_key; Type: CONSTRAINT; Schema: autotest; Owner: postgres
--

ALTER TABLE ONLY autotest.user_info
    ADD CONSTRAINT user_info_username_key UNIQUE (username);


--
-- Name: SCHEMA autotest; Type: ACL; Schema: -; Owner: postgres
--

GRANT ALL ON SCHEMA autotest TO PUBLIC;


--
-- PostgreSQL database dump complete
--

