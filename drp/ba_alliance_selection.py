import os
from pprint import pprint
import requests
from typing import Any, Dict
import json


def get_blue_alliance_api(token: str, url: str, key: str) -> Any:
    response = requests.get(url, headers={'X-TBA-Auth-Key': key})
    if response.status_code != 200:
        raise IOError(f"Getting {token} failed with status code {response.status_code}")
    return response.json()


def get_event_keys(year_district: str, key: str) -> str:
    path = f"https://www.thebluealliance.com/api/v3/district/{year_district}/events/keys"
    return get_blue_alliance_api(year_district, path, key)


def get_event_alliances(event: str,  key: str) -> Any:
    path = f"https://www.thebluealliance.com/api/v3/event/{event}/alliances"
    return get_blue_alliance_api(event, path, key)


def get_event_rankings(event: str,  key: str) -> Any:
    path = f"https://www.thebluealliance.com/api/v3/event/{event}/rankings"
    return get_blue_alliance_api(event, path, key)


def compile_ranking_db(rankings: Any) -> Dict[str, int]:
    db = {}
    for team in rankings["rankings"]:
        db[team['team_key']] = int(team['rank'])
    return db


def get_blue_alliance_data():

    api_key = os.environ.get("X-TBA-Auth-Key")

    results = {}

    for district in ["2017pnw", "2018pnw", "2019pnw", "2022pnw", "2023pnw", "2024pnw"]:
        for event in get_event_keys(district, api_key):
            if not event.endswith("pncmp"):
                print(event)
                rankings = compile_ranking_db(get_event_rankings(event, api_key))
                for rank in rankings.values():
                    results.setdefault(rank, {}).setdefault(0, []).append(-1)
                for alliance in get_event_alliances(event, api_key):
                    print(alliance["name"])
                    alliance_number = int(alliance["name"].split()[-1])
                    for i, pick in enumerate(alliance["picks"]):
                        if pick in rankings:
                            rank = rankings[pick]
                            print(alliance_number, rank)
                            results.setdefault(rank, {}).setdefault(alliance_number, []).append(i)
                            results[rank][0].pop()

    print("Blue Alliance Data")
    pprint(results)
    print()

    return results


if __name__ == "__main__":
    alliance_selection_data = get_blue_alliance_data()
    with open("alliance_selection_data.json", "w") as json_file:
        json.dump(alliance_selection_data, json_file, indent=4)
