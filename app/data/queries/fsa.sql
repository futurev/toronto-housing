SELECT fsa, province, geom, 1 as stat
FROM all_fsa
WHERE province = {{ province_filter }}
