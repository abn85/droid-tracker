import json
import urllib.request
import os

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
        starts = deal.get("startsAt", "N/A")
        ends = deal.get("endsAt", "N/A")

        msg = f"🚨 **New Droid Deal Alert!** 🚨\n• **Droid:** {droid}\n• **Variant/Mutation:** {mutation}\n• **Rarity:** {rarity}\n• **Starts:** {starts}\n• **Ends:** {ends}"
        print(msg)
        
        # Write directly to GitHub Actions output safely
        github_output = os.getenv("GITHUB_OUTPUT")
        if github_output:
            with open(github_output, "a") as f:
                f.write(f"message<<EOF\n{msg}\nEOF\n")
except Exception as e:
    print(f"Error fetching deal: {e}")
  
