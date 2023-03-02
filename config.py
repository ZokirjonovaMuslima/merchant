host = "127.0.0.1"
user = "postgres"
password = "1"
db_name = "task_user"

'''
create table users
(
    id        serial primary key,
    name      varchar(255),
    username  varchar(255),
    balance   int,
    password  varchar(255),
    is_client bool
);
'''
