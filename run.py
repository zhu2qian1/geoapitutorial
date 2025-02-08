import src.gameutil as gameutil
import src.geoapi as geoapi
import sys

def main():
    pref = geoapi.GeoAPIInterface(sys.argv[1])
    gameutil.city_name_guesser(pref)

if __name__ == "__main__":
    main()
