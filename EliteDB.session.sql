CREATE TABLE IF NOT EXISTS goals (
    id INT NOT NULL AUTO_INCREMENT,
    squad_id INT,
    goal_units VARCHAR(40),
    progress_data JSON,
    PRIMARY KEY (id)
)