--
-- PostgreSQL database dump
--

-- Dumped from database version 9.6.9
-- Dumped by pg_dump version 9.6.9

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner:
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner:
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: mgallery
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO mgallery;

--
-- Name: gallery; Type: TABLE; Schema: public; Owner: mgallery
--

CREATE TABLE public.gallery (
    id integer NOT NULL,
    path character varying,
    date date,
    name character varying,
    year smallint
);


ALTER TABLE public.gallery OWNER TO mgallery;

--
-- Name: gallery_id_seq; Type: SEQUENCE; Schema: public; Owner: mgallery
--

CREATE SEQUENCE public.gallery_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.gallery_id_seq OWNER TO mgallery;

--
-- Name: gallery_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: mgallery
--

ALTER SEQUENCE public.gallery_id_seq OWNED BY public.gallery.id;


--
-- Name: image; Type: TABLE; Schema: public; Owner: mgallery
--

CREATE TABLE public.image (
    id integer NOT NULL,
    path character varying,
    phash character varying,
    gallery_id integer,
    camera character varying,
    datetime timestamp without time zone,
    lens character varying,
    location character varying
);


ALTER TABLE public.image OWNER TO mgallery;

--
-- Name: image_id_seq; Type: SEQUENCE; Schema: public; Owner: mgallery
--

CREATE SEQUENCE public.image_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.image_id_seq OWNER TO mgallery;

--
-- Name: image_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: mgallery
--

ALTER SEQUENCE public.image_id_seq OWNED BY public.image.id;


--
-- Name: gallery id; Type: DEFAULT; Schema: public; Owner: mgallery
--

ALTER TABLE ONLY public.gallery ALTER COLUMN id SET DEFAULT nextval('public.gallery_id_seq'::regclass);


--
-- Name: image id; Type: DEFAULT; Schema: public; Owner: mgallery
--

ALTER TABLE ONLY public.image ALTER COLUMN id SET DEFAULT nextval('public.image_id_seq'::regclass);


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: mgallery
--

COPY public.alembic_version (version_num) FROM stdin;
0fe7cf51bacc
\.


--
-- Data for Name: gallery; Type: TABLE DATA; Schema: public; Owner: mgallery
--


--
-- Name: gallery_id_seq; Type: SEQUENCE SET; Schema: public; Owner: mgallery
--

SELECT pg_catalog.setval('public.gallery_id_seq', 1, true);


--
-- Data for Name: image; Type: TABLE DATA; Schema: public; Owner: mgallery
--


--
-- Name: image_id_seq; Type: SEQUENCE SET; Schema: public; Owner: mgallery
--

SELECT pg_catalog.setval('public.image_id_seq', 1, true);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: mgallery
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: gallery gallery_pkey; Type: CONSTRAINT; Schema: public; Owner: mgallery
--

ALTER TABLE ONLY public.gallery
    ADD CONSTRAINT gallery_pkey PRIMARY KEY (id);


--
-- Name: image image_pkey; Type: CONSTRAINT; Schema: public; Owner: mgallery
--

ALTER TABLE ONLY public.image
    ADD CONSTRAINT image_pkey PRIMARY KEY (id);


--
-- Name: image image_gallery_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: mgallery
--

ALTER TABLE ONLY public.image
    ADD CONSTRAINT image_gallery_id_fkey FOREIGN KEY (gallery_id) REFERENCES public.gallery(id);


--
-- PostgreSQL database dump complete
--