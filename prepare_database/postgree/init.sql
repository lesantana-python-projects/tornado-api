create user usr_dev with PASSWORD '123456';

create DATABASE gaivota
    with
    OWNER = usr_dev
    ENCODING = 'UTF8'
    CONNECTION LIMIT = -1;

grant all privileges on DATABASE gaivota to usr_dev;

\connect gaivota;

create SCHEMA gaivota
    AUTHORIZATION usr_dev;

SET search_path TO gaivota;

ALTER USER usr_dev CREATEDB;
