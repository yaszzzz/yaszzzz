import requests
import datetime
import matplotlib.pyplot as plt

USERNAME = "yaszzzz"
TOKEN = None  # pakai GITHUB_TOKEN

HEADERS = {
    "Authorization": f"token {TOKEN}" if TOKEN else None
}

end = datetime.date.today()
start = end - datetime.timedelta(days=365)

url = f"https://api.github.com/users/{USERNAME}/events"
r = requests.get(url, headers=HEADERS).json()

daily = {}

for e in r:
    if e["type"] == "PushEvent":
        date = e["created_at"][:10]
        daily[date] = daily.get(date, 0) + len(e["payload"]["commits"])

dates = []
counts = []

current = start
total = 0

while current <= end:
    d = current.isoformat()
    total += daily.get(d, 0)
    dates.append(d)
    counts.append(total)
    current += datetime.timedelta(days=1)

plt.figure(figsize=(10, 4))
plt.plot(counts)
plt.fill_between(range(len(counts)), counts, alpha=0.3)
plt.title("Total Commits Growth (Last 1 Year)")
plt.axis("off")
plt.savefig("assets/commit-growth.svg", transparent=True)
