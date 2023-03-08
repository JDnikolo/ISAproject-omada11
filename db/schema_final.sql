drop database if exists `iot_home`;
create schema if not exists `iot_home`;

use `iot_home`;
--  15min sensors and aggregates-- 
-- TH[1,2]
create table if not exists iot_home.TH(
    dtime datetime  not null,
    device varchar(5) not null,
    reading decimal(6,3) not null,
    primary key (dtime,device)
);
create table if not exists iot_home.THAvgDay(
    dtime datetime not null,
    device varchar(5) not null,
    day_avg decimal(6,3) not null,
    primary key (dtime,device)
);
-- HVAC[1,2]
create table if not exists iot_home.HVAC(
    dtime datetime  not null,
    device varchar(5)  not null,
    reading smallint unsigned not null,
    primary key (dtime,device)
);
create table if not exists iot_home.HVACSumDay(
    dtime datetime not null,
    device varchar(5) not null,
    day_sum int unsigned not null,
    primary key (dtime,device)
);
-- MiAC[1,2]
CREATE TABLE IF NOT EXISTS iot_home.MIAC(
    dtime DATETIME NOT NULL,
    device VARCHAR(5) NOT NULL,
    reading SMALLINT UNSIGNED NOT NULL,
    primary key (dtime,device)
);
CREATE TABLE IF NOT EXISTS iot_home.MIACSumDay(
    dtime DATETIME NOT NULL,
    device varchar(5) not null,
    day_sum SMALLINT UNSIGNED NOT NULL,
    primary key (dtime,device)
);
-- W1
CREATE TABLE IF NOT EXISTS iot_home.Water(
    dtime DATETIME NOT NULL,
    device VARCHAR(5) NOT NULL,
    reading DECIMAL(4,3) NOT NULL,
    arrival_status ENUM('ontime','late','rejected') DEFAULT 'ontime' NOT NULL,
    PRIMARY KEY (dtime,device,arrival_status)   
);
CREATE TABLE IF NOT EXISTS iot_home.WaterSumDay(
    dtime DATETIME NOT NULL,
    device varchar(5) not null,
    day_sum DECIMAL(6,3) NOT NULL,
    primary key (dtime,device)
);

-- daily sensors and diff aggregates-- 
-- Etot
CREATE TABLE IF NOT EXISTS iot_home.Etot(
    dtime DATETIME NOT NULL,
    reading int UNSIGNED NOT NULL,
    PRIMARY KEY (dtime)   
);
CREATE TABLE IF NOT EXISTS iot_home.EtotDayDiff(
    dtime DATETIME NOT NULL,
    day_diff int UNSIGNED NOT NULL,
    PRIMARY KEY (dtime)   
);
-- Wtot
CREATE TABLE IF NOT EXISTS iot_home.Wtot(
    dtime DATETIME NOT NULL,
    reading int UNSIGNED NOT NULL,
    PRIMARY KEY (dtime)   
);
CREATE TABLE IF NOT EXISTS iot_home.WtotDayDiff(
    dtime DATETIME NOT NULL,
    day_diff int UNSIGNED NOT NULL,
    PRIMARY KEY (dtime) 
);

--  leak aggregates-- 

CREATE TABLE IF NOT EXISTS iot_home.ElecDayRest(
    dtime DATETIME NOT NULL,
    leak_amount int NOT NULL,
    PRIMARY KEY (dtime)   
);
CREATE TABLE IF NOT EXISTS iot_home.WaterDayRest(
    dtime DATETIME NOT NULL,
    leak_amount int NOT NULL,
    PRIMARY KEY (dtime)   
);

--  movement sensor and alarm-- 

CREATE TABLE IF NOT EXISTS iot_home.Movement(
    dtime DATETIME NOT NULL,
    device VARCHAR(5) NOT NULL,
    PRIMARY KEY (dtime,device)   
);
CREATE TABLE IF NOT EXISTS iot_home.MovementSumDay(
    dtime DATETIME NOT NULL,
    device varchar(5) not null,
    day_count int NOT NULL,
    primary key (dtime,device)
);
CREATE TABLE IF NOT EXISTS iot_home.Alarms(
    dtime DATETIME NOT NULL,
    alarm_trigger VARCHAR(50) NOT null, --  what triggered the alarm
    --  TODO: consider adding fields here.
    PRIMARY KEY (dtime)   
);

-- rejected late events

CREATE TABLE IF NOT EXISTS iot_home.RejectedEvents(
    dtime_event DATETIME NOT NULL,
    dtime_received DATETIME NOT NULL,
    device varchar(5) NOT NULL,
    reading float, -- float in order to accomodate late events from all devices
    PRIMARY KEY (dtime_event,device)
)