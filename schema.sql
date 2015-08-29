drop table if exists users;
create table users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  userName string not null ,
  password string not null
);
