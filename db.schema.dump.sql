--
-- PostgreSQL database dump
--

-- Dumped from database version 9.5.3
-- Dumped by pg_dump version 9.5.3

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: -
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: auth_group; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE auth_group (
    id integer NOT NULL,
    name character varying(80) NOT NULL
);


--
-- Name: auth_group_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE auth_group_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: auth_group_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE auth_group_id_seq OWNED BY auth_group.id;


--
-- Name: auth_group_permissions; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE auth_group_permissions (
    id integer NOT NULL,
    group_id integer NOT NULL,
    permission_id integer NOT NULL
);


--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE auth_group_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE auth_group_permissions_id_seq OWNED BY auth_group_permissions.id;


--
-- Name: auth_permission; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE auth_permission (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    content_type_id integer NOT NULL,
    codename character varying(100) NOT NULL
);


--
-- Name: auth_permission_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE auth_permission_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: auth_permission_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE auth_permission_id_seq OWNED BY auth_permission.id;


--
-- Name: auth_user; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE auth_user (
    id integer NOT NULL,
    password character varying(128) NOT NULL,
    last_login timestamp with time zone,
    is_superuser boolean NOT NULL,
    username character varying(30) NOT NULL,
    first_name character varying(30) NOT NULL,
    last_name character varying(30) NOT NULL,
    email character varying(254) NOT NULL,
    is_staff boolean NOT NULL,
    is_active boolean NOT NULL,
    date_joined timestamp with time zone NOT NULL
);


--
-- Name: auth_user_groups; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE auth_user_groups (
    id integer NOT NULL,
    user_id integer NOT NULL,
    group_id integer NOT NULL
);


--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE auth_user_groups_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE auth_user_groups_id_seq OWNED BY auth_user_groups.id;


--
-- Name: auth_user_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE auth_user_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: auth_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE auth_user_id_seq OWNED BY auth_user.id;


--
-- Name: auth_user_user_permissions; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE auth_user_user_permissions (
    id integer NOT NULL,
    user_id integer NOT NULL,
    permission_id integer NOT NULL
);


--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE auth_user_user_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE auth_user_user_permissions_id_seq OWNED BY auth_user_user_permissions.id;


--
-- Name: authmod_codehash; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE authmod_codehash (
    id integer NOT NULL,
    hash character varying(255) NOT NULL,
    challenge integer NOT NULL,
    responseagent character varying(512),
    requestip character varying(16),
    requestagent character varying(512),
    resolve_status boolean NOT NULL,
    mitigate boolean NOT NULL,
    ts timestamp with time zone NOT NULL
);


--
-- Name: authmod_codehash_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE authmod_codehash_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: authmod_codehash_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE authmod_codehash_id_seq OWNED BY authmod_codehash.id;


--
-- Name: authmod_rawuser; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE authmod_rawuser (
    id integer NOT NULL,
    phone_no character varying(16) NOT NULL,
    attempt integer NOT NULL,
    uastring character varying(512),
    ipaddress character varying(16),
    ts timestamp with time zone
);


--
-- Name: authmod_rawuser_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE authmod_rawuser_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: authmod_rawuser_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE authmod_rawuser_id_seq OWNED BY authmod_rawuser.id;


--
-- Name: common_session; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE common_session (
    sessionid integer NOT NULL,
    uastring character varying(512) NOT NULL,
    ipaddress character varying(16) NOT NULL,
    active boolean NOT NULL,
    start_ts timestamp with time zone NOT NULL,
    end_ts timestamp with time zone NOT NULL,
    user_id integer NOT NULL
);


--
-- Name: common_session_sessionid_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE common_session_sessionid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: common_session_sessionid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE common_session_sessionid_seq OWNED BY common_session.sessionid;


--
-- Name: common_user; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE common_user (
    userid integer NOT NULL,
    dialcode character varying(8) NOT NULL,
    phone bigint NOT NULL,
    countrycode character varying(4) NOT NULL,
    username character varying(16),
    fullname character varying(255),
    account_ts timestamp with time zone NOT NULL,
    update_ts timestamp with time zone NOT NULL
);


--
-- Name: common_user_userid_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE common_user_userid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: common_user_userid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE common_user_userid_seq OWNED BY common_user.userid;


