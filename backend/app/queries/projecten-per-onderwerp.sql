select
  "Waarde" as "Onderwerp",
  count(*) as "Aantal"
from
  "vProjectIndicator"
where
  "IndicatorTitel" = 'Onderwerp'
group by
  "Waarde"
order by
  "Aantal" desc