PS C:\Users\parnika\Desktop\sqlite-tools-win-x64-3440000> .\sqlite3.exe
SQLite version 3.44.0 2023-11-01 11:23:50 (utf8 I/O)
Enter ".help" for usage hints.
Connected to a transient in-memory database.
Use ".open FILENAME" to reopen on a persistent database.
sqlite> .open C:\Users\parnika\PycharmProjects\pythonProject1\expense_tracker.db
sqlite> CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, password TEXT);
sqlite> CREATE TABLE IF NOT EXISTS expenses (username TEXT, date TEXT, category TEXT, amount REAL, paid_by TEXT, comments TEXT);
sqlite>