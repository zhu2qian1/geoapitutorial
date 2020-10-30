import json
from urllib import parse

import requests as req


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

    def __init__(self, prefecture: str):
        """
        Fetch data of GeoAPI.
        """
        self.prefecture = prefecture
        if hasfetched(prefecture):
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


def fetch_pref_data(prefecture: str) -> dict:
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
    with open(".\\json\\{}.json".format(prefecture), encoding="utf8") as f:
        d: dict = json.load(f)
    return d


def update_fetched_file(prefecture: str) -> None:
    """
    Update fetched.json.
    """
    with open(".\\json\\fetched.json", encoding="utf8") as f:
        d: list = json.load(f)
        d.append(prefecture)
    with open(".\\json\\fetched.json", mode="w", encoding="utf8") as f:
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


def hasfetched(prefecture: str) -> bool:
    """
    check if the prefecture has been fetched already.
    """
    with open(".\\json\\fetched.json", encoding="utf8") as f:
        d = json.load(f)
    if prefecture in d:
        return True
    return False


def validate(arg: str) -> bool:
    """
    Check whether the prefecture is valid.
    """
    import json

    with open(".\\json\\prefectures.json", encoding="utf8") as f:
        prefectures: list = json.load(f)
    if arg not in prefectures:
        return False
    return True
