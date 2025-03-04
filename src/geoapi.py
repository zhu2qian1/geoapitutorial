from urllib import parse

import json
import requests as req

from pyi.Prefecture import Prefecture

path = ".\\json\\fetched.json"


class GeoAPIInterface:
    """
    Data of cities, towns, and villages in a prefecture.
    Parameters
    --------
    prefecture: str
        The name of the prefecture in kanji.
    Attributes
    --------
    prefecture: str
        The name of prefecture.
    json: dict
        Raw json.
    contents: list
        List of contents in the json.
    dataset: list[tuple]
        List[("name", "name_kana"), ...]
        Optimized for games.
    """

    # todo stop downloading data in __init__
    def __init__(self, prefecture: str):
        """
        Fetch data of GeoAPI.
        """
        if not is_preset(prefecture):
            raise ValueError("The name is not valid.")

        self.prefecture = prefecture
        if has_fetched(prefecture):
            self.json = fetch_pref_data(prefecture)
        else:
            self.response: req.Request = req.get(
                "http://geoapi.heartrails.com/api/json?method=getCities&prefecture="
                + parse.quote(prefecture)
            )
            self.json = self.response.json()

            create_new_json(prefecture, self.json)
            update_fetched_file(prefecture)

        self.contents: list = self.json["response"]["location"]
        self.dataset: list[tuple] = [(i["city"], i["city_kana"]) for i in self.contents]


def fetch_pref_data(prefecture: str) -> Prefecture:
    """
    Fetch prefecture data.
    Parameters
    --------
    prefecture: str
        The name of prefecture in kanji.
    Return
    --------
    d: dict
        Raw json.
    """
    with open(f".\\json\\{prefecture}.json", encoding="utf8") as f:
        d: Prefecture = json.load(f)
    return d


def update_fetched_file(prefecture: str) -> None:
    """
    Update fetched.json.
    """
    with open(path, encoding="utf8") as f:
        d: list = json.load(f)
        d.append(prefecture)
    with open(path, mode="w", encoding="utf8") as f:
        json.dump(d, f, indent=2, ensure_ascii=False)
    return None


def create_new_json(prefecture: str, d: dict) -> None:
    """
    Create a new json file for a new prefecture.
    Parameters
    --------
    prefecture: str
        The name of the prefecture in kanji.
    d: dict
        The dict (json) of the prefecture.
    """
    with open(f".\\json\\{prefecture}.json", mode="w", encoding="utf8") as f:
        json.dump(d, f, indent=2, ensure_ascii=False)
    return None


def has_fetched(prefecture: str) -> bool:
    """
    check if the prefecture has been fetched already.
    """
    with open(path, encoding="utf8") as f:
        d = json.load(f)
    if prefecture in d:
        return True
    return False


def is_preset(pref_name: str) -> bool:
    """
    Check whether the prefecture is valid.
    """
    import json

    with open(".\\json\\prefectures.json", encoding="utf8") as f:
        prefectures: list[str] = json.load(f)
    if pref_name not in prefectures:
        return False
    return True
