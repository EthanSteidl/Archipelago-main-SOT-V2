import time

from worlds.seaofthieves.Client.windowcapture import WindowCapture
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--interval', dest='interval', type=int, help='ip address : port of host')
parser.add_argument('--count', dest='count', type=int, help='Player ship name')
parser.add_argument('--prefix', dest='prefix', type=str, help='Player ship name')
parser.add_argument('--output_dir', dest='output_dir', type=str,
                    help='Microsoft login cookie given to www.seaofthieves.com', nargs='+')
args = parser.parse_args()
interval = int(args.interval)
count = int(args.count)
prefix = str(args.prefix)
output_dir = str(args.output_dir[0])


windowCapture = WindowCapture()



for i in range(count):
    time.sleep(interval)

    #using 240p

    rgb_image = windowCapture.get_screenshot_right_hand()
    fname = "{}\\{}{}.png".format(output_dir,prefix, i)
    rgb_image.save(fname)