import src.gameutil as gameutil
import src.geoapi as geoapi
import sys

def main():
    if (len(sys.argv) <= 1):
        print("引数に都道府県名を指定してください。")
        exit(1)
    pref = geoapi.GeoAPIInterface(sys.argv[1])
    gameutil.city_name_guesser(pref)

if __name__ == "__main__":
    main()
