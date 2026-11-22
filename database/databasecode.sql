PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS captchas_type (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    type_name VARCHAR(50) NOT NULL UNIQUE,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS captchas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    captcha_type_id INTEGER NOT NULL,
    name VARCHAR(100) NOT NULL,
    difficulty VARCHAR(20) NOT NULL,
    challenge_data TEXT,
    solution VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE CASCADE,
    FOREIGN KEY (captcha_type_id) REFERENCES captchas_type(id) ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS captchas_image (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    captcha_id INTEGER NOT NULL,
    image_path VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (captcha_id) REFERENCES captchas(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS publicacao (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    captcha_id INTEGER NOT NULL,
    title VARCHAR(100) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE CASCADE,
    FOREIGN KEY (captcha_id) REFERENCES captchas(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS publicacao_voto (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    publicacao_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    voto INTEGER NOT NULL CHECK (voto IN (1, -1)), -- 1 = Like, -1 = Dislike
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (publicacao_id, user_id),
    FOREIGN KEY (publicacao_id) REFERENCES publicacao(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE CASCADE
);



CREATE TRIGGER IF NOT EXISTS captchas_set_changed_at
AFTER UPDATE ON captchas
FOR EACH ROW
WHEN NEW.changed_at IS OLD.changed_at
BEGIN
    UPDATE captchas SET changed_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;


INSERT OR IGNORE INTO captchas_type (type_name, description) VALUES
    ('Texto', 'Desafio baseado em caracteres de texto'),
    ('Emoji', 'Desafio baseado em sequência ou identificação de emojis'),
    ('Matemático', 'Desafio baseado em operações matemáticas');

CREATE INDEX IF NOT EXISTS idx_captchas_user_id ON captchas(user_id);
CREATE UNIQUE INDEX IF NOT EXISTS idx_captchas_user_name ON captchas(user_id, name);
CREATE INDEX IF NOT EXISTS idx_captchas_captcha_type_id ON captchas(captcha_type_id);
CREATE INDEX IF NOT EXISTS idx_captchas_image_captcha_id ON captchas_image(captcha_id);
CREATE INDEX IF NOT EXISTS idx_publicacao_user_id ON publicacao(user_id);
CREATE INDEX IF NOT EXISTS idx_publicacao_captcha_id ON publicacao(captcha_id);
CREATE INDEX IF NOT EXISTS idx_publicacao_voto_pub_id ON publicacao_voto(publicacao_id);
CREATE INDEX IF NOT EXISTS idx_publicacao_voto_user_id ON publicacao_voto(user_id);