--
-- Name: common_usermobiledevice; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE common_usermobiledevice (
    id integer NOT NULL,
    phoneagent character varying(512) NOT NULL,
    ts timestamp with time zone NOT NULL,
    user_id integer NOT NULL
);


--
-- Name: common_usermobiledevice_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE common_usermobiledevice_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: common_usermobiledevice_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE common_usermobiledevice_id_seq OWNED BY common_usermobiledevice.id;


--
-- Name: contact_contact; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE contact_contact (
    contactid integer NOT NULL,
    contact_name character varying(512) NOT NULL,
    add_ts timestamp with time zone NOT NULL,
    update_ts timestamp with time zone NOT NULL,
    user_id integer NOT NULL
);


--
-- Name: contact_contact_contactid_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE contact_contact_contactid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: contact_contact_contactid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE contact_contact_contactid_seq OWNED BY contact_contact.contactid;


--
-- Name: contact_nativecontact; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE contact_nativecontact (
    id integer NOT NULL,
    contact_id integer NOT NULL,
    contact_user_id integer NOT NULL
);


--
-- Name: contact_nativecontact_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE contact_nativecontact_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: contact_nativecontact_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE contact_nativecontact_id_seq OWNED BY contact_nativecontact.id;


--
-- Name: contact_unregisteredcontact; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE contact_unregisteredcontact (
    id integer NOT NULL,
    contact_phone character varying(18) NOT NULL,
    contact_id integer NOT NULL
);


--
-- Name: contact_unregisteredcontact_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE contact_unregisteredcontact_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: contact_unregisteredcontact_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE contact_unregisteredcontact_id_seq OWNED BY contact_unregisteredcontact.id;


--
-- Name: django_admin_log; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE django_admin_log (
    id integer NOT NULL,
    action_time timestamp with time zone NOT NULL,
    object_id text,
    object_repr character varying(200) NOT NULL,
    action_flag smallint NOT NULL,
    change_message text NOT NULL,
    content_type_id integer,
    user_id integer NOT NULL,
    CONSTRAINT django_admin_log_action_flag_check CHECK ((action_flag >= 0))
);


--
-- Name: django_admin_log_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE django_admin_log_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: django_admin_log_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE django_admin_log_id_seq OWNED BY django_admin_log.id;


--
-- Name: django_content_type; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE django_content_type (
    id integer NOT NULL,
    app_label character varying(100) NOT NULL,
    model character varying(100) NOT NULL
);


--
-- Name: django_content_type_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE django_content_type_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: django_content_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE django_content_type_id_seq OWNED BY django_content_type.id;


--
-- Name: django_migrations; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE django_migrations (
    id integer NOT NULL,
    app character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    applied timestamp with time zone NOT NULL
);


--
-- Name: django_migrations_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE django_migrations_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: django_migrations_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE django_migrations_id_seq OWNED BY django_migrations.id;


--
-- Name: django_session; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE django_session (
    session_key character varying(40) NOT NULL,
    session_data text NOT NULL,
    expire_date timestamp with time zone NOT NULL
);


--
-- Name: file_blinddelivery; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE file_blinddelivery (
    id integer NOT NULL,
    phone character varying(100) NOT NULL,
    status character varying(1) NOT NULL,
    update_ts timestamp with time zone NOT NULL,
    file_id integer NOT NULL
);


--
-- Name: file_blinddelivery_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE file_blinddelivery_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: file_blinddelivery_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE file_blinddelivery_id_seq OWNED BY file_blinddelivery.id;


--
-- Name: file_delivery; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE file_delivery (
    id integer NOT NULL,
    status character varying(1) NOT NULL,
    update_ts timestamp with time zone NOT NULL,
    file_id integer NOT NULL,
    user_id integer NOT NULL
);


--
-- Name: file_delivery_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE file_delivery_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: file_delivery_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE file_delivery_id_seq OWNED BY file_delivery.id;


--
-- Name: file_directunsignedview; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE file_directunsignedview (
    id integer NOT NULL,
    viewer_ip character varying(16) NOT NULL,
    viewer_ua character varying(512) NOT NULL,
    ts timestamp with time zone NOT NULL,
    file_id integer NOT NULL
);


--
-- Name: file_directunsignedview_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE file_directunsignedview_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: file_directunsignedview_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE file_directunsignedview_id_seq OWNED BY file_directunsignedview.id;


