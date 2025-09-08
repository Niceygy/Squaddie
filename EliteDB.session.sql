-- CREATE TABLE IF NOT EXISTS goals (
--     id INT NOT NULL AUTO_INCREMENT,
--     squad_id INT,
--     goal_units VARCHAR(40),
--     progress_data JSON,
--     PRIMARY KEY (id)
-- )

-- DROP TABLE contributions;

-- CREATE TABLE IF NOT EXISTS contributions (
--     id INT NOT NULL AUTO_INCREMENT,
--     goal_id INT,
--     user_id INT,
--     squad_id INT,
--     units VARCHAR(40),
--     quantity INTEGER,
--     PRIMARY KEY (id)
-- )

CREATE TABLE IF NOT EXISTS plugin_lastseen (
    id INT NOT NULL AUTO_INCREMENT,
    cmdr_name VARCHAR(40),
    time DATETIME,
    PRIMARY KEY (id)
)