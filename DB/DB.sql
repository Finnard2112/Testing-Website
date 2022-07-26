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
-- Name: groups; Type: TABLE; Schema: autotest; Owner: postgres
--

CREATE TABLE autotest.groups (
    id integer NOT NULL,
    name character varying,
    type character varying,
    username character varying
);


ALTER TABLE autotest.groups OWNER TO postgres;

--
-- Name: groups_id_seq; Type: SEQUENCE; Schema: autotest; Owner: postgres
--

CREATE SEQUENCE autotest.groups_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE autotest.groups_id_seq OWNER TO postgres;

--
-- Name: groups_id_seq; Type: SEQUENCE OWNED BY; Schema: autotest; Owner: postgres
--

ALTER SEQUENCE autotest.groups_id_seq OWNED BY autotest.groups.id;


--
-- Name: tests; Type: TABLE; Schema: autotest; Owner: postgres
--

CREATE TABLE autotest.tests (
    id integer NOT NULL,
    groupid integer,
    test_name character varying,
    status character varying,
    message character varying,
    description character varying
);


ALTER TABLE autotest.tests OWNER TO postgres;

--
-- Name: tests_id_seq; Type: SEQUENCE; Schema: autotest; Owner: postgres
--

CREATE SEQUENCE autotest.tests_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE autotest.tests_id_seq OWNER TO postgres;

--
-- Name: tests_id_seq; Type: SEQUENCE OWNED BY; Schema: autotest; Owner: postgres
--

ALTER SEQUENCE autotest.tests_id_seq OWNED BY autotest.tests.id;


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
-- Name: groups id; Type: DEFAULT; Schema: autotest; Owner: postgres
--

ALTER TABLE ONLY autotest.groups ALTER COLUMN id SET DEFAULT nextval('autotest.groups_id_seq'::regclass);


--
-- Name: tests id; Type: DEFAULT; Schema: autotest; Owner: postgres
--

ALTER TABLE ONLY autotest.tests ALTER COLUMN id SET DEFAULT nextval('autotest.tests_id_seq'::regclass);


--
-- Name: tests_registration id; Type: DEFAULT; Schema: autotest; Owner: postgres
--

ALTER TABLE ONLY autotest.tests_registration ALTER COLUMN id SET DEFAULT nextval('autotest.tests_registration_id_seq'::regclass);


--
-- Name: user_info id; Type: DEFAULT; Schema: autotest; Owner: postgres
--

ALTER TABLE ONLY autotest.user_info ALTER COLUMN id SET DEFAULT nextval('autotest.user_info_id_seq'::regclass);


--
-- Data for Name: groups; Type: TABLE DATA; Schema: autotest; Owner: postgres
--

COPY autotest.groups (id, name, type, username) FROM stdin;
1	Test Group	api	huynq
2	huynq group	api	huynq
\.


--
-- Data for Name: tests; Type: TABLE DATA; Schema: autotest; Owner: postgres
--

COPY autotest.tests (id, groupid, test_name, status, message, description) FROM stdin;
4	1	STT1	Ready	success	hello
5	1	TTS1	Ready	success	hello
6	1	IBeta1	Ready	success	hello
7	1	STT2	Ready	success	hello
8	1	TTS2	Ready	success	tss2
\.


--
-- Data for Name: tests_registration; Type: TABLE DATA; Schema: autotest; Owner: postgres
--

COPY autotest.tests_registration (id, start_timestamp, end_timestamp, status, author) FROM stdin;
1	2022-07-29 09:08:00+07	2022-07-30 09:09:00+07	1	huynq
2	2022-07-22 09:39:00+07	2022-07-23 09:39:00+07	1	huynq
3	2022-07-25 09:45:00+07	2022-07-26 09:45:00+07	1	huynq
\.


--
-- Data for Name: user_info; Type: TABLE DATA; Schema: autotest; Owner: postgres
--

COPY autotest.user_info (id, username, role) FROM stdin;
\.


--
-- Name: groups_id_seq; Type: SEQUENCE SET; Schema: autotest; Owner: postgres
--

SELECT pg_catalog.setval('autotest.groups_id_seq', 2, true);


--
-- Name: tests_id_seq; Type: SEQUENCE SET; Schema: autotest; Owner: postgres
--

SELECT pg_catalog.setval('autotest.tests_id_seq', 8, true);


--
-- Name: tests_registration_id_seq; Type: SEQUENCE SET; Schema: autotest; Owner: postgres
--

SELECT pg_catalog.setval('autotest.tests_registration_id_seq', 3, true);


--
-- Name: user_info_id_seq; Type: SEQUENCE SET; Schema: autotest; Owner: postgres
--

SELECT pg_catalog.setval('autotest.user_info_id_seq', 1, false);


--
-- Name: groups groups_pkey; Type: CONSTRAINT; Schema: autotest; Owner: postgres
--

ALTER TABLE ONLY autotest.groups
    ADD CONSTRAINT groups_pkey PRIMARY KEY (id);


--
-- Name: tests tests_pkey; Type: CONSTRAINT; Schema: autotest; Owner: postgres
--

ALTER TABLE ONLY autotest.tests
    ADD CONSTRAINT tests_pkey PRIMARY KEY (id);


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
-- Name: tests tests_groupid_fkey; Type: FK CONSTRAINT; Schema: autotest; Owner: postgres
--

ALTER TABLE ONLY autotest.tests
    ADD CONSTRAINT tests_groupid_fkey FOREIGN KEY (groupid) REFERENCES autotest.groups(id);


--
-- Name: SCHEMA autotest; Type: ACL; Schema: -; Owner: postgres
--

GRANT ALL ON SCHEMA autotest TO PUBLIC;


--
-- PostgreSQL database dump complete
--

