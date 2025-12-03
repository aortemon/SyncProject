INSERT INTO public.roles (id, description) VALUES
(1,'admin'),
(2,'manager'),
(3,'executor');

INSERT INTO public.workhours (id, starttime, endtime, lunchbreak_start, lunchbreak_end) VALUES
(1, '09:00:00', '17:00:00', '13:00:00', '13:30:00'),
(2, '10:00:00', '18:00:00', '14:00:00', '14:30:00'),
(3, '16:00:00', '16:00:00', '16:00:00', '16:00:00'),
(0, '16:00:00', '16:00:00', '16:00:00', '16:00:00');

INSERT INTO public.schedules (id, sun_id, mon_id, tue_id, wed_id, thu_id, fri_id, sat_id) VALUES
(0,1,1,1,1,1,0,0),
(1,1,1,1,1,0,0,0),
(2,0,0,0,0,0,0,1);

INSERT INTO public.employees (id, lname, fname, mname, dob, schedule_id, role_id, phone, email, password, "position") VALUES
(1,'manager','manager','manager','1995-08-20',0,2,'+79607495028','manager@manager.manager','$2b$12$WTdlN.yOotcBnlZZH56kyen6cLmHgd4CPcadDlRGdQN1mKJefiVVq','manager'),
(2,'exec','exec','exec','1955-08-20',0,3,'+79607495028','exec@exec.exec','$2b$12$WTdlN.yOotcBnlZZH56kyen6cLmHgd4CPcadDlRGdQN1mKJefiVVq','executor'),
(0,'admin','admin','admin','1995-08-20',0,1,'+79607495028','admin@admin.admin','$2b$12$WTdlN.yOotcBnlZZH56kyen6cLmHgd4CPcadDlRGdQN1mKJefiVVq','admin');



INSERT INTO public.departments (id, name, lead_id) VALUES
(0,'depart1',0),
(1,'depart2',1);


INSERT INTO public.statuses (id, alias) VALUES
(0, 'Status1'),
(1, 'Status2'),
(2, 'Status3');

INSERT INTO public.releases (id, name, description, status_id, "version") VALUES
(0, 'release1', 'description', 0, 'v1.0'),
(1, 'release1', 'description', 1, 'v1.0'),
(2, 'release1', 'description', 2, 'v1.0');

INSERT INTO public.projects (id, name, description, status_id, release_id, manager_id) VALUES
(0, 'proj', 'descr', 0, 0, 1),
(1, 'proj', 'descr', 0, 0, 1),
(2, 'proj', 'descr', 0, 0, 1);

INSERT INTO meetings (id, name, description, creator_id, date, link) VALUES 
(0, 'name', 'description', 1, '2026-01-15 16:00:00', 'yandex.ru'),
(1, 'name1', 'description', 1, '2026-01-15 16:00:00', 'yandex.ru'),
(2, 'name2', 'description', 1, '2026-01-16 16:00:00', 'yandex.ru');

INSERT INTO public.employeemeetings (meeting_id, employee_id) VALUES
(0, 0),
(0, 1),
(1, 1),
(1, 2),
(2, 0),
(2, 2);


INSERT INTO public.tasks (id, creator_id, executor_id, start_date, end_date, name, description, status_id, project_id) VALUES
(1, 1, 2, '2025-12-02', '2025-12-17', 'taskname1', 'description', 0, 0),
(2, 1, 2, '2025-12-02', '2025-12-17', 'taskname2', 'description', 0, 0),
(3, 1, 2, '2025-12-02', '2025-12-17', 'taskname3', 'description', 0, 0);


INSERT INTO public.tasks (id, creator_id, start_date, end_date, name, description, status_id, project_id) VALUES
(4, 1, '2025-12-02', '2025-12-17', 'taskname4', 'description', 0, 0),
(5, 1, '2025-12-02', '2025-12-17', 'taskname5', 'description', 0, 0);


SELECT setval('departments_id_seq', COALESCE(MAX(id), 0) + 1, false) FROM departments;
SELECT setval('employees_id_seq', COALESCE(MAX(id), 0) + 1, false) FROM employees;
SELECT setval('roles_id_seq', COALESCE(MAX(id), 0) + 1, false) FROM roles;
SELECT setval('workhours_id_seq', COALESCE(MAX(id), 0) + 1, false) FROM workhours;
SELECT setval('statuses_id_seq', COALESCE(MAX(id), 0) + 1, false) FROM statuses;
SELECT setval('releases_id_seq', COALESCE(MAX(id), 0) + 1, false) FROM releases;
SELECT setval('projects_id_seq', COALESCE(MAX(id), 0) + 1, false) FROM projects;
SELECT setval('meetings_id_seq', COALESCE(MAX(id), 0) + 1, false) FROM meetings;
SELECT setval('tasks_id_seq', COALESCE(MAX(id), 0) + 1, false) FROM tasks;
SELECT setval('schedules_id_seq', COALESCE(MAX(id), 0) + 1, false) FROM schedules;