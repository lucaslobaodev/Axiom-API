import phonenumbers
from schemas.lead import Lead
from repository.lead import insert_lead

def create_lead(lead: Lead):
    parsed = phonenumbers.parse(lead.phone, "BR")
    normalized = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164)
    lead.phone = normalized
    result = insert_lead(lead)
    return result[0]
