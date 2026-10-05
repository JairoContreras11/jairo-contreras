-- ====================================================================
-- Script: 01_init_db.sql
-- Propósito: Creación de Base de Datos, Usuario y Asignación de Privilegios
-- Proyecto: Sistema de Inventario para PYMEs / API Backend (DRF)
-- Autor: Jairo Contreras
-- ====================================================================

-- 1. Creación de la Base de Datos para MySQL en XAMPP
CREATE DATABASE IF NOT EXISTS pymes_db 
    CHARACTER SET utf8mb4 
    COLLATE utf8mb4_unicode_ci;

-- 2. Creación de Usuario Local para la aplicación
CREATE USER IF NOT EXISTS 'pymes_user'@'localhost' 
    IDENTIFIED BY 'pymes123';

-- 3. Asignación de Privilegios Completos
GRANT ALL PRIVILEGES ON pymes_db.* TO 'pymes_user'@'localhost';

-- 4. Aplicar los privilegios en el servidor
FLUSH PRIVILEGES;
