drop table if exists users;
create table users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  userName string not null ,
  password string not null
);

drop table if exists spend;
create table spend(
  id INTEGER  PRIMARY KEY  AUTOINCREMENT,
  userName string not null,
  itemName string not null,
  money INTEGER not null,
  daydata date not null,
  text string
);

drop table if exists snotification;
create table snotification(
  sender string,
  recipient string,
  itemName string,
  id INTEGER
);

drop table if exists spendShare;
create table spendShare(
  sender string,
  recipient string,
  itemName string,
  itemID INTEGER
);

drop table if exists friend;
create table friend(
   userName string not null,
   friendName string not null
);