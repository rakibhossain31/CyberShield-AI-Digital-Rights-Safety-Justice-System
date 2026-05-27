# System Card

## System name
CyberShield AI: Digital Rights, Safety and Justice Support System

## Intended use
A demonstration system for cyber incident triage, complaint drafting support, evidence hash logging, awareness guidance, and anonymized pattern monitoring.

## Not intended for
- Legal advice
- Automated legal decision-making
- Real FIR submission
- Public offender identification
- Processing real victim data without safeguards
- Replacing police, lawyers, courts, NGOs, or human support workers

## Inputs
- Victim statement or support-worker summary
- Incident channel and location
- Optional suspect handle or contact identifier
- Evidence text or file content for hashing

## Outputs
- Case category
- Risk score and priority level
- Complaint/FIR-style draft for human review
- Relevant guidance snippets from local knowledge base
- Evidence hash and chain hash
- Awareness and safety tips
- Audit entries and dashboard metrics

## Safety design
- PII redaction helper
- Anonymized suspect identifiers
- Human-review disclaimers
- Audit logging
- No real submission workflow
- Synthetic data only
- Local database by default

## Limitations
- The classifier is keyword-based, not a validated legal model.
- The legal knowledge base is demo content, not official legal advice.
- Hash-chain simulation is not a real blockchain network.
- Risk scores are prioritization aids, not determinations of harm or guilt.
- Any real deployment would require expert legal review, security assessment, privacy assessment, and stakeholder validation.
