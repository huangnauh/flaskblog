drop table if exists entries;
drop table if exists author;
create table entries (
    id integer primary key autoincrement,
    title string not null,
    text string not null,
    path string not null
);
create table author  (
    username string primary key,
    email string not null,
    password string not null
);