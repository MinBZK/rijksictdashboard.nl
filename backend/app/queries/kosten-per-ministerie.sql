SELECT  ministerie.afkorting, cast(SUM(kosten_meerjarig_geschat_initieel) as decimal(100,2)) as kosten
FROM project 
INNER JOIN "ministerie" 
ON "project".ministerie_id="ministerie".ministerie_id
GROUP BY ministerie.afkorting
ORDER BY ministerie.afkorting