-- EVIDENCIA 3: Asignación de Privilegios Exclusivos sobre el Esquema
GRANT ALL PRIVILEGES ON pyme_inventario_db.* TO 'pyme_admin'@'localhost';
GRANT ALL PRIVILEGES ON pyme_inventario_db.* TO 'pyme_admin'@'127.0.0.1';
GRANT ALL PRIVILEGES ON pyme_inventario_db.* TO 'pyme_admin'@'%';
FLUSH PRIVILEGES;
