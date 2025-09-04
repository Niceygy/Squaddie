CREATE TABLE IF NOT EXISTS users (
    id INT NOT NULL AUTO_INCREMENT,
    commander_name VARCHAR(50),
    squad_id INT,
    progress_data JSON,
    PRIMARY KEY (id)
)