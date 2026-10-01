# hackathon/classifier.py

def classify_grievance(text: str) -> dict:
    text_lower = text.lower()
    
    # Priority & Category Logic
    if any(w in text_lower for w in ["pothole", "accident", "road", "biker", "vehicle", "traffic"]):
        return {
            "summary": "Severe road hazard/pothole causing traffic congestion and safety risk.",
            "category": "Road Infrastructure",
            "priority": "URGENT",
            "action": "Route immediately to Ward G/North maintenance team."
        }
    elif any(w in text_lower for w in ["garbage", "dump", "waste", "smell", "trash", "bin"]):
        return {
            "summary": "Uncollected garbage accumulation posing public sanitation hazards.",
            "category": "Public Health & Sanitation",
            "priority": "HIGH" if "smell" in text_lower or "market" in text_lower else "MEDIUM",
            "action": "Assign to Local Ward Sanitation Crew."
        }
    elif any(w in text_lower for w in ["water", "leak", "pipe", "overflow", "drain"]):
        return {
            "summary": "Water pipeline leakage or drainage overflow reported.",
            "category": "Water Resources & Drainage",
            "priority": "HIGH",
            "action": "Dispatch Hydraulic Engineer & Repair Unit."
        }
    elif any(w in text_lower for w in ["light", "dark", "electricity", "pole"]):
        return {
            "summary": "Non-functional street lighting causing safety issues at night.",
            "category": "Electrical & Street Lighting",
            "priority": "MEDIUM",
            "action": "Assign to Ward Electricity Department."
        }
    else:
        truncated = text[:70] + "..." if len(text) > 70 else text
        return {
            "summary": f"General citizen complaint: '{truncated}'",
            "category": "General Civic Helpdesk",
            "priority": "LOW",
            "action": "Route to Central Ward Customer Support Desk."
        }