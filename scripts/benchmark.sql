-- \timing
EXPLAIN ANALYZE
SELECT
    g.name,
    g.alternatenames,
    f.name as featuretype,
    ST_AsGeoJSON(g.the_geom) AS geometry
FROM geoname AS g
JOIN featurecodes AS f
ON f.code = g.featurecodeid
WHERE g.the_geom && ST_MakeEnvelope(-61.93, 11.90, -61.18, 12.65, 4326);

-- geoms only, 128MB, 9688.3, 9683.9
-- geoms + gist index, 128MB, 6.6, 2.5
-- geoms + gist + cluster, 128MB, 6.2, 3.6, 2.7
-- geoms + gist + cluster,928MB, 2.2