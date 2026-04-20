from db.connection import execute_query
from schemas.lead import Lead

def insert_lead(lead: Lead):
    return execute_query(
        "insert_lead.sql",
        (lead.name, lead.email, lead.phone),
        fetch=True
    )

def get_all_leads(limit: int = 20, offset: int = 0):
    return execute_query("get_all_leads.sql", (limit, offset), fetch=True)

def get_leads_by_email(email: str):
    return execute_query("get_leads_by_email.sql", (email,), fetch=True)

def get_leads_by_phone(phone: str):
    return execute_query("get_leads_by_phone.sql", (phone,), fetch=True)

def get_lead_by_id(lead_id: int):
    return execute_query("get_lead_by_id.sql", (lead_id,), fetch=True)