--
-- Name: file_file; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE file_file (
    fileid integer NOT NULL,
    filename character varying(255) NOT NULL,
    path character varying(512) NOT NULL,
    size character varying(10) NOT NULL,
    type character varying(255),
    sent_ts timestamp with time zone NOT NULL,
    author_id integer NOT NULL,
    shorturl character varying(8)
);


--
-- Name: file_file_fileid_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE file_file_fileid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: file_file_fileid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE file_file_fileid_seq OWNED BY file_file.fileid;


--
-- Name: home_picture; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE home_picture (
    picid integer NOT NULL,
    large character varying(100) NOT NULL,
    med character varying(100) NOT NULL,
    small character varying(100) NOT NULL,
    active boolean NOT NULL,
    "timestamp" timestamp with time zone NOT NULL,
    user_id integer NOT NULL
);


--
-- Name: home_picture_picid_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE home_picture_picid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: home_picture_picid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE home_picture_picid_seq OWNED BY home_picture.picid;


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY auth_group ALTER COLUMN id SET DEFAULT nextval('auth_group_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY auth_group_permissions ALTER COLUMN id SET DEFAULT nextval('auth_group_permissions_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY auth_permission ALTER COLUMN id SET DEFAULT nextval('auth_permission_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY auth_user ALTER COLUMN id SET DEFAULT nextval('auth_user_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY auth_user_groups ALTER COLUMN id SET DEFAULT nextval('auth_user_groups_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY auth_user_user_permissions ALTER COLUMN id SET DEFAULT nextval('auth_user_user_permissions_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY authmod_codehash ALTER COLUMN id SET DEFAULT nextval('authmod_codehash_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY authmod_rawuser ALTER COLUMN id SET DEFAULT nextval('authmod_rawuser_id_seq'::regclass);


--
-- Name: sessionid; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY common_session ALTER COLUMN sessionid SET DEFAULT nextval('common_session_sessionid_seq'::regclass);


--
-- Name: userid; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY common_user ALTER COLUMN userid SET DEFAULT nextval('common_user_userid_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY common_usermobiledevice ALTER COLUMN id SET DEFAULT nextval('common_usermobiledevice_id_seq'::regclass);


--
-- Name: contactid; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY contact_contact ALTER COLUMN contactid SET DEFAULT nextval('contact_contact_contactid_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY contact_nativecontact ALTER COLUMN id SET DEFAULT nextval('contact_nativecontact_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY contact_unregisteredcontact ALTER COLUMN id SET DEFAULT nextval('contact_unregisteredcontact_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY django_admin_log ALTER COLUMN id SET DEFAULT nextval('django_admin_log_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY django_content_type ALTER COLUMN id SET DEFAULT nextval('django_content_type_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY django_migrations ALTER COLUMN id SET DEFAULT nextval('django_migrations_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY file_blinddelivery ALTER COLUMN id SET DEFAULT nextval('file_blinddelivery_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY file_delivery ALTER COLUMN id SET DEFAULT nextval('file_delivery_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY file_directunsignedview ALTER COLUMN id SET DEFAULT nextval('file_directunsignedview_id_seq'::regclass);


--
-- Name: fileid; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY file_file ALTER COLUMN fileid SET DEFAULT nextval('file_file_fileid_seq'::regclass);


--
-- Name: picid; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY home_picture ALTER COLUMN picid SET DEFAULT nextval('home_picture_picid_seq'::regclass);


--
-- Name: auth_group_name_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY auth_group
    ADD CONSTRAINT auth_group_name_key UNIQUE (name);


--
-- Name: auth_group_permissions_group_id_0cd325b0_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_0cd325b0_uniq UNIQUE (group_id, permission_id);


--
-- Name: auth_group_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_group_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY auth_group
    ADD CONSTRAINT auth_group_pkey PRIMARY KEY (id);


--
-- Name: auth_permission_content_type_id_01ab375a_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_01ab375a_uniq UNIQUE (content_type_id, codename);


--
-- Name: auth_permission_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY auth_permission
    ADD CONSTRAINT auth_permission_pkey PRIMARY KEY (id);


--
-- Name: auth_user_groups_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY auth_user_groups
    ADD CONSTRAINT auth_user_groups_pkey PRIMARY KEY (id);


--
-- Name: auth_user_groups_user_id_94350c0c_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_94350c0c_uniq UNIQUE (user_id, group_id);


--
-- Name: auth_user_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY auth_user
    ADD CONSTRAINT auth_user_pkey PRIMARY KEY (id);


--
-- Name: auth_user_user_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_user_user_permissions_user_id_14a6b632_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_user_id_14a6b632_uniq UNIQUE (user_id, permission_id);


--
-- Name: auth_user_username_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY auth_user
    ADD CONSTRAINT auth_user_username_key UNIQUE (username);


--
-- Name: authmod_codehash_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY authmod_codehash
    ADD CONSTRAINT authmod_codehash_pkey PRIMARY KEY (id);


--
-- Name: authmod_rawuser_phone_no_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY authmod_rawuser
    ADD CONSTRAINT authmod_rawuser_phone_no_key UNIQUE (phone_no);


--
-- Name: authmod_rawuser_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY authmod_rawuser
    ADD CONSTRAINT authmod_rawuser_pkey PRIMARY KEY (id);


--
-- Name: common_session_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY common_session
    ADD CONSTRAINT common_session_pkey PRIMARY KEY (sessionid);


--
-- Name: common_user_dialcode_316ca2cf_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY common_user
    ADD CONSTRAINT common_user_dialcode_316ca2cf_uniq UNIQUE (dialcode, phone);


--
-- Name: common_user_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY common_user
    ADD CONSTRAINT common_user_pkey PRIMARY KEY (userid);


--
-- Name: common_user_username_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY common_user
    ADD CONSTRAINT common_user_username_key UNIQUE (username);


--
-- Name: common_usermobiledevice_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY common_usermobiledevice
    ADD CONSTRAINT common_usermobiledevice_pkey PRIMARY KEY (id);


--
-- Name: contact_contact_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY contact_contact
    ADD CONSTRAINT contact_contact_pkey PRIMARY KEY (contactid);


--
-- Name: contact_nativecontact_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY contact_nativecontact
    ADD CONSTRAINT contact_nativecontact_pkey PRIMARY KEY (id);


--
-- Name: contact_unregisteredcontact_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY contact_unregisteredcontact
    ADD CONSTRAINT contact_unregisteredcontact_pkey PRIMARY KEY (id);


--
-- Name: django_admin_log_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY django_admin_log
    ADD CONSTRAINT django_admin_log_pkey PRIMARY KEY (id);


--
-- Name: django_content_type_app_label_76bd3d3b_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY django_content_type
    ADD CONSTRAINT django_content_type_app_label_76bd3d3b_uniq UNIQUE (app_label, model);


--
-- Name: django_content_type_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY django_content_type
    ADD CONSTRAINT django_content_type_pkey PRIMARY KEY (id);


--
-- Name: django_migrations_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY django_migrations
    ADD CONSTRAINT django_migrations_pkey PRIMARY KEY (id);


--
-- Name: django_session_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY django_session
    ADD CONSTRAINT django_session_pkey PRIMARY KEY (session_key);


--
-- Name: file_blinddelivery_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY file_blinddelivery
    ADD CONSTRAINT file_blinddelivery_pkey PRIMARY KEY (id);


--
-- Name: file_delivery_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY file_delivery
    ADD CONSTRAINT file_delivery_pkey PRIMARY KEY (id);


--
-- Name: file_directunsignedview_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY file_directunsignedview
    ADD CONSTRAINT file_directunsignedview_pkey PRIMARY KEY (id);


--
-- Name: file_file_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY file_file
    ADD CONSTRAINT file_file_pkey PRIMARY KEY (fileid);


--
-- Name: file_file_shorturl_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY file_file
    ADD CONSTRAINT file_file_shorturl_key UNIQUE (shorturl);


--
-- Name: home_picture_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY home_picture
    ADD CONSTRAINT home_picture_pkey PRIMARY KEY (picid);


--
-- Name: auth_group_name_a6ea08ec_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX auth_group_name_a6ea08ec_like ON auth_group USING btree (name varchar_pattern_ops);


--
-- Name: auth_group_permissions_0e939a4f; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX auth_group_permissions_0e939a4f ON auth_group_permissions USING btree (group_id);


--
-- Name: auth_group_permissions_8373b171; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX auth_group_permissions_8373b171 ON auth_group_permissions USING btree (permission_id);


--
-- Name: auth_permission_417f1b1c; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX auth_permission_417f1b1c ON auth_permission USING btree (content_type_id);


--
-- Name: auth_user_groups_0e939a4f; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX auth_user_groups_0e939a4f ON auth_user_groups USING btree (group_id);


--
-- Name: auth_user_groups_e8701ad4; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX auth_user_groups_e8701ad4 ON auth_user_groups USING btree (user_id);


--
-- Name: auth_user_user_permissions_8373b171; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX auth_user_user_permissions_8373b171 ON auth_user_user_permissions USING btree (permission_id);


--
-- Name: auth_user_user_permissions_e8701ad4; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX auth_user_user_permissions_e8701ad4 ON auth_user_user_permissions USING btree (user_id);


--
-- Name: auth_user_username_6821ab7c_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX auth_user_username_6821ab7c_like ON auth_user USING btree (username varchar_pattern_ops);


--
-- Name: authmod_rawuser_phone_no_8d52c22b_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX authmod_rawuser_phone_no_8d52c22b_like ON authmod_rawuser USING btree (phone_no varchar_pattern_ops);


--
-- Name: common_session_e8701ad4; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX common_session_e8701ad4 ON common_session USING btree (user_id);


--
-- Name: common_user_username_01dcd042_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX common_user_username_01dcd042_like ON common_user USING btree (username varchar_pattern_ops);


--
-- Name: common_usermobiledevice_e8701ad4; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX common_usermobiledevice_e8701ad4 ON common_usermobiledevice USING btree (user_id);


--
-- Name: contact_contact_e8701ad4; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX contact_contact_e8701ad4 ON contact_contact USING btree (user_id);


--
-- Name: contact_nativecontact_29df0c81; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX contact_nativecontact_29df0c81 ON contact_nativecontact USING btree (contact_user_id);


--
-- Name: contact_nativecontact_6d82f13d; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX contact_nativecontact_6d82f13d ON contact_nativecontact USING btree (contact_id);


--
-- Name: contact_unregisteredcontact_6d82f13d; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX contact_unregisteredcontact_6d82f13d ON contact_unregisteredcontact USING btree (contact_id);


--
-- Name: django_admin_log_417f1b1c; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX django_admin_log_417f1b1c ON django_admin_log USING btree (content_type_id);


--
-- Name: django_admin_log_e8701ad4; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX django_admin_log_e8701ad4 ON django_admin_log USING btree (user_id);


--
-- Name: django_session_de54fa62; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX django_session_de54fa62 ON django_session USING btree (expire_date);


--
-- Name: django_session_session_key_c0390e0f_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX django_session_session_key_c0390e0f_like ON django_session USING btree (session_key varchar_pattern_ops);


--
-- Name: file_blinddelivery_814552b9; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX file_blinddelivery_814552b9 ON file_blinddelivery USING btree (file_id);


--
-- Name: file_delivery_814552b9; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX file_delivery_814552b9 ON file_delivery USING btree (file_id);


--
-- Name: file_delivery_e8701ad4; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX file_delivery_e8701ad4 ON file_delivery USING btree (user_id);


--
-- Name: file_directunsignedview_814552b9; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX file_directunsignedview_814552b9 ON file_directunsignedview USING btree (file_id);


--
-- Name: file_file_4f331e2f; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX file_file_4f331e2f ON file_file USING btree (author_id);


--
-- Name: home_picture_e8701ad4; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX home_picture_e8701ad4 ON home_picture USING btree (user_id);


--
-- Name: auth_group_permiss_permission_id_84c5c92e_fk_auth_permission_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY auth_group_permissions
    ADD CONSTRAINT auth_group_permiss_permission_id_84c5c92e_fk_auth_permission_id FOREIGN KEY (permission_id) REFERENCES auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_group_permissions_group_id_b120cbf9_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_b120cbf9_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_permiss_content_type_id_2f476e4b_fk_django_content_type_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY auth_permission
    ADD CONSTRAINT auth_permiss_content_type_id_2f476e4b_fk_django_content_type_id FOREIGN KEY (content_type_id) REFERENCES django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_groups_group_id_97559544_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY auth_user_groups
    ADD CONSTRAINT auth_user_groups_group_id_97559544_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_groups_user_id_6a12ed8b_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_6a12ed8b_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_user_per_permission_id_1fbb5f2c_fk_auth_permission_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_per_permission_id_1fbb5f2c_fk_auth_permission_id FOREIGN KEY (permission_id) REFERENCES auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: common_session_user_id_d0b8f3f7_fk_common_user_userid; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY common_session
    ADD CONSTRAINT common_session_user_id_d0b8f3f7_fk_common_user_userid FOREIGN KEY (user_id) REFERENCES common_user(userid) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: common_usermobiledevice_user_id_e5c29755_fk_common_user_userid; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY common_usermobiledevice
    ADD CONSTRAINT common_usermobiledevice_user_id_e5c29755_fk_common_user_userid FOREIGN KEY (user_id) REFERENCES common_user(userid) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: contact_contact_user_id_2e02db50_fk_common_user_userid; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY contact_contact
    ADD CONSTRAINT contact_contact_user_id_2e02db50_fk_common_user_userid FOREIGN KEY (user_id) REFERENCES common_user(userid) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: contact_native_contact_id_ad6982f7_fk_contact_contact_contactid; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY contact_nativecontact
    ADD CONSTRAINT contact_native_contact_id_ad6982f7_fk_contact_contact_contactid FOREIGN KEY (contact_id) REFERENCES contact_contact(contactid) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: contact_nativeco_contact_user_id_0f91ab11_fk_common_user_userid; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY contact_nativecontact
    ADD CONSTRAINT contact_nativeco_contact_user_id_0f91ab11_fk_common_user_userid FOREIGN KEY (contact_user_id) REFERENCES common_user(userid) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: contact_unregi_contact_id_cfd1eb11_fk_contact_contact_contactid; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY contact_unregisteredcontact
    ADD CONSTRAINT contact_unregi_contact_id_cfd1eb11_fk_contact_contact_contactid FOREIGN KEY (contact_id) REFERENCES contact_contact(contactid) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_content_type_id_c4bce8eb_fk_django_content_type_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY django_admin_log
    ADD CONSTRAINT django_admin_content_type_id_c4bce8eb_fk_django_content_type_id FOREIGN KEY (content_type_id) REFERENCES django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log_user_id_c564eba6_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY django_admin_log
    ADD CONSTRAINT django_admin_log_user_id_c564eba6_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: file_blinddelivery_file_id_a088608f_fk_file_file_fileid; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY file_blinddelivery
    ADD CONSTRAINT file_blinddelivery_file_id_a088608f_fk_file_file_fileid FOREIGN KEY (file_id) REFERENCES file_file(fileid) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: file_delivery_file_id_d3579bb2_fk_file_file_fileid; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY file_delivery
    ADD CONSTRAINT file_delivery_file_id_d3579bb2_fk_file_file_fileid FOREIGN KEY (file_id) REFERENCES file_file(fileid) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: file_delivery_user_id_c1f72e46_fk_common_user_userid; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY file_delivery
    ADD CONSTRAINT file_delivery_user_id_c1f72e46_fk_common_user_userid FOREIGN KEY (user_id) REFERENCES common_user(userid) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: file_directunsignedview_file_id_a3327789_fk_file_file_fileid; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY file_directunsignedview
    ADD CONSTRAINT file_directunsignedview_file_id_a3327789_fk_file_file_fileid FOREIGN KEY (file_id) REFERENCES file_file(fileid) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: file_file_author_id_a4f60ca6_fk_common_user_userid; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY file_file
    ADD CONSTRAINT file_file_author_id_a4f60ca6_fk_common_user_userid FOREIGN KEY (author_id) REFERENCES common_user(userid) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: home_picture_user_id_9a62c910_fk_common_user_userid; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY home_picture
    ADD CONSTRAINT home_picture_user_id_9a62c910_fk_common_user_userid FOREIGN KEY (user_id) REFERENCES common_user(userid) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: public; Type: ACL; Schema: -; Owner: -
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--

