drop table if exists eduplace_participant, participant, place, eduplace, test, eo;

create table if not exists place(
    placeid serial primary key,
    regname varchar,
    areaname varchar,
    tername varchar,
    tertypename varchar,
    unique (regname, areaname, tername)
);

create table if not exists eduplace(
    eduplaceid serial primary key,
    eoname varchar,
    eotypename varchar,
    eoparent varchar,
    placeid integer references place (placeid),
    unique (eoname, eotypename, eoparent)
);

create table if not exists participant(
    outid varchar primary key,
    birth integer not null,
    sextypename varchar not null,
    regtypename varchar not null,
    classprofilename varchar,
    classlangname varchar,
    zno_year integer not null,
    placeid integer references place (placeid)
);

create table if not exists eduplace_participant(
    relid serial primary key,
    eduplaceid integer references eduplace (eduplaceid),
    outid varchar references participant (outid),
    unique (eduplaceid, outid)
);

create table if not exists test(
    testid serial primary key,
    outid varchar not null references participant (outid),
    name varchar,
    status varchar,
    ball100 numeric(4, 1),
    ball12 integer,
    ball integer,
    adaptscale integer,
    langname varchar,
    dpalevel varchar,
    placeid integer references place (placeid),
    unique (outid, name)
);