with temp_func as(
select regname, round(avg(ball100), 2) as "2019"
from place, test, participant where (place.placeid = test.placeid) and (test.outid = participant.outid)
and (status = 'Зараховано') and (name = 'Історія України') and (zno_year = 2019)
group by regname
), temp_func2 as(
select regname, round(avg(ball100), 2) as "2020"
from place, test, participant where (place.placeid = test.placeid) and (test.outid = participant.outid)
and (status = 'Зараховано') and (name = 'Історія України') and (zno_year = 2020)
group by regname
)  select temp_func.regname, "2019", "2020" from temp_func, temp_func2 where temp_func.regname = temp_func2.regname