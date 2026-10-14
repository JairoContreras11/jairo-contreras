from django.db.backends.base.base import BaseDatabaseWrapper
from django.db.backends.mysql.features import DatabaseFeatures

# Compatibilidad con MariaDB / MySQL de XAMPP en Windows
BaseDatabaseWrapper.check_database_version_supported = lambda self: None
DatabaseFeatures.can_return_columns_from_insert = property(lambda self: False)
DatabaseFeatures.can_return_rows_from_bulk_insert = property(lambda self: False)
