SELECT id, name, email, phone FROM leads WHERE email = %s AND deleted_at IS NULL;
