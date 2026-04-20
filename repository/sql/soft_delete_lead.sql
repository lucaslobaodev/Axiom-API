UPDATE leads SET deleted_at = NOW() WHERE id = %s AND deleted_at IS NULL RETURNING id;
