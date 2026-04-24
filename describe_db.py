import sys
sys.path.append('.')
from modules.database import DatabaseConnection

db = DatabaseConnection()
db.connect()
rows = db.execute_query('DESCRIBE books')
for row in rows:
    print(f"{row['Field']}: {row['Type']}")
