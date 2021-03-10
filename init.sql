\set db_name `echo $DB_NAME`
\set db_name_test `echo $DB_NAME`_test
\set db_user `echo $DB_USER`
\set db_password `echo $DB_PASSWORD`

create user :db_user with encrypted password :'db_password';
create database :db_name with owner :db_user;
create database :db_name_test with owner :db_user;
