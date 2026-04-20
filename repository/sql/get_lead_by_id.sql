SELECT id, name, email, phone FROM leads WHERE id = %s AND deleted_at IS NULL;
