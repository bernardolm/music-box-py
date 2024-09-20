from pprint import pprint
import datetime
import os

from dotenv import load_dotenv
from github import Github, Auth, InputFileContent
import requests


def get_env(key: str, default=None):
    val = os.getenv(key)

    if val is None or len(val) == 0:
        val = default

    return val


def get_config():
    load_dotenv()

    cfg = {
        "bar_empty_symbol": get_env("BAR_EMPTY_SYMBOL", "⣀"),
        "bar_filled_symbol": get_env("BAR_FILLED_SYMBOL", "⣿"),
        "bar_width": get_env("BAR_WIDTH", 20),
        "debug": bool(get_env("DEBUG", False)),
        "github_gist_id": get_env("GH_GIST_ID"),
        "github_token": get_env("GH_TOKEN"),
        "header_decoration": get_env("HEADER_DECORATION", "-"),
        "lastfm_api_key": get_env("LASTFM_API_KEY"),
        "lastfm_api_url": get_env(
            "lastfm_api_url",
            "http://ws.audioscrobbler.com/2.0/?method=user.gettopartists&format=json",
        ),
        "lastfm_limit": get_env("LASTFM_LIMIT", 10),
        "lastfm_period": get_env("LASTFM_PERIOD", "7day"),
        "lastfm_username": get_env("LASTFM_USERNAME"),
        "lines_width": get_env("LINES_WIDTH", 51),
        "plays_prefix": get_env("PLAYS_PREFIX", " "),
        "plays_sufix": get_env("PLAYS_SUFIX", ""),
        "plays_width": get_env("PLAYS_WIDTH", 4),
        "spaces_width": get_env("SPACES_WIDTH", 1),
    }

    if cfg["debug"]:
        print("config loaded:")
        pprint(cfg)

    cfg["bar_width_fraction"] = cfg["bar_width"] / 100
    cfg["space"] = " " * cfg["spaces_width"]

    return cfg


def sum_total_play_count(top_artists: dict) -> int:
    total_play_count = 0

    for artist in top_artists:
        play_count = int(artist["playcount"])
        total_play_count += play_count
        artist["playcount_int"] = play_count

    return total_play_count


def build_lastfm_url() -> str:
    url = config["lastfm_api_url"]
    url += f"&api_key={config['lastfm_api_key']}"
    url += f"&limit={config['lastfm_limit']}"
    url += f"&period={config['lastfm_period']}"
    url += f"&user={config['lastfm_username']}"
    return url


def get_top_artists() -> dict:
    url = build_lastfm_url()

    if config["debug"]:
        print(f"downloading from url: {url}")

    res = requests.get(url)

    if res.status_code != 200:
        raise Exception(f"{res.status_code} status code was returned from last.fm API")

    return res.json()["topartists"]["artist"]


def build_header(total_play_count: int) -> str:
    header = f" {total_play_count} plays".rjust(
        config["lines_width"] - 3, config["header_decoration"]
    )

    return f"{header} {config['header_decoration'] * 2}"


def build_name(artist: dict, name_width: int) -> str:
    name = artist["name"]
    name_width -= config["spaces_width"]

    if len(name) >= name_width:
        return name[:name_width]

    return name.rjust(name_width)


def build_bar(artist: dict, total_play_count: int) -> str:
    play_count = artist["playcount_int"]

    percent = play_count / total_play_count
    percent = percent * 100

    bar_filled_size = round(percent * config["bar_width_fraction"])
    bar_filled = config["bar_filled_symbol"] * bar_filled_size

    bar = bar_filled.ljust(config["bar_width"], config["bar_empty_symbol"])

    return bar


def build_plays(artist: dict) -> str:
    play_count = artist["playcount_int"]
    plays = str(play_count)
    plays = plays.rjust(config["plays_width"], config["plays_prefix"])

    if len(config["plays_sufix"]) > 0:
        return plays + config["space"] + config["plays_sufix"]

    return plays


def build_content(top_artists: dict, total_play_count: int) -> str:
    content = ""

    for artist in top_artists:
        bar = build_bar(artist, total_play_count)
        plays = build_plays(artist)

        line = config["space"].join([bar, plays])

        name_width = config["lines_width"] - len(line)
        name = build_name(artist, name_width)

        line = config["space"].join([name, line])
        content += line + "\n"

        if config["debug"]:
            print(line)

    return content


def save_gist_content(content: str, description: str):
    auth = Auth.Token(config["github_token"])
    g = Github(auth=auth)
    gist = g.get_gist(id=config["github_gist_id"])

    filename = "gistfile1.txt"

    if gist.files is not None:
        filename = next(iter(gist.files))

    now = datetime.datetime.now()

    gist.edit(
        description=description,
        files={filename: InputFileContent(content)},
    )

    g.close()


def main():
    top_artists = get_top_artists()

    total_play_count = sum_total_play_count(top_artists)

    if config["debug"]:
        header = build_header(total_play_count)
        print(header)

    description = (
        f"🎶 music box: {total_play_count} plays in the last {config['lastfm_period']}"
    )

    if config["debug"]:
        print(description)

    content = build_content(top_artists, total_play_count)

    save_gist_content(content, description)


config = get_config()

main()
