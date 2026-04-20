from db.connection import execute_query
from schemas.lead import Lead

def insert_lead(lead: Lead):
    return execute_query(
        "insert_lead.sql",
        (lead.name, lead.email, lead.phone),
        fetch=True
    )

def get_all_leads(limit: int = 20, offset: int = 0, order_by: str = "id", direction: str = "asc", phone_contains: str = None):
    od = (order_by, direction)
    if phone_contains:
        params = (f"%{phone_contains}%",) + od * 8 + (limit, offset)
        return execute_query("get_all_leads_phone_contains.sql", params, fetch=True)
    params = od * 8 + (limit, offset)
    return execute_query("get_all_leads.sql", params, fetch=True)

def get_leads_by_email(email: str):
    return execute_query("get_leads_by_email.sql", (email,), fetch=True)

def get_leads_by_phone(phone: str):
    return execute_query("get_leads_by_phone.sql", (phone,), fetch=True)

def get_lead_by_id(lead_id: int):
    return execute_query("get_lead_by_id.sql", (lead_id,), fetch=True)

def soft_delete_lead(lead_id: int):
    return execute_query("soft_delete_lead.sql", (lead_id,), fetch=True)

def count_all_leads(phone_contains: str = None) -> int:
    if phone_contains:
        result = execute_query("count_all_leads_phone_contains.sql", (f"%{phone_contains}%",), fetch=True)
    else:
        result = execute_query("count_all_leads.sql", fetch=True)
    return result[0]["count"]
