-- place migration
insert into place (regname, areaname, tername, tertypename)
select distinct regname, areaname, tername, tertypename
from zno
where regname is not null
on conflict do nothing;

insert into place (regname, areaname, tername)
select distinct eoregname, eoareaname, eotername
from zno
where eoregname is not null
on conflict do nothing;

insert into place (regname, areaname, tername)
select distinct ukrptregname, ukrptareaname, ukrpttername
from zno
where ukrptregname is not null
on conflict do nothing;

insert into place (regname, areaname, tername)
select distinct histptregname, histptareaname, histpttername
from zno
where histptregname is not null
on conflict do nothing;

insert into place (regname, areaname, tername)
select distinct mathptregname, mathptareaname, mathpttername
from zno
where mathptregname is not null
on conflict do nothing;

insert into place (regname, areaname, tername)
select distinct physptregname, physptareaname, physpttername
from zno
where physptregname is not null
on conflict do nothing;

insert into place (regname, areaname, tername)
select distinct chemptregname, chemptareaname, chempttername
from zno
where chemptregname is not null
on conflict do nothing;

insert into place (regname, areaname, tername)
select distinct bioptregname, bioptareaname, biopttername
from zno
where bioptregname is not null
on conflict do nothing;

insert into place (regname, areaname, tername)
select distinct geoptregname, geoptareaname, geopttername
from zno
where geoptregname is not null
on conflict do nothing;

insert into place (regname, areaname, tername)
select distinct engptregname, engptareaname, engpttername
from zno
where engptregname is not null
on conflict do nothing;

insert into place (regname, areaname, tername)
select distinct fraptregname, fraptareaname, frapttername
from zno
where fraptregname is not null
on conflict do nothing;

insert into place (regname, areaname, tername)
select distinct deuptregname, deuptareaname, deupttername
from zno
where deuptregname is not null
on conflict do nothing;

insert into place (regname, areaname, tername)
select distinct spaptregname, spaptareaname, spapttername
from zno
where spaptregname is not null
on conflict do nothing;

-- eduplace migration
insert into eduplace (eoname, eotypename, eoparent, placeid)
select distinct eoname, eotypename, eoparent,
(select placeid from place where
regname = zno.eoregname and
areaname = zno.eoareaname and
tername = zno.eotername)
from zno
where eoname is not null
on conflict do nothing;

-- participant migration
insert into participant (outid, birth, sextypename,
regtypename, classprofilename, classlangname, zno_year, placeid)
select distinct outid, birth, sextypename, regtypename, classprofilename, classlangname, zno_year,
(select placeid from place where
regname = zno.regname and
areaname = zno.areaname and
tername = zno.tername)
from zno
on conflict do nothing;

-- eduplace participant migration
insert into eduplace_participant (eduplaceid, outid)
select distinct
(select eduplaceid from eduplace where
eoname = zno.eoname and
eotypename = zno.eotypename and
eoparent = zno.eoparent), outid
from zno
where eoname is not null
on conflict do nothing;

-- test migration
insert into test (outid, name, status, ball100, ball12, ball, adaptscale, placeid)
select outid, ukrtest, ukrteststatus, ukrball100, ukrball12, ukrball,
ukradaptscale,
(select placeid from place where
regname = zno.ukrptregname and
areaname = zno.ukrptareaname and
tername = zno.ukrpttername)
from zno
where ukrtest is not null;

insert into test (outid, name, status, ball100, ball12, ball, langname, placeid)
select outid, histtest, histteststatus, histball100, histball12, histball, histlang,
(select placeid from place where
regname = zno.histptregname and
areaname = zno.histptareaname and
tername = zno.histpttername)
from zno
where histtest is not null;

insert into test (outid, name, status, ball100, ball12, ball, langname,
dpalevel, placeid)
select outid, mathtest, mathteststatus, mathball100, mathball12, mathball,
mathlang, mathdpalevel,
(select placeid from place where
regname = zno.mathptregname and
areaname = zno.mathptareaname and
tername = zno.mathpttername)
from zno
where mathtest is not null;

insert into test (outid, name, status, ball100, ball12, ball, langname, placeid)
select outid, phystest, physteststatus, physball100, physball12, physball,
physlang,
(select placeid from place where
regname = zno.physptregname and
areaname = zno.physptareaname and
tername = zno.physpttername)
from zno
where phystest is not null;

insert into test (outid, name, status, ball100, ball12, ball, langname, placeid)
select outid, chemtest, chemteststatus, chemball100, chemball12, chemball, chemlang,
(select placeid from place where
regname = zno.chemptregname and
areaname = zno.chemptareaname and
tername = zno.chempttername)
from zno
where chemtest is not null;

insert into test (outid, name, status, ball100, ball12, ball, langname, placeid)
select outid, biotest, bioteststatus, bioball100, bioball12, bioball, biolang,
(select placeid from place where
regname = zno.bioptregname and
areaname = zno.bioptareaname and
tername = zno.biopttername)
from zno
where biotest is not null;

insert into test (outid, name, status, ball100, ball12, ball, langname, placeid)
select outid, geotest, geoteststatus, geoball100, geoball12, geoball, geolang,
(select placeid from place where
regname = zno.geoptregname and
areaname = zno.geoptareaname and
tername = zno.geopttername)
from zno
where geotest is not null;

insert into test (outid, name, status, ball100, ball12, ball, dpalevel, placeid)
select outid, engtest, engteststatus, engball100, engball12, engball, engdpalevel,
(select placeid from place where
regname = zno.engptregname and
areaname = zno.engptareaname and
tername = zno.engpttername)
from zno
where engtest is not null;

insert into test (outid, name, status, ball100, ball12, ball, dpalevel, placeid)
select outid, fratest, frateststatus, fraball100, fraball12, fraball, fradpalevel,
(select placeid from place where
regname = zno.fraptregname and
areaname = zno.fraptareaname and
tername = zno.frapttername)
from zno
where fratest is not null;

insert into test (outid, name, status, ball100, ball12, ball, dpalevel, placeid)
select outid, deutest, deuteststatus, deuball100, deuball12, deuball, deudpalevel,
(select placeid from place where
regname = zno.deuptregname and
areaname = zno.deuptareaname and
tername = zno.deupttername)
from zno
where deutest is not null;

insert into test (outid, name, status, ball100, ball12, ball, dpalevel, placeid)
select outid, spatest, spateststatus, spaball100, spaball12, spaball, spadpalevel,
(select placeid from place where
regname = zno.spaptregname and
areaname = zno.spaptareaname and
tername = zno.spapttername)
from zno
where spatest is not null;