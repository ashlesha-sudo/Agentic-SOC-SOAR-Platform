# Autonomous Agentic SOC & SOAR Platform

An enterprise-grade, cloud-native automated incident response pipeline deployed natively on Google Cloud Platform (GCP). This framework leverages Vertex AI and the Gemini model architecture to autonomously parse telemetry logs, query data planes, collaborate with specialized domain sub-agents, and trigger active network remediation.

---

##  System Architecture & Workflow

The platform completely replaces manual human triage loops by engineering a multi-agent cognitive architecture structured around LLM Function Calling (Tool Utilization).

1. **Telemetry Ingestion:** Ingests raw security operation flags detailing authentication anomalies.
2. **Data Isolation (SIEM):** The central agent loop connects natively to a **Google BigQuery** data warehouse via Application Default Credentials (ADC) to extract user connection history maps (`soc_logs.login_history`).
3. **Multi-Agent Handoff (CTI):** Upon discovering an anomalous external footprint, the primary Governor Agent delegates infrastructure analytics to a specialized **Cyber Threat Intelligence (CTI) Sub-Agent** to verify network reputation mechanics.
4. **Active Containment (SOAR):** If an active Account Takeover (ATO) breach signature is mathematically confirmed, the framework invokes automated remediation scripts to generate network edge-firewall block rules, neutralizing the malicious IP vector instantly.

---

##  Tech Stack & Technical Domains
* **Cloud Infrastructure Platform:** Google Cloud Platform (GCP)
* **Data Engineering & Analytics:** Google BigQuery (Serverless Log SQL Architectures)
* **Identity & Access Security:** GCP IAM System Profiles (Principle of Least Privilege Enforced)
* **AI Orchestration Plane:** Google Vertex AI, Unified `google-genai` SDK Core, Function Calling
* **Runtime Language & Environment:** Python 3, GCP Cloud Shell (Cloud Native Prototyping)

---

##  Behavioral Case Study: Output Verification

During testing execution loops inside Cloud Shell, the platform evaluated identical incoming alerts against distinct backend telemetry criteria to validate autonomous contextual discretion.

### Case Profile 1: Verified Compromise (True Positive)
* **Log Input:** 5 high-frequency failed authentications from an unmapped external host capped by a `Success` flag.
* **Agent Flow:** Governor queries BigQuery $\rightarrow$ Identifies IP $\rightarrow$ CTI Sub-Agent flags IP as a known Botnet node $\rightarrow$ Governor triggers Firewall Block.
* **Calculated MTTR (Mean Time to Remediate):** ~1.2 Seconds.

### Case Profile 2: Internal User Error (False Positive)
* **Log Input:** Multiple sequential login failures originating from a known enterprise device and internal corporate IP range, caped by a successful user entry.  
* **Agent Flow:** Governor queries logs $\rightarrow$ Evaluates device registry match $\rightarrow$ Evaluates clean reputation metrics via CTI Agent $\rightarrow$ Declares harmless user mistake. No containment tools are triggered.
