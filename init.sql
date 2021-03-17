\set db_name `echo $KINTON_DATABASE`
\set db_name_test `echo $KINTON_DATABASE`_test
\set db_user `echo $KINTON_USER`
\set db_password `echo $KINTON_PASSWORD`

create user :db_user with encrypted password :'db_password';
create database :db_name with owner :db_user;
create database :db_name_test with owner :db_user;
