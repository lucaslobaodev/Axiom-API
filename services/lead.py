import phonenumbers
from schemas.lead import Lead
from repository.lead import insert_lead
from core.logger import setup_logger

logger = setup_logger(__name__)

def create_lead(lead: Lead):
    parsed = phonenumbers.parse(lead.phone, "BR")
    normalized = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164)
    lead.phone = normalized
    result = insert_lead(lead)
    logger.info("lead criado", extra={"email": lead.email, "phone": lead.phone})
    return result[0]
