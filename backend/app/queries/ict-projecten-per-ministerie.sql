SELECT ministerie.ministerie_id, ministerie.afkorting, count(project_id) as aantal
FROM project
INNER JOIN ministerie
ON project.ministerie_id=ministerie.ministerie_id
GROUP BY ministerie.afkorting, ministerie.ministerie_id
ORDER BY ministerie.ministerie_id

