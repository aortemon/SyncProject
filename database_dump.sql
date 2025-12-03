--
-- PostgreSQL database dump
--

\restrict IpgjqXGjGyk13W3QbRRsVkP6Lz9tmYcNbUG0Npbvidaz7g2egdRhTLBEwISnG6c

-- Dumped from database version 16.10 (Ubuntu 16.10-0ubuntu0.24.04.1)
-- Dumped by pg_dump version 16.10 (Ubuntu 16.10-0ubuntu0.24.04.1)

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

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO admin;

--
-- Name: departments; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.departments (
    id integer NOT NULL,
    name character varying(256) NOT NULL,
    lead_id integer NOT NULL
);


ALTER TABLE public.departments OWNER TO admin;

--
-- Name: departments_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.departments_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.departments_id_seq OWNER TO admin;

--
-- Name: departments_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.departments_id_seq OWNED BY public.departments.id;


--
-- Name: employeedepartments; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.employeedepartments (
    department_id integer NOT NULL,
    employee_id integer NOT NULL,
    office character varying(256) NOT NULL
);


ALTER TABLE public.employeedepartments OWNER TO admin;

--
-- Name: employeemeetings; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.employeemeetings (
    meeting_id integer NOT NULL,
    employee_id integer NOT NULL
);


ALTER TABLE public.employeemeetings OWNER TO admin;

--
-- Name: employees; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.employees (
    id integer NOT NULL,
    lname character varying(256) NOT NULL,
    fname character varying(256) NOT NULL,
    mname character varying(256) NOT NULL,
    dob timestamp without time zone NOT NULL,
    schedule_id integer NOT NULL,
    role_id integer NOT NULL,
    phone character varying(256) NOT NULL,
    email character varying(256) NOT NULL,
    password character varying(256) NOT NULL,
    "position" character varying(256)
);


ALTER TABLE public.employees OWNER TO admin;

--
-- Name: employees_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.employees_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.employees_id_seq OWNER TO admin;

--
-- Name: employees_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.employees_id_seq OWNED BY public.employees.id;


--
-- Name: files; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.files (
    id integer NOT NULL,
    source character varying(256) NOT NULL,
    extension character varying(256) NOT NULL,
    name character varying(256) NOT NULL
);


ALTER TABLE public.files OWNER TO admin;

--
-- Name: files_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.files_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.files_id_seq OWNER TO admin;

--
-- Name: files_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.files_id_seq OWNED BY public.files.id;


--
-- Name: meetings; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.meetings (
    id integer NOT NULL,
    name character varying(256) NOT NULL,
    description text,
    creator_id integer NOT NULL,
    date timestamp without time zone NOT NULL,
    link character varying(256) NOT NULL
);


ALTER TABLE public.meetings OWNER TO admin;

--
-- Name: meetings_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.meetings_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.meetings_id_seq OWNER TO admin;

--
-- Name: meetings_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.meetings_id_seq OWNED BY public.meetings.id;


--
-- Name: notifications; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.notifications (
    id integer NOT NULL,
    reciever_id integer NOT NULL,
    title character varying(256) NOT NULL,
    description character varying(256) NOT NULL,
    link character varying(256) NOT NULL,
    created_at timestamp without time zone DEFAULT now() NOT NULL,
    is_read boolean DEFAULT false NOT NULL
);


ALTER TABLE public.notifications OWNER TO admin;

--
-- Name: notifications_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.notifications_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.notifications_id_seq OWNER TO admin;

--
-- Name: notifications_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.notifications_id_seq OWNED BY public.notifications.id;


--
-- Name: projects; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.projects (
    id integer NOT NULL,
    name character varying(256) NOT NULL,
    description text NOT NULL,
    created_at timestamp without time zone DEFAULT now() NOT NULL,
    manager_id integer NOT NULL,
    status_id integer NOT NULL,
    release_id integer NOT NULL
);


ALTER TABLE public.projects OWNER TO admin;

--
-- Name: projects_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.projects_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.projects_id_seq OWNER TO admin;

--
-- Name: projects_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.projects_id_seq OWNED BY public.projects.id;


--
-- Name: releases; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.releases (
    id integer NOT NULL,
    name character varying(256) NOT NULL,
    version character varying(256) NOT NULL,
    description text NOT NULL,
    status_id integer NOT NULL
);


ALTER TABLE public.releases OWNER TO admin;

--
-- Name: releases_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.releases_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.releases_id_seq OWNER TO admin;

--
-- Name: releases_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.releases_id_seq OWNED BY public.releases.id;


--
-- Name: roles; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.roles (
    id integer NOT NULL,
    description character varying(15) NOT NULL
);


ALTER TABLE public.roles OWNER TO admin;

--
-- Name: roles_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.roles_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.roles_id_seq OWNER TO admin;

--
-- Name: roles_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.roles_id_seq OWNED BY public.roles.id;


--
-- Name: schedules; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.schedules (
    id integer NOT NULL,
    sun_id integer NOT NULL,
    mon_id integer NOT NULL,
    tue_id integer NOT NULL,
    wed_id integer NOT NULL,
    thu_id integer NOT NULL,
    fri_id integer NOT NULL,
    sat_id integer NOT NULL
);


ALTER TABLE public.schedules OWNER TO admin;

--
-- Name: schedules_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.schedules_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.schedules_id_seq OWNER TO admin;

--
-- Name: schedules_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.schedules_id_seq OWNED BY public.schedules.id;


--
-- Name: statuses; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.statuses (
    id integer NOT NULL,
    alias character varying(16) NOT NULL
);


ALTER TABLE public.statuses OWNER TO admin;

--
-- Name: statuses_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.statuses_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.statuses_id_seq OWNER TO admin;

--
-- Name: statuses_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.statuses_id_seq OWNED BY public.statuses.id;


--
-- Name: taskcomments; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.taskcomments (
    id integer NOT NULL,
    task_id integer NOT NULL,
    author_id integer NOT NULL,
    created_at timestamp without time zone DEFAULT now() NOT NULL,
    text text NOT NULL
);


ALTER TABLE public.taskcomments OWNER TO admin;

--
-- Name: taskcomments_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.taskcomments_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.taskcomments_id_seq OWNER TO admin;

--
-- Name: taskcomments_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.taskcomments_id_seq OWNED BY public.taskcomments.id;


--
-- Name: taskfiles; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.taskfiles (
    task_id integer NOT NULL,
    file_id integer NOT NULL
);


ALTER TABLE public.taskfiles OWNER TO admin;

--
-- Name: tasks; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.tasks (
    id integer NOT NULL,
    creator_id integer NOT NULL,
    executor_id integer,
    created_at timestamp without time zone DEFAULT now() NOT NULL,
    start_date timestamp without time zone NOT NULL,
    end_date timestamp without time zone NOT NULL,
    name character varying(256) NOT NULL,
    description text NOT NULL,
    status_id integer NOT NULL,
    project_id integer NOT NULL
);


ALTER TABLE public.tasks OWNER TO admin;

--
-- Name: tasks_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.tasks_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.tasks_id_seq OWNER TO admin;

--
-- Name: tasks_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.tasks_id_seq OWNED BY public.tasks.id;


--
-- Name: vacations; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.vacations (
    id integer NOT NULL,
    employee_id integer NOT NULL,
    start_day date NOT NULL,
    end_day date NOT NULL
);


ALTER TABLE public.vacations OWNER TO admin;

--
-- Name: vacations_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.vacations_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.vacations_id_seq OWNER TO admin;

--
-- Name: vacations_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.vacations_id_seq OWNED BY public.vacations.id;


--
-- Name: workhours; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.workhours (
    id integer NOT NULL,
    starttime time without time zone NOT NULL,
    endtime time without time zone NOT NULL,
    lunchbreak_start time without time zone NOT NULL,
    lunchbreak_end time without time zone NOT NULL
);


ALTER TABLE public.workhours OWNER TO admin;

--
-- Name: workhours_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.workhours_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.workhours_id_seq OWNER TO admin;

--
-- Name: workhours_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.workhours_id_seq OWNED BY public.workhours.id;


--
-- Name: departments id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.departments ALTER COLUMN id SET DEFAULT nextval('public.departments_id_seq'::regclass);


--
-- Name: employees id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.employees ALTER COLUMN id SET DEFAULT nextval('public.employees_id_seq'::regclass);


--
-- Name: files id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.files ALTER COLUMN id SET DEFAULT nextval('public.files_id_seq'::regclass);


--
-- Name: meetings id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.meetings ALTER COLUMN id SET DEFAULT nextval('public.meetings_id_seq'::regclass);


--
-- Name: notifications id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.notifications ALTER COLUMN id SET DEFAULT nextval('public.notifications_id_seq'::regclass);


--
-- Name: projects id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.projects ALTER COLUMN id SET DEFAULT nextval('public.projects_id_seq'::regclass);


--
-- Name: releases id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.releases ALTER COLUMN id SET DEFAULT nextval('public.releases_id_seq'::regclass);


--
-- Name: roles id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.roles ALTER COLUMN id SET DEFAULT nextval('public.roles_id_seq'::regclass);


--
-- Name: schedules id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.schedules ALTER COLUMN id SET DEFAULT nextval('public.schedules_id_seq'::regclass);


