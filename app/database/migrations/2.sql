CREATE TABLE IF NOT EXISTS deadlines(
    id INTEGER PRIMARY KEY,
    weekday TEXT NOT NULL,
    time TIME NOT NULL
);

CREATE TABLE IF NOT EXISTS users_deadlines (
    user_id INTEGER,
    deadline_id INTEGER,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (deadline_id) REFERENCES deadlines(id) ON DELETE CASCADE,
    CONSTRAINT pk PRIMARY KEY (user_id, deadline_id)
);

INSERT INTO deadlines(id, weekday, time) 
VALUES 
    (1, 'MON', '8:00:00'),
    (2, 'MON', '9:50:00'),
    (3, 'MON', '11:40:00'),
    (4, 'MON', '13:40:00'),
    (5, 'MON', '15:30:00'),
    (6, 'MON', '17:20:00'),
    (7, 'TUE', '8:00:00'),
    (8, 'TUE', '9:50:00'),
    (9, 'TUE', '11:40:00'),
    (10, 'TUE', '13:40:00'),
    (11, 'TUE', '15:30:00'),
    (12, 'TUE', '17:20:00'),
    (13, 'WEN', '8:00:00'),
    (14, 'WEN', '9:50:00'),
    (15, 'WEN', '11:40:00'),
    (16, 'WEN', '13:40:00'),
    (17, 'WEN', '15:30:00'),
    (18, 'WEN', '17:20:00'),
    (19, 'THU', '8:00:00'),
    (20, 'THU', '9:50:00'),
    (21, 'THU', '11:40:00'),
    (22, 'THU', '13:40:00'),
    (23, 'THU', '15:30:00'),
    (24, 'THU', '17:20:00'),
    (25, 'FRI', '8:00:00'),
    (26, 'FRI', '9:50:00'),
    (27, 'FRI', '11:40:00'),
    (28, 'FRI', '13:40:00'),
    (29, 'FRI', '15:30:00'),
    (30, 'FRI', '17:20:00'),
    (31, 'SAT', '8:00:00'),
    (32, 'SAT', '9:50:00'),
    (33, 'SAT', '11:40:00'),
    (34, 'SAT', '13:40:00'),
    (35, 'SAT', '15:30:00'),
    (36, 'SAT', '17:20:00')
 ON CONFLICT (id) DO NOTHING;

CREATE TABLE IF NOT EXISTS groups (
    id INTEGER PRIMARY KEY,
    api_id INTEGER NOT NULL
);

ALTER TABLE users 
ADD COLUMN IF NOT EXISTS group_id INTEGER REFERENCES groups(id) ON DELETE CASCADE;
