drop table if exists groups;
create table groups (
  id integer primary key autoincrement ,
  groupname text not null,
  username text not null
);

drop table if exists users;
create table users (
  id integer primary key autoincrement ,
  username text not null,
  password text not null
);

drop table if exists entries;
create table entries (
  id integer primary key autoincrement,
  title string not null,
  text string not null
);