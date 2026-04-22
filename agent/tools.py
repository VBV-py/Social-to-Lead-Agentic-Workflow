def mock_lead_capture(name: str, email: str, platform: str):
    """
    Mock API to capture the user's high-intent lead information.
    Triggered exclusively by the LLM when all conditions are fulfilled.
    """
    print(f"\n[LEAD CAPTURE TRIGGERED] Lead successfully logged for: {name}, {email}, {platform}")
    return f"Lead captured successfully for {name} ({email}) on {platform}."
