import httpx
import requests
from config.config import FRAUD_API_KEY, FRAUD_API_URL

class FraudChecker:
    def __init__(self):
        self.api_key = FRAUD_API_KEY
        self.api_url = FRAUD_API_URL

    def check_ip(self, ip: str) -> str:
        try:
            url = f"{self.api_url}{self.api_key}/{ip}"
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                return f"Fraud Score: {data.get('fraud_score')}, VPN: {data.get('vpn')},"\
                       f" Proxy: {data.get('proxy')}, Tor: {data.get('tor')},"\
                       f" Crawler: {data.get('crawler')}, Recent Abuse: {data.get('recent_abuse')},"\
                       f" Bot: {data.get('is_bot')}"
            else:
                return f"Error from API: {response.status_code}"
        except Exception as e:
            return f"Exception during fraud check: {str(e)}"
        
async def check_ip_fraud(ip_address: str) -> dict:
    """
    Query IPQualityScore API to check if the IP address is associated with fraud or malicious behavior.
    """
    if not FRAUD_API_KEY:
        raise ValueError("FRAUD_API_KEY is not set in .env")

    url = f"{FRAUD_API_URL}{FRAUD_API_KEY}/{ip_address}"

    #print(url)
    async with httpx.AsyncClient() as client:
        response = await client.get(url, timeout=10)

    if response.status_code != 200:
        raise Exception(f"IPQS API request failed with status {response.status_code}: {response.text}")

    data = response.json()
    return {
        "ip_address": data.get("ip_address"),
        "fraud_score": data.get("fraud_score"),
        "is_proxy": data.get("proxy"),
        "is_vpn": data.get("vpn"),
        "is_tor": data.get("tor"),
        "is_crawler": data.get("crawler"),
        "recent_abuse": data.get("recent_abuse"),
        "bot_status": data.get("bot_status"),
        "region": data.get("region"),
        "city": data.get("city"),
        "isp": data.get("ISP"),
        "organization": data.get("organization"),
        "timestamp": data.get("timestamp")
    }

import asyncio

async def test_ip_fraud():
    result = await check_ip_fraud("152.58.121.146")
    print(result)

#asyncio.run(test_ip_fraud())