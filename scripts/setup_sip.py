"""Setup SIP trunks via API"""
import asyncio
import json
import os
from dotenv import load_dotenv
from livekit import api

load_dotenv()


async def create_inbound_trunk():
    """Create inbound SIP trunk"""
    
    # Load config
    with open("config/inbound_trunk.json", "r") as f:
        config = json.load(f)
    
    livekit_api = api.LiveKitAPI(
        os.getenv("LIVEKIT_URL"),
        os.getenv("LIVEKIT_API_KEY"),
        os.getenv("LIVEKIT_API_SECRET"),
    )
    
    try:
        trunk = await livekit_api.sip.create_sip_inbound_trunk(
            api.CreateSIPInboundTrunkRequest(**config)
        )
        print(f"Inbound trunk created: {trunk.sip_trunk_id}")
        return trunk
    finally:
        await livekit_api.aclose()


async def create_outbound_trunk():
    """Create outbound SIP trunk"""
    
    # Load config
    with open("config/outbound_trunk.json", "r") as f:
        config = json.load(f)
    
    livekit_api = api.LiveKitAPI(
        os.getenv("LIVEKIT_URL"),
        os.getenv("LIVEKIT_API_KEY"),
        os.getenv("LIVEKIT_API_SECRET"),
    )
    
    try:
        trunk = await livekit_api.sip.create_sip_outbound_trunk(
            api.CreateSIPOutboundTrunkRequest(**config)
        )
        print(f"Outbound trunk created: {trunk.sip_trunk_id}")
        return trunk
    finally:
        await livekit_api.aclose()


async def create_dispatch_rule():
    """Create dispatch rule for inbound calls"""
    
    # Load config
    with open("config/dispatch_rules.json", "r") as f:
        config = json.load(f)
    
    livekit_api = api.LiveKitAPI(
        os.getenv("LIVEKIT_URL"),
        os.getenv("LIVEKIT_API_KEY"),
        os.getenv("LIVEKIT_API_SECRET"),
    )
    
    try:
        rule = await livekit_api.sip.create_sip_dispatch_rule(
            api.CreateSIPDispatchRuleRequest(**config)
        )
        print(f"Dispatch rule created: {rule.sip_dispatch_rule_id}")
        return rule
    finally:
        await livekit_api.aclose()


async def setup_all():
    """Setup all SIP components"""
    print("\nSetting up SIP trunks and rules...\n")
    
    inbound = await create_inbound_trunk()
    outbound = await create_outbound_trunk()
    dispatch = await create_dispatch_rule()
    
    print(f"\nSetup complete!")
    print(f"\nAdd these to your .env file:")
    print(f"SIP_TRUNK_ID={inbound.sip_trunk_id}")
    print(f"SIP_OUTBOUND_TRUNK_ID={outbound.sip_trunk_id}")


if __name__ == "__main__":
    asyncio.run(setup_all())