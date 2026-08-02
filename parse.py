import json
import urllib.request
import os
from datetime import datetime, timezone

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
        
        starts_str = deal.get("startsAt")
        ends_str = deal.get("endsAt")
        
        def get_discord_timestamp(iso_str, format_type="f"):
            if not iso_str:
                return "N/A"
            try:
                # Parse ISO time and convert to Unix epoch timestamp seconds
                dt = datetime.strptime(iso_str.replace("Z", "+00:00"), "%Y-%m-%dT%H:%M:%S.%f%z")
                epoch_seconds = int(dt.timestamp())
                # Discord markdown format: <t:TIMESTAMP:TYPE>
                return f"<t:{epoch_seconds}:{format_type}>"
            except Exception:
                return iso_str

        starts_formatted = get_discord_timestamp(starts_str, "f") # Full local date & time
        ends_countdown = get_discord_timestamp(ends_str, "R")     # Relative countdown (e.g., "in 2 hours")

        msg = f"🚨 **New Droid Deal Alert!** 🚨\n• **Droid:** {droid}\n• **Variant/Mutation:** {mutation}\n• **Rarity:** {rarity}\n• **Starts:** {starts_formatted}\n• **Ends In:** {ends_countdown}"
        print(msg)
        
        github_output = os.getenv("GITHUB_OUTPUT")
        if github_output:
            with open(github_output, "a") as f:
                f.write(f"message<<EOF\n{msg}\nEOF\n")
except Exception as e:
    print(f"Error fetching deal: {e}")
    
