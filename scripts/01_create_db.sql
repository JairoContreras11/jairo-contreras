-- Creación de Base de Datos para Inventario PYME
CREATE DATABASE IF NOT EXISTS pyme_inventario_db
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;
-- Creación del Usuario de Aplicación
CREATE USER IF NOT EXISTS 'pyme_admin'@'localhost'
IDENTIFIED BY 'PymeSecure2026!';
-- Asignación de Privilegios Exclusivos sobre el Esquema
GRANT ALL PRIVILEGES ON pyme_inventario_db.* TO 'pyme_admin'@'localhost';
FLUSH PRIVILEGES;
