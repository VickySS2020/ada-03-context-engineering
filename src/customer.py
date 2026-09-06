import re
from dataclasses import dataclass

EMAIL_REGEX = re.compile(r"^[^@\s]+@[^@\s\.]+(\.[^@\s\.]+)+$")

@dataclass
class Customer:
    customer_id: int
    name: str
    email: str
    created_by: str
    updated_by: str

def update_customer_email(customer, new_email, updated_by):
    if not isinstance(new_email, str):
        raise ValueError("invalid-email")
    cleaned_email = new_email.strip()
    if not EMAIL_REGEX.match(cleaned_email):
        raise ValueError("invalid-email")
    if not isinstance(updated_by, str):
        raise ValueError("invalid-user")
    customer.email = cleaned_email.lower()
    customer.updated_by = updated_by
    return customer

