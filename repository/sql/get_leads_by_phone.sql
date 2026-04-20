SELECT id, name, email, phone FROM leads WHERE phone = %s AND deleted_at IS NULL;
