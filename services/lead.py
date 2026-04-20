import phonenumbers
from schemas.lead import Lead
from repository.lead import insert_lead, get_leads_by_email
from core.logger import setup_logger

logger = setup_logger(__name__)

def create_lead(lead: Lead):
    parsed = phonenumbers.parse(lead.phone, "BR")
    normalized = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164)
    lead.phone = normalized
    try:
        result = insert_lead(lead)
        logger.info("lead criado", extra={"email": lead.email, "phone": lead.phone})
        return result[0]
    except ValueError as e:
        if str(e) == "duplicate":
            logger.info("lead já existente, retornando cadastro atual", extra={"email": lead.email})
            existing = get_leads_by_email(lead.email)
            return existing[0]
        raise
