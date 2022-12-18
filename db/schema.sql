drop database if exists `iot_home`;
create schema if not exists `iot_home`;

use `iot_home`;

create table if not exists iot_home.TH(
    dtime datetime  not null,
    device varchar(5) not null,
    reading decimal(3,3) not null,
    primary key (dtime,device)
);

create table if not exists iot_home.THAvgDay(
    dtime datetime not null,
    day_avg decimal(3,3) not null,
    primary key (dtime)
);

create table if not exists iot_home.HVAC(
    dtime datetime  not null,
    device varchar(5)  not null,
    reading smallint unsigned not null,
    primary key (dtime,device)
);


create table if not exists iot_home.HVACSumDay(
    dtime datetime not null,
    reading int unsigned not null,
    primary key (dtime));

