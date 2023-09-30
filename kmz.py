from simplekml import Kml
from argparse import ArgumentParser

parser = ArgumentParser(prog="kmz", usage="$(prog)s [options]", description="Coordinates to kmz format")
parser.add_argument("-n", "--name", type=str, help="The name shows on the pin", metavar="NAME", dest="name")
parser.add_argument("-x", required=True, type=float, help="x coordinate", metavar="X", dest="x")
parser.add_argument("-y", required=True, type=float, help="y coordinate", metavar="Y", dest="y")
parser.add_argument("output", type=str, help="Output filename")
args = parser.parse_args()

try:
    kml = Kml()

    # Add placemarks to the KML object
    kml.newpoint(name=args.name, coords=[(args.x, args.y)])

    # Save the KML object as a KMZ file
    kml.savekmz(args.output)
except Exception as error:
    print("[-]", error)