import os
from google import genai
from google.genai import types
from google.cloud import bigquery

# Initialize Google Cloud Clients
bq_client = bigquery.Client()
client = genai.Client(vertexai=True)

# --- TOOLS ---
def query_login_logs(user_email: str) -> str:
    """Tool: Queries BigQuery login logs to pull history records for a user."""
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    query = f"""
        SELECT timestamp, ip_address, country, status, device_id 
        FROM `{project_id}.soc_logs.login_history` 
        WHERE user_email = '{user_email}' 
        ORDER BY timestamp DESC LIMIT 10
    """
    query_job = bq_client.query(query)
    log_dump = f"Logs found for {user_email}:\n"
    for row in query_job.result():
        log_dump += f"[{row.timestamp}] IP: {row.ip_address} | Location: {row.country} | Status: {row.status} | Device: {row.device_id}\n"
    return log_dump

def simulate_threat_intel_lookup(ip_address: str) -> str:
    """Tool: Simulates looking up an IP address in external threat databases."""
    if ip_address == "185.220.101.5":
        return f"Threat Intel Alert for IP {ip_address}: Flagged as malicious infrastructure. Category: Active Botnet."
    return f"Threat Intel Report for IP {ip_address}: Clean reputation."

def block_malicious_ip(ip_address: str) -> str:
    """Tool: Remediation action that blocks an IP address at the corporate firewall level."""
    print(f"\n [SOAR ACTION TRIGGERED] Executing automated firewall rule generation...")
    print(f" [FIREWALL] Successfully blocked all incoming traffic from IP: {ip_address}")
    return f"Success: IP address {ip_address} has been blacklisted on the edge firewall. Active connections severed."

# --- SPECIALIZED SUB-AGENT ---
def threat_intel_agent(ip_address: str) -> str:
    """Sub-Agent: An expert cyber threat intelligence analyst agent."""
    intel_prompt = """
    You are a Threat Intelligence Specialist Agent. Your only job is to analyze infrastructure.
    Use 'simulate_threat_intel_lookup' to research the provided IP. Summarize the threat rating.
    """
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=f"Analyze this IP address: {ip_address}",
        config=types.GenerateContentConfig(
            system_instruction=intel_prompt,
            tools=[simulate_threat_intel_lookup],
            temperature=0.1
        )
    )
    return response.text

# --- MAIN GOVERNOR AGENT ---
governor_instructions = """
You are the Lead SOC Governor Agent orchestrating incident response.
When given an alert, follow this strict playbook:
1. Call 'query_login_logs' to pull internal user authentication history.
2. If an anomalous IP is found, invoke 'threat_intel_agent' to analyze the infrastructure.
3. If the sub-agent confirms the IP is malicious AND there is a successful login, you are looking at an active breach (Account Takeover). Immediately invoke 'block_mali>
4. Output a comprehensive final briefing detailing the timeline, the malicious infrastructure metrics, and a confirmation of the containment action taken.
"""

mock_alert_trigger = "High Alert: Critical authentication anomaly detected for user: j_doe@company.com"

print(" Launching Production-Grade Multi-Agent SOC & SOAR Loop...")
print("Contents: Analyzing incoming telemetry...")

import time
print("Pausing for 5 seconds to manage API rate limits...")
time.sleep(5)

final_briefing = client.models.generate_content(
    model='gemini-2.5-flash',

    contents=mock_alert_trigger,
    config=types.GenerateContentConfig(
        system_instruction=governor_instructions,
        # We expose the data tools, sub-agents, and the active remediation tool to the Governor
        tools=[query_login_logs, threat_intel_agent, block_malicious_ip],
        temperature=0.2
    )
)

print("\n--- FINAL MULTI-AGENT CONTAINMENT & INCIDENT BRIEFING --- ")
print(final_briefing.text)
  
