import requests
import datetime
import matplotlib.pyplot as plt
import os

USERNAME = "yaszzzz"
TOKEN = os.getenv("GH_TOKEN")

HEADERS = {}
if TOKEN:
    HEADERS["Authorization"] = f"Bearer {TOKEN}"

end = datetime.date.today()
start = end - datetime.timedelta(days=365)

url = f"https://api.github.com/users/{USERNAME}/events"
r = requests.get(url, headers=HEADERS)
r.raise_for_status()
events = r.json()

daily = {}

for e in events:
    if e.get("type") == "PushEvent":
        date = e["created_at"][:10]

        # ✅ AMAN: selalu ada
        commit_count = e["payload"].get("size", 0)

        daily[date] = daily.get(date, 0) + commit_count

counts = []
current = start
total = 0

while current <= end:
    d = current.isoformat()
    total += daily.get(d, 0)
    counts.append(total)
    current += datetime.timedelta(days=1)

plt.figure(figsize=(10, 4))
plt.plot(counts, color="#00f7ff", linewidth=3)
plt.fill_between(range(len(counts)), counts, color="#00f7ff", alpha=0.25)
plt.title("Total Commits Growth (Last 1 Year)", color="#00f7ff")
plt.axis("off")

os.makedirs("assets", exist_ok=True)
plt.savefig("assets/commit-growth.svg", transparent=True)
