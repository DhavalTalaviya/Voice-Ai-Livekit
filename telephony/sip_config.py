import os
from livekit import rtc


def get_sip_config() -> dict:
    """
    Get SIP trunk configuration from environment
    
    Returns:
        dict: SIP configuration
    """
    return {
        "inbound_trunk_id": os.getenv("SIP_TRUNK_ID"),
        "outbound_trunk_id": os.getenv("SIP_OUTBOUND_TRUNK_ID"),
        "livekit_url": os.getenv("LIVEKIT_URL"),
    }


def is_sip_participant(participant: rtc.Participant) -> bool:
    """
    Check if participant is from a phone call (SIP)
    
    Args:
        participant: LiveKit participant
        
    Returns:
        bool: True if SIP participant
    """
    return participant.kind == rtc.ParticipantKind.SIP


def validate_sip_config() -> bool:
    """
    Validate SIP configuration
    
    Returns:
        bool: True if valid
        
    Raises:
        ValueError: If configuration is invalid
    """
    config = get_sip_config()
    
    if not config["inbound_trunk_id"] and not config["outbound_trunk_id"]:
        raise ValueError("At least one SIP trunk must be configured")
    
    if not config["livekit_url"]:
        raise ValueError("LIVEKIT_URL is required")
    
    return True