import os

import requests

import override

# Этот файл взаимодействует с Steam Web API для получения инфы о игре и игроке

api_key = os.getenv("STEAM_API_KEY")


def arrtostring(arr):
    if len(arr) > 1:
        return ", ".join(arr)
    else:
        return str(arr[0])


def get_progress(sid, gid):
    url = "http://api.steampowered.com/ISteamUserStats/GetUserStatsForGame/v0002/"
    params = {"key": api_key, "steamid": sid, "appid": gid}
    response1 = requests.get(url, params=params)

    url2 = "http://api.steampowered.com/ISteamUserStats/GetSchemaForGame/v2/"
    params2 = {"key": api_key, "appid": gid}

    try:
        response2 = requests.get(url2, params=params2)
    except:
        return "Error fetching schema"

    try:
        return f"{sum(1 for achievement in response1.json()['playerstats']['achievements'] if achievement['achieved'] == 1)}:{len(response2.json()['game']['availableGameStats']['achievements'])}"
    except KeyError:
        return (
            f"0:{len(response2.json()['game']['availableGameStats']['achievements'])}"
        )


def get_game(gid):
    url = f"https://store.steampowered.com/api/appdetails?appids={gid}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    }
    response = requests.get(url, headers)
    data = response.json()

    return {
        "name": data[f"{gid}"]["data"]["name"],
        "developer": arrtostring(data[f"{gid}"]["data"]["developers"]),
    }


def get_image(gid):
    return {
        "hero": f"https://steamcdn-a.akamaihd.net/steam/apps/{gid}/hero_capsule.jpg",
        "icon": f"https://steamcdn-a.akamaihd.net/steam/apps/{gid}/community_icon.jpg",  # <---- не работает бтв, вырежу/заменю позже
    }


def get_player(sid):
    url = "http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/"
    params = {"key": api_key, "steamids": sid}
    response = requests.get(url, params=params)
    return {
        "name": response.json()["response"]["players"][0]["personaname"],
        "avatar": response.json()["response"]["players"][0]["avatarfull"],
    }


if __name__ == "__main__":
    print(get_game(250900))
    print(get_progress(76561199091628137, 250900))
    print(get_image(250900))
    print(get_player(76561199091628137))
