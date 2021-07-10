### To reset Auto Number cloumn
UPDATE SQLITE_SEQUENCE SET SEQ=0 WHERE NAME='table_name';

### To delete all table records
DELETE FROM table_name;

### To Empty memory after deletion
VACUUM;