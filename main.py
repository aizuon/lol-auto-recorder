import time
import requests
import re

name = "lulu yuumi al"
name.replace(" ", "+")

live_game_req_url = f"https://porofessor.gg/partial/live-partial/tr/{name}"

live_game_headers = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.9,tr;q=0.8",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Cookie": "darkMode=1; languageBanner_en_count=1",
    "DNT": "1",
    "Host": "porofessor.gg",
    "Pragma": "no-cache",
    "Referrer": "https://porofessor.gg/",
    "sec-ch-ua": '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest",
}

recording_headers = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.9,tr;q=0.8",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Cookie": "darkMode=1; lolg_euconsent=nitro; languageBanner_en_count=1",
    "DNT": "1",
    "Host": "www.leagueofgraphs.com",
    "Pragma": "no-cache",
    "Referrer": "https://www.leagueofgraphs.com/",
    "sec-ch-ua": '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest",
}

match_id_pattern = re.compile(r'data-spectate-gameid="([0-9]+)"')
record_url_pattern = re.compile(r"recordUrl: '([^']*)'")

last_match: int = -1
in_match: bool = False
while True:
    live_game_resp = requests.get(live_game_req_url, headers=live_game_headers)
    if not live_game_resp.ok:
        print("Error requesting live game")
        exit()
    in_match = (
        live_game_resp.text.find(
            "The summoner is not in-game, please retry later. The game must be on the loading screen or it must have started. "
        )
        == -1
    )
    if in_match:
        current_match = int(match_id_pattern.search(live_game_resp.text).group(1))
        if last_match != current_match:
            print("Match started")
            record_url = record_url_pattern.search(live_game_resp.text).group(1)
            record_resp = requests.get(record_url, headers=recording_headers)
            if not record_resp.ok:
                print("Error requesting recording")
                exit()
            last_match = current_match
    else:
        if last_match != -1:
            print("Match ended")
            last_match = -1
    time.sleep(30)
