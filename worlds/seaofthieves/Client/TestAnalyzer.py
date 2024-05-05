
import argparse
import os
import time

import SOTDataAnalyzer
import UserInformation
from worlds.seaofthieves.Locations.LocationCollection import LocationDetailsCollection, LocDetails
import typing
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--ship', dest='ship', type=str, help='Player ship name')
    parser.add_argument('--mscookie', dest='msCookie', type=str,
                        help='Microsoft login cookie given to www.seaofthieves.com', nargs='+')
    args = parser.parse_args()
    real_cookie = ""
    if args.msCookie is not None:
        filepath = args.msCookie[0]
        while not os.path.exists(filepath):
            filepath = input('File not found. Enter an absolute Filepath to a text file containing your mscookie : ')
        file = open(filepath, "r")
        real_cookie = str(file.read())
        file.close()

    crds = UserInformation.SotLoginCredentials(real_cookie)
    analyzer_dets = UserInformation.SotAnalyzerDetails(args.ship,None)
    userInfo: UserInformation.UserInformation = UserInformation.UserInformation(crds, analyzer_dets, "fake", "fake")
    analyzer: SOTDataAnalyzer.SOTDataAnalyzer = SOTDataAnalyzer.SOTDataAnalyzer(userInfo, 1)

    locationCollection = LocationDetailsCollection()
    locs: typing.List[LocDetails] = locationCollection.findDetailsCheckable(set(), True)

    #id to locDet
    mappings = {}
    for loc in locs:
        analyzer.allowTrackingOfLocation(loc)
        mappings[loc.id] = loc

    while True:
        analyzer.update()
        completedChecks: typing.Dict[int, bool] = analyzer.getAllCompletedChecks()
        for k in completedChecks.keys():
            if completedChecks[k]:
                print("Completed -> " + str(mappings[k].name))
                analyzer.stopTracking(k)

        time.sleep(1)


if __name__ == '__main__':
    main()