import json
import os

import requests

import api
from config import config

min, max = api.get_progress(config["sid"], config["gid"]).split(":")

discord = {
    "token": os.getenv("DISCORD_TOKEN"),
    "appid": int(os.getenv("DISCORD_APP_ID")),
    "uid": int(os.getenv("DISCORD_USER_ID")),
}

data = json.dumps(
    {
        "username": f"{config['discord_user']}",
        "data": {
            "dynamic": [
                {
                    "type": 1,  # эту хуету менять надо если меняешь игру, конкретно тут у меня разработчики айзека
                    "name": "subtitle",
                    "value": f"{api.get_game(config['gid'])['developer']}",
                },
                {
                    "type": 1,
                    "name": "title",
                    "value": f"{api.get_game(config['gid'])['name']}",
                },
                {
                    "type": 3,
                    "name": "imageico",
                    "value": {"url": f"{api.get_image(config['gid'])['hero']}"},
                },
                {"type": 1, "name": "objective", "value": f"{int(min) / int(max) * 100:.0f}%"},
                {"type": 2, "name": "curr", "value": int(min)},
                {"type": 2, "name": "max", "value": int(max)},
                {"type": 1, "name": "objdesc", "value": "from 100%"},
                {
                    "type": 1,
                    "name": "ministat",
                    "value": f"{min}/{max} | {int(min) / int(max) * 100:.0f}%",
                },
                {
                    "type": 3,
                    "name": "miniimg",
                    "value": {"url": f"{api.get_image(config['gid'])['hero']}"},
                },
                {"type": 1, "name": "minilabel", "value": f""},
                {
                    "type": 3,
                    "name": "objimage",
                    "value": {"url": f"{api.get_player(config['sid'])['avatar']}"},
                },
            ]
        },
    }
)

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bot {discord['token']}",
    "User-Agent": "DiscordBot (https://github.com/discord/discord-api-docs, 1.0.0)",
}

url = f"https://discord.com/api/v9/applications/{discord['appid']}/users/{discord['uid']}/identities/0/profile"

try:
    response = requests.patch(url, headers=headers, data=data)

    if response.status_code in [200, 201, 204]:
        print("✅ Профиль успешно обновлён")
        print(response.json())
    else:
        print(f"❌ Ошибка {response.status_code}")
        print(response.text)

except Exception as e:
    print(f"Ошибка подключения: {e}")
