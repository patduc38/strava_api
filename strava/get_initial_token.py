import requests
import json
# Make Strava auth API call with your 
# client_code, client_secret and code
response = requests.post(
                    url = 'https://www.strava.com/oauth/token',
                    data = {
                            'client_id': 33645,
                            'client_secret': '00889cefb82d93f0bab5241b6adcfbcf75625ffb',
                            'code': '888b120514ca808d88a0d53a17bc7cda9c2c80c5',
                            'grant_type': 'authorization_code'
                            })
# 'code': 'e9dbc8e1daf5315d4caa7a7e390af9814f2c57a0',
# Save json response as a variable
strava_tokens = response.json()
# Save tokens to file
with open('strava_tokens.json', 'w') as outfile:
    json.dump(strava_tokens, outfile)
# Open JSON file and print the file contents 
# to check it's worked properly
with open('strava_tokens.json') as check:
  data = json.load(check)
print(data)