--
-- Name: statuses id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.statuses ALTER COLUMN id SET DEFAULT nextval('public.statuses_id_seq'::regclass);


--
-- Name: taskcomments id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.taskcomments ALTER COLUMN id SET DEFAULT nextval('public.taskcomments_id_seq'::regclass);


--
-- Name: tasks id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.tasks ALTER COLUMN id SET DEFAULT nextval('public.tasks_id_seq'::regclass);


--
-- Name: vacations id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.vacations ALTER COLUMN id SET DEFAULT nextval('public.vacations_id_seq'::regclass);


--
-- Name: workhours id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.workhours ALTER COLUMN id SET DEFAULT nextval('public.workhours_id_seq'::regclass);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: departments departments_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.departments
    ADD CONSTRAINT departments_pkey PRIMARY KEY (id);


--
-- Name: employeedepartments employeedepartments_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.employeedepartments
    ADD CONSTRAINT employeedepartments_pkey PRIMARY KEY (department_id, employee_id);


--
-- Name: employeemeetings employeemeetings_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.employeemeetings
    ADD CONSTRAINT employeemeetings_pkey PRIMARY KEY (meeting_id, employee_id);


--
-- Name: employees employees_email_key; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.employees
    ADD CONSTRAINT employees_email_key UNIQUE (email);


--
-- Name: employees employees_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.employees
    ADD CONSTRAINT employees_pkey PRIMARY KEY (id);


--
-- Name: files files_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.files
    ADD CONSTRAINT files_pkey PRIMARY KEY (id);


--
-- Name: meetings meetings_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.meetings
    ADD CONSTRAINT meetings_pkey PRIMARY KEY (id);


--
-- Name: notifications notifications_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.notifications
    ADD CONSTRAINT notifications_pkey PRIMARY KEY (id);


--
-- Name: projects projects_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.projects
    ADD CONSTRAINT projects_pkey PRIMARY KEY (id);


--
-- Name: releases releases_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.releases
    ADD CONSTRAINT releases_pkey PRIMARY KEY (id);


--
-- Name: roles roles_description_key; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.roles
    ADD CONSTRAINT roles_description_key UNIQUE (description);


--
-- Name: roles roles_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.roles
    ADD CONSTRAINT roles_pkey PRIMARY KEY (id);


--
-- Name: schedules schedules_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.schedules
    ADD CONSTRAINT schedules_pkey PRIMARY KEY (id);


--
-- Name: statuses statuses_alias_key; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.statuses
    ADD CONSTRAINT statuses_alias_key UNIQUE (alias);


--
-- Name: statuses statuses_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.statuses
    ADD CONSTRAINT statuses_pkey PRIMARY KEY (id);


--
-- Name: taskcomments taskcomments_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.taskcomments
    ADD CONSTRAINT taskcomments_pkey PRIMARY KEY (id);


--
-- Name: taskfiles taskfiles_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.taskfiles
    ADD CONSTRAINT taskfiles_pkey PRIMARY KEY (task_id, file_id);


--
-- Name: tasks tasks_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.tasks
    ADD CONSTRAINT tasks_pkey PRIMARY KEY (id);


--
-- Name: vacations vacations_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.vacations
    ADD CONSTRAINT vacations_pkey PRIMARY KEY (id);


--
-- Name: workhours workhours_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.workhours
    ADD CONSTRAINT workhours_pkey PRIMARY KEY (id);


--
-- Name: departments departments_lead_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.departments
    ADD CONSTRAINT departments_lead_id_fkey FOREIGN KEY (lead_id) REFERENCES public.employees(id);


--
-- Name: employeedepartments employeedepartments_department_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.employeedepartments
    ADD CONSTRAINT employeedepartments_department_id_fkey FOREIGN KEY (department_id) REFERENCES public.departments(id);


--
-- Name: employeedepartments employeedepartments_employee_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.employeedepartments
    ADD CONSTRAINT employeedepartments_employee_id_fkey FOREIGN KEY (employee_id) REFERENCES public.employees(id);


--
-- Name: employeemeetings employeemeetings_employee_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.employeemeetings
    ADD CONSTRAINT employeemeetings_employee_id_fkey FOREIGN KEY (employee_id) REFERENCES public.employees(id);


--
-- Name: employeemeetings employeemeetings_meeting_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.employeemeetings
    ADD CONSTRAINT employeemeetings_meeting_id_fkey FOREIGN KEY (meeting_id) REFERENCES public.meetings(id);


--
-- Name: employees employees_role_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.employees
    ADD CONSTRAINT employees_role_id_fkey FOREIGN KEY (role_id) REFERENCES public.roles(id);


