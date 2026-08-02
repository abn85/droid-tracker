import json
import urllib.request
import os
from datetime import datetime

url = "https://gonk.tools/api/droid-alerts/limited-deal"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})

try:
    with urllib.request.urlopen(req) as response:
        body = response.read().decode("utf-8")
        data = json.loads(body)
        deal = data.get("deal", {})
        
        droid = deal.get("droid", "Unknown")
        mutation = deal.get("mutation", "Standard")
        rarity = deal.get("rarity", "Unknown")
        
        # Function to make timestamps clean and readable
        def format_time(iso_str):
            if not iso_str:
                return "N/A"
            try:
                # Parse ISO format and convert to a clean layout like Aug 2, 2026 at 12:00 AM UTC
                dt = datetime.strptime(iso_str.replace("Z", "+00:00"), "%Y-%m-%dT%H:%M:%S.%f%z")
                return dt.strftime("%b %d, %Y at %I:%M %p UTC")
            except Exception:
                return iso_str # Fallback if format varies

        starts = format_time(deal.get("startsAt"))
        ends = format_time(deal.get("endsAt"))

        msg = f"🚨 **New Droid Deal Alert!** 🚨\n• **Droid:** {droid}\n• **Variant/Mutation:** {mutation}\n• **Rarity:** {rarity}\n• **Starts:** {starts}\n• **Ends:** {ends}"
        print(msg)
        
        github_output = os.getenv("GITHUB_OUTPUT")
        if github_output:
            with open(github_output, "a") as f:
                f.write(f"message<<EOF\n{msg}\nEOF\n")
except Exception as e:
    print(f"Error fetching deal: {e}")
    
