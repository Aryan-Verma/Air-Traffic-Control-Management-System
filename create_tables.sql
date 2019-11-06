create database proj;
use proj;

create table Login(
  username varchar(20),
  password varchar(20)
);
    
create table Runway(
  run_no int,
  status varchar(20),
    Time time(6),
  PRIMARY KEY(run_no)
);

create table Route(
  r_no int,
  status varchar(20),
  PRIMARY KEY(r_no)
);

create table Hangar(
    p_no int,
  status varchar(20),
    Time time(6),
  PRIMARY KEY(p_no)
);

create table FlightAir(
  f_no varchar(20) NOT NULL,
    p_no int,
    r_no int,
    run_no int,
  landing time(6),
    leaving time(6),
    arrival time(6),
  duration time(6),
    departure time(6),
    FOREIGN KEY(r_no) REFERENCES Route(r_no),
    FOREIGN KEY(run_no) REFERENCES Runway(run_no),
  FOREIGN KEY(p_no) REFERENCES Hangar(p_no),
  PRIMARY KEY(f_no)
);

create table Schedule(
    Time time(6),
    f_no varchar(20),
    task varchar(30),
    PRIMARY KEY(Time, f_no),
  FOREIGN KEY(f_no) REFERENCES FlightAir(f_no)
);

insert into Route values (1, 'unoccupied');
insert into Route values (2, 'unoccupied');
insert into Route values (3, 'unoccupied');
insert into Route values (4, 'unoccupied');
insert into Route values (5, 'unoccupied');
insert into Route values (6, 'unoccupied');
insert into Route values (7, 'unoccupied');
insert into Route values (8, 'unoccupied');
insert into Route values (9, 'unoccupied');
insert into Route values (10, 'unoccupied');
insert into Route values (11, 'unoccupied');
insert into Route values (12, 'unoccupied');
insert into Route values (13, 'unoccupied');
insert into Route values (14, 'unoccupied');
insert into Route values (15, 'unoccupied');
insert into Route values (16, 'unoccupied');
insert into Route values (17, 'unoccupied');
insert into Route values (18, 'unoccupied');
insert into Route values (19, 'unoccupied');
insert into Route values (20, 'unoccupied');
insert into Route values (21, 'unoccupied');
insert into Route values (22, 'unoccupied');
insert into Route values (23, 'unoccupied');
insert into Route values (24, 'unoccupied');

insert into Hangar values (1, 'unoccupied', NULL);
insert into Hangar values (2, 'unoccupied', NULL);
insert into Hangar values (3, 'unoccupied', NULL);
insert into Hangar values (4, 'unoccupied', NULL);

insert into Runway values(1, 'unoccupied', NULL);
insert into Runway values(2, 'unoccupied', NULL);
insert into Runway values(3, 'unoccupied', NULL);
insert into Runway values(4, 'unoccupied', NULL);
insert into Runway values(5, 'unoccupied', NULL);