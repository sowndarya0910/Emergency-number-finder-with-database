create database emergency_system;
use emergency_system;
create table user_info(
	id int auto_increment primary key,
    name varchar(100),
    age int,
    phone_number varchar(10),
    problem varchar(100),
    emergency_number varchar(10)
);
select * from user_info;
