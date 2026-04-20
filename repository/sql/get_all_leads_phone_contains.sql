SELECT id, name, email, phone FROM leads
WHERE deleted_at IS NULL AND phone LIKE %s
ORDER BY
  CASE WHEN %s = 'id'    AND %s = 'asc'  THEN id END ASC,
  CASE WHEN %s = 'id'    AND %s = 'desc' THEN id END DESC,
  CASE WHEN %s = 'name'  AND %s = 'asc'  THEN name
       WHEN %s = 'email' AND %s = 'asc'  THEN email
       WHEN %s = 'phone' AND %s = 'asc'  THEN phone END ASC,
  CASE WHEN %s = 'name'  AND %s = 'desc' THEN name
       WHEN %s = 'email' AND %s = 'desc' THEN email
       WHEN %s = 'phone' AND %s = 'desc' THEN phone END DESC
LIMIT %s OFFSET %s;
