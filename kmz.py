from argparse import ArgumentParser, RawTextHelpFormatter
from util import KMZ

VERSION = "1.1.0"

parser = ArgumentParser(prog="kmz", usage="%(prog)s [options]", description="Coordinates to kmz format", formatter_class=RawTextHelpFormatter)
parser.add_argument("-n", "--name", type=str, help="The name shows on the pin", metavar="NAME", dest="name", default="")
parser.add_argument("-x", required=True, type=float, help="X coordinate (longitude;horizontal)", metavar="X", dest="x")
parser.add_argument("-y", required=True, type=float, help="Y coordinate (latitude;vertical)", metavar="Y", dest="y")
parser.add_argument("-z", required=False, type=float, help="Z coordinate (altitude;depth)", metavar="Z", dest="z",
                    default=0)
parser.add_argument("--encoding", required=False, type=str, help="Encoding type of inner kml file", dest="encoding",
                    default="utf-8")
parser.add_argument("--datafile", required=False, type=str, help="Name of the kml file inside the compressed kmz",
                    metavar="NAME.kml", dest="datafile", default="data.kml")
parser.add_argument("--kml", required=False, help="Output the kml file to a filename", metavar="NAME.kml",
                    dest="kml_save")
parser.add_argument("-v", "--version", action="version", help="Show tool version", dest="version",
                    version=f"%(prog)s {VERSION} 2023-03-10")
parser.add_argument("output", type=str, help="Output filename")
parser.epilog = """\n
Example:
    %(prog)s location.kmz -x 0.0 -y 0.0
    %(prog)s location.kmz -x 0.0 -y 0.0 -z 0.0
    %(prog)s location.kmz -x 0.0 -y 0.0 -n \"My Work\"
    %(prog)s location.kmz -x 0.0 -y 0.0 --kml work.kml
"""
args = parser.parse_args()

try:
    kmz = KMZ(args.output)

    kmz.add_point(name=args.name, x=args.x, y=args.y, z=args.z)

    if args.kml_save:
        with open(args.kml_save, "w") as save_to:
            save_to.write(kmz.get_kml())

    kmz.save(args.datafile, args.encoding)
except Exception as error:
    print("[-]", error)
