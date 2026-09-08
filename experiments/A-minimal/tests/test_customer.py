from src.customer import Customer, update_customer_email

def test_update_customer_email_preserves_id_and_audit():
    customer = Customer(10, "Ana", "ana@example.com", "admin", "admin")
    updated = update_customer_email(customer, "NEW@example.com", "agent")
    assert updated.customer_id == 10
    assert updated.created_by == "admin"
    assert updated.updated_by == "agent"
    assert updated.email == "new@example.com"

def test_invalid_email_is_rejected():
    customer = Customer(10, "Ana", "ana@example.com", "admin", "admin")
    try:
        update_customer_email(customer, "invalid", "agent")
        assert False
    except ValueError as exc:
        assert str(exc) == "invalid-email"

def test_update_customer_email_strips_whitespace():
    customer = Customer(10, "Ana", "ana@example.com", "admin", "admin")
    updated = update_customer_email(customer, "  user@example.com  ", "agent")
    assert updated.email == "user@example.com"

def test_various_invalid_emails_rejected():
    customer = Customer(10, "Ana", "ana@example.com", "admin", "admin")
    invalid_emails = [
        "",
        "   ",
        "missing-at.com",
        "@missing-user.com",
        "user@",
        "user@missing-domain",
        "user@.com",
        "user@domain.",
        "user@dom..ain.com",
        "user with spaces@example.com",
        "user@exam ple.com",
        None,
        123,
    ]
    for email in invalid_emails:
        try:
            update_customer_email(customer, email, "agent")
            assert False, f"Expected ValueError for email: {email}"
        except ValueError as exc:
            assert str(exc) == "invalid-email"