--
-- Name: employees employees_schedule_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.employees
    ADD CONSTRAINT employees_schedule_id_fkey FOREIGN KEY (schedule_id) REFERENCES public.schedules(id);


--
-- Name: meetings meetings_creator_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.meetings
    ADD CONSTRAINT meetings_creator_id_fkey FOREIGN KEY (creator_id) REFERENCES public.employees(id);


--
-- Name: notifications notifications_reciever_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.notifications
    ADD CONSTRAINT notifications_reciever_id_fkey FOREIGN KEY (reciever_id) REFERENCES public.employees(id);


--
-- Name: projects projects_manager_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.projects
    ADD CONSTRAINT projects_manager_id_fkey FOREIGN KEY (manager_id) REFERENCES public.employees(id);


--
-- Name: projects projects_release_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.projects
    ADD CONSTRAINT projects_release_id_fkey FOREIGN KEY (release_id) REFERENCES public.releases(id);


--
-- Name: projects projects_status_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.projects
    ADD CONSTRAINT projects_status_id_fkey FOREIGN KEY (status_id) REFERENCES public.statuses(id);


--
-- Name: releases releases_status_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.releases
    ADD CONSTRAINT releases_status_id_fkey FOREIGN KEY (status_id) REFERENCES public.statuses(id);


--
-- Name: schedules schedules_fri_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.schedules
    ADD CONSTRAINT schedules_fri_id_fkey FOREIGN KEY (fri_id) REFERENCES public.workhours(id);


--
-- Name: schedules schedules_mon_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.schedules
    ADD CONSTRAINT schedules_mon_id_fkey FOREIGN KEY (mon_id) REFERENCES public.workhours(id);


--
-- Name: schedules schedules_sat_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.schedules
    ADD CONSTRAINT schedules_sat_id_fkey FOREIGN KEY (sat_id) REFERENCES public.workhours(id);


--
-- Name: schedules schedules_sun_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.schedules
    ADD CONSTRAINT schedules_sun_id_fkey FOREIGN KEY (sun_id) REFERENCES public.workhours(id);


--
-- Name: schedules schedules_thu_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.schedules
    ADD CONSTRAINT schedules_thu_id_fkey FOREIGN KEY (thu_id) REFERENCES public.workhours(id);


--
-- Name: schedules schedules_tue_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.schedules
    ADD CONSTRAINT schedules_tue_id_fkey FOREIGN KEY (tue_id) REFERENCES public.workhours(id);


--
-- Name: schedules schedules_wed_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.schedules
    ADD CONSTRAINT schedules_wed_id_fkey FOREIGN KEY (wed_id) REFERENCES public.workhours(id);


--
-- Name: taskcomments taskcomments_author_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.taskcomments
    ADD CONSTRAINT taskcomments_author_id_fkey FOREIGN KEY (author_id) REFERENCES public.employees(id);


--
-- Name: taskcomments taskcomments_task_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.taskcomments
    ADD CONSTRAINT taskcomments_task_id_fkey FOREIGN KEY (task_id) REFERENCES public.tasks(id);


--
-- Name: taskfiles taskfiles_file_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.taskfiles
    ADD CONSTRAINT taskfiles_file_id_fkey FOREIGN KEY (file_id) REFERENCES public.files(id);


--
-- Name: taskfiles taskfiles_task_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.taskfiles
    ADD CONSTRAINT taskfiles_task_id_fkey FOREIGN KEY (task_id) REFERENCES public.tasks(id);


--
-- Name: tasks tasks_creator_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.tasks
    ADD CONSTRAINT tasks_creator_id_fkey FOREIGN KEY (creator_id) REFERENCES public.employees(id);


--
-- Name: tasks tasks_executor_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.tasks
    ADD CONSTRAINT tasks_executor_id_fkey FOREIGN KEY (executor_id) REFERENCES public.employees(id);


--
-- Name: tasks tasks_project_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.tasks
    ADD CONSTRAINT tasks_project_id_fkey FOREIGN KEY (project_id) REFERENCES public.projects(id);


--
-- Name: tasks tasks_status_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.tasks
    ADD CONSTRAINT tasks_status_id_fkey FOREIGN KEY (status_id) REFERENCES public.statuses(id);


--
-- Name: vacations vacations_employee_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.vacations
    ADD CONSTRAINT vacations_employee_id_fkey FOREIGN KEY (employee_id) REFERENCES public.employees(id);


--
-- Name: SCHEMA public; Type: ACL; Schema: -; Owner: pg_database_owner
--

GRANT ALL ON SCHEMA public TO admin;


--
-- PostgreSQL database dump complete
--

\unrestrict IpgjqXGjGyk13W3QbRRsVkP6Lz9tmYcNbUG0Npbvidaz7g2egdRhTLBEwISnG6c

