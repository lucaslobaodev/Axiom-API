SELECT COUNT(*) FROM leads WHERE deleted_at IS NULL AND phone LIKE %s;
