import sys
import argparse
import os


class Ellipse:
    def __init__(self, x0, y0, a, b):
        self.x0 = x0
        self.y0 = y0
        self.a = a
        self.b = b

    @classmethod
    def from_file(cls, file_path):

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Файл эллипса не найден: {file_path}")
        try:
            with open(file_path) as f:
                line1 = f.readline().split()
                x0 = float(line1[0])
                y0 = float(line1[1])

                line2 = f.readline().split()
                a = float(line2[0])
                b = float(line2[1])

        except IndexError:
            raise ValueError(f"Некорректный формат файла эллипса: {file_path}")

        except ValueError:
            raise ValueError(f"Некорректные числа в файле эллипса: {file_path}")

        return cls(x0, y0, a, b)

    def contains(self, point):

        x, y = point.x, point.y
        result = (x - self.x0) ** 2 / self.a**2 + (y - self.y0) ** 2 / self.b**2

        if result == 1:
            return 0
        if result < 1:
            return 1
        else:
            return 2


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    @classmethod
    def read_points(cls, file_path):

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Файл с точками не найден: {file_path}")

        points = []
        with open(file_path) as f:
            for line_num, line in enumerate(f, start=1):
                line = line.strip()
                if line == "":
                    continue
                parts = line.split()
                if len(parts) != 2:
                    raise ValueError(
                        f"Некорректная строка {line_num} в файле точек: {line}"
                    )
                try:
                    x = float(parts[0])
                    y = float(parts[1])
                except ValueError:
                    raise ValueError(
                        f"Невозможно преобразовать координаты в числа в строке {line_num}: {line}"
                    )
                points.append(cls(x, y))
        return points


class EllipseAnalyzer:
    def __init__(self, ellipse_file, points_file):
        self.ellipse = Ellipse.from_file(ellipse_file)
        self.points = Point.read_points(points_file)

    def analyze(self):

        for point in self.points:
            print(self.ellipse.contains(point))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--ellipse", required=True, help="Файл с координатами эллипса")
    parser.add_argument("--points", required=True, help="Файл с координатами точек")
    args = parser.parse_args()

    try:
        analyzer = EllipseAnalyzer(args.ellipse, args.points)
        analyzer.analyze()
    except Exception as e:
        print(f"Ошибка: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
