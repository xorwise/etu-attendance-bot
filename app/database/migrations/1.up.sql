CREATE TABLE IF NOT EXISTS classes (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    weekday TEXT NOT NULL,
    time TIME NOT NULL
);

CREATE TABLE IF NOT EXISTS users_classes (
    user_id INTEGER PRIMARY KEY,
    class_id INTEGER PRIMARY KEY,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (class_id) REFERENCES classes(id)
);

SET IDENTITY_INSERT classes ON;

INSERT INTO classes VALUES (
    (1, "Mon", "8:00:00"),
    (2, "Mon", "9:50:00"),
    (3, "Mon", "11:40:00"),
    (4, "Mon", "13:40:00"),
    (5, "Mon", "15:30:00"),
    (6, "Mon", "17:20:00"),
    (7, "Tue", "8:00:00"),
    (8, "Tue", "9:50:00"),
    (9, "Tue", "11:40:00"),
    (10, "Tue", "13:40:00"),
    (11, "Tue", "15:30:00"),
    (12, "Tue", "17:20:00"),
    (13, "Wen", "8:00:00"),
    (14, "Wen", "9:50:00"),
    (15, "Wen", "11:40:00"),
    (16, "Wen", "13:40:00"),
    (17, "Wen", "15:30:00"),
    (18, "Wen", "17:20:00"),
    (19, "Thu", "8:00:00"),
    (20, "Thu", "9:50:00"),
    (21, "Thu", "11:40:00"),
    (22, "Thu", "13:40:00"),
    (23, "Thu", "15:30:00"),
    (24, "Thu", "17:20:00"),
    (25, "Fri", "8:00:00"),
    (26, "Fri", "9:50:00"),
    (27, "Fri", "11:40:00"),
    (28, "Fri", "13:40:00"),
    (29, "Fri", "15:30:00"),
    (30, "Fri", "17:20:00"),
    (31, "Sat", "8:00:00"),
    (32, "Sat", "9:50:00"),
    (33, "Sat", "11:40:00"),
    (34, "Sat", "13:40:00"),
    (35, "Sat", "15:30:00"),
    (36, "Sat", "17:20:00")
) ON CONFLICT (id) DO NOTHING;

