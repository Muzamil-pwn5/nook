import re


def extract_customer_info(message: str) -> dict:
    """
    Extract customer name and email from a natural-language message.

    Returns only information that can be confidently detected.
    """

    email_match = re.search(
        r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",
        message,
    )

    email = email_match.group(0) if email_match else None

    name = None

    if email:
        text_before_email = message[:email_match.start()].strip()

        text_before_email = re.sub(
            r"^(my name is|i am|i'm|name is)\s+",
            "",
            text_before_email,
            flags=re.IGNORECASE,
        )

        text_before_email = text_before_email.rstrip(",; ")

        if text_before_email:
            words = text_before_email.split()

            if 1 <= len(words) <= 5:
                name = " ".join(words)

    return {
        "name": name,
        "email": email,
    }