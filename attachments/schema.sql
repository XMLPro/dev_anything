drop table if exists users;
create table users (
  userName string primary key not null ,
  password string not null
);