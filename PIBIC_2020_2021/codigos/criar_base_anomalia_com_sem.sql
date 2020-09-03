copy (select *
from nasc
where idanomal = 1
) to 'D:\Downloads\com_anomalia.csv' DELIMITER ',' CSV HEADER;

copy (select *
from nasc
where idanomal = 2
order by random()
limit 344142
) to 'D:\Downloads\sem_anomalia.csv' DELIMITER ',' CSV HEADER;