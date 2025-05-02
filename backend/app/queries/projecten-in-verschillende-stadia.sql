SELECT ministerie.afkorting, status.omschrijving, count(project_id) as aantal
FROM project as p
INNER JOIN ministerie ON p.ministerie_id=ministerie.ministerie_id
INNER JOIN status ON p.status_id=status.status_id
GROUP BY ministerie.afkorting, ministerie.ministerie_id, status.omschrijving
ORDER BY ministerie.afkorting