import json
from checker import Checker

with open('env.json','r') as f:
    env = json.load(f)

def main():
    checker = Checker(debug_discord_url=env['debug_discord'])
    checker.run()
