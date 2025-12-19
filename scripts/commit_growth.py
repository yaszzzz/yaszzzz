import requests
import datetime
import matplotlib.pyplot as plt
import os

USERNAME = "yaszzzz"
TOKEN = os.getenv("GH_TOKEN")

HEADERS = {
    "Authorization": f"Bearer {TOKEN}"
}

# range 1 tahun
end = datetime.date.today()
start = end - datetime.timedelta(days=365)

query = """
query($login: String!) {
  user(login: $login) {
    repositories(first: 100, ownerAffiliations: OWNER, isFork: false) {
      nodes {
        defaultBranchRef {
          target {
            ... on Commit {
              history(since: "%sT00:00:00Z") {
                edges {
                  node {
                    committedDate
                  }
                }
              }
            }
          }
        }
      }
    }
  }
}
""" % start.isoformat()

res = requests.post(
    "https://api.github.com/graphql",
    headers=HEADERS,
    json={"query": query, "variables": {"login": USERNAME}}
)
res.raise_for_status()
data = res.json()

daily = {}

repos = data["data"]["user"]["repositories"]["nodes"]
for repo in repos:
    ref = repo.get("defaultBranchRef")
    if not ref:
        continue

    commits = ref["target"]["history"]["edges"]
    for c in commits:
        date = c["node"]["committedDate"][:10]
        daily[date] = daily.get(date, 0) + 1

counts = []
total = 0
current = start

while current <= end:
    d = current.isoformat()
    total += daily.get(d, 0)
    counts.append(total)
    current += datetime.timedelta(days=1)

plt.figure(figsize=(12, 4))
plt.plot(counts, color="#00f7ff", linewidth=3)
plt.fill_between(range(len(counts)), counts, color="#00f7ff", alpha=0.25)
plt.title("Total Commits Growth (Last 1 Year)", color="#00f7ff")
plt.axis("off")

os.makedirs("assets", exist_ok=True)
plt.savefig("assets/commit-growth.svg", transparent=True)
