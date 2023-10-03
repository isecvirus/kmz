"""
@author=virus
@version=1.0.0
"""

import hashlib
import random
from zipfile import ZipFile, ZIP_DEFLATED

DATAFILE = "data.kml"
ENCODING = "utf-8"

class Point(dict):
    def set_name(self, name: float) -> None:
        self['name'] = name

    def get_name(self) -> str:
        return self['name']

    def set_x(self, x: float) -> None:
        self['x'] = x

    def get_x(self) -> float:
        return self['x']

    def set_y(self, y: float) -> None:
        self['y'] = y

    def get_y(self) -> float:
        return self['y']

    def set_z(self, z: float) -> None:
        self['z'] = z

    def get_z(self) -> float:
        return self['z']

    def get_hash(self):
        return self

class KMZ:
    """ XML Format
    <?xml version="1.0" encoding="UTF-8"?>
    <kml project="kmz" author="virus">
        <Document>
            <Placemark id="xxxx-xxxx-xxxx-xxxx-xxxx">
                <name> ... </name>
                <Point>
                    <coordinates>x,y,z</coordinates>
                </Point>
            </Placemark>
            ...
        </Document>
    </kml>
    """

    def __init__(self, filename: str):
        self.filename: str = filename
        self.points: {str: Point} = {}

    def add_point(self, x: float, y: float, z: float = 0.0, name: str = ""):
        id = self.generate_id()
        data = Point({"name": name, "x": x, "y": y, "z": z})

        if not data in self.points.values():
            self.points[id] = data

    def get_points(self) -> dict:
        return self.points

    def get_kml(self) -> str:
        # add opening header
        data = (
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            '<kml project="kmz" author="virus">\n'
            '<Document>\n'
        )

        for point in self.points:
            name = str(self.points[point].get_name())
            x = float(self.points[point].get_x())
            y = float(self.points[point].get_y())
            z = float(self.points[point].get_z())

            # add point to data
            data += (
                f'\t<Placemark id="{point}">\n'
                f'\t\t<name>{name}</name>\n'
                f'\t\t<Point>\n'
                f'\t\t\t<coordinates>{x},{y},{z}</coordinates>\n'
                f'\t\t</Point>\n'
                f'\t</Placemark>\n'
            )

        # add closing footer
        data += (
            '</Document>\n'
            '</kml>'
        )

        return data

    def get_point(self, id: str) -> Point:
        if id in self.points:
            return self.points[id]

    def save(self, datafile: str = DATAFILE, encoding:str=ENCODING):
        with ZipFile(self.filename, "w", ZIP_DEFLATED) as data_file:
            data_file.writestr(
                datafile,
                self.get_kml().encode(
                    encoding=encoding,
                    errors="replace"
                )
            )

    @staticmethod
    def generate_id(bits: int = 128):
        rand_bits = random.getrandbits(bits)

        rand_id = hashlib.sha1(
            str(rand_bits).encode()
        ).hexdigest()[20:]

        id = "-".join(
            [
                rand_id[i:i + 4] for i in range(0, len(rand_id), 4)
            ]
        )
        return id