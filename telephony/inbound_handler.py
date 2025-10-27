import logging
from livekit.agents import JobContext
from livekit import rtc

logger = logging.getLogger("inbound-handler")


async def handle_inbound_call(ctx: JobContext, participant: rtc.Participant):
    """
    Handle incoming phone calls
    
    Args:
        ctx: Job context
        participant: SIP participant who joined
        
    Returns:
        dict: Caller information
    """
    
    logger.info(f"Incoming call in room: {ctx.room.name}")
    logger.info(f"SIP participant joined: {participant.identity}")
    
    caller_info = {
        "identity": participant.identity,
        "number": "Unknown",
        "trunk_id": None,
    }
    
    # Extract caller information from SIP attributes
    if participant.attributes:
        caller_info["number"] = participant.attributes.get("sip.phoneNumber", "Unknown")
        caller_info["trunk_id"] = participant.attributes.get("sip.trunkId")
        caller_info["call_id"] = participant.attributes.get("sip.callId")
        
        logger.info(f"Caller number: {caller_info['number']}")
        logger.info(f"Trunk ID: {caller_info['trunk_id']}")
    
    return caller_info