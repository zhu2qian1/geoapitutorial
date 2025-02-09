class Prefecture:
    Response: dict[str, Location]
    class Location:
        data: tuple[CityInfo]
        class CityInfo:
            data: dict[str, str]
