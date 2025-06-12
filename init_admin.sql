-- Supprime l'utilisateur admin s'il existe déjà
DELETE FROM users WHERE username = 'admin';

-- Insère l'utilisateur admin avec le mot de passe hashé 'admin'
INSERT INTO users (username, email, hashed_password, is_active, role)
VALUES (
    'admin',
    'admin@example.com',
    '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW',  -- hash de 'admin'
    true,
    'admin'
); 