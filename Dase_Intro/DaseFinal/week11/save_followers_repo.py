import requests
import json

# token
token = 'ghp_B1SEHJ1YTfVCVCyh0L9ZZTkQwcDg23KR9nI'
headers = {
    'Authorization': f'token {token}',
    'Accept': 'application/vnd.github.v3+json'
}
followers_url = 'https://api.github.com/user/following'
response = requests.get(followers_url, headers=headers)
followers = response.json()
# get every followes' repo
followers_repos = {}
# print(type(followers))
print(followers)

for follower in followers:
    repos_url = follower['repos_url']
    response = requests.get(repos_url, headers=headers)
    followers_repos[follower['login']] = response.json()

# save data
with open('followers_repos.json', 'w') as file:
    json.dump(followers_repos, file)