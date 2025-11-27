import pytest
from pathlib import Path
from task2 import Ellipse, Point, EllipseAnalyzer


class TestEllipse:

    def test_inside_outside_border(self):
        e = Ellipse(0, 0, 5, 3)
        p_inside = Point(0, 0)
        p_border = Point(5, 0)
        p_outside = Point(6, 0)

        assert e.contains(p_inside) == 1
        assert e.contains(p_border) == 0
        assert e.contains(p_outside) == 2

    def test_from_file(self, tmp_path):
        ellipse_file = tmp_path / "ellipse.txt"
        ellipse_file.write_text("0 0\n5 3\n")
        e = Ellipse.from_file(str(ellipse_file))
        assert e.x0 == 0
        assert e.y0 == 0
        assert e.a == 5
        assert e.b == 3

    def test_file_not_found(self, tmp_path):
        with pytest.raises(FileNotFoundError):
            Ellipse.from_file(str(tmp_path / "nonexistent.txt"))


class TestPoint:

    def test_read_points(self, tmp_path):
        points_file = tmp_path / "points.txt"
        points_file.write_text("0 0\n1 2\n3 4\n")
        points = Point.read_points(str(points_file))
        assert len(points) == 3
        assert points[0].x == 0 and points[0].y == 0
        assert points[1].x == 1 and points[1].y == 2
        assert points[2].x == 3 and points[2].y == 4

    def test_invalid_format(self, tmp_path):
        points_file = tmp_path / "points.txt"
        points_file.write_text("0 0\nstr\n")
        with pytest.raises(ValueError):
            Point.read_points(str(points_file))

    def test_file_not_found(self, tmp_path):
        with pytest.raises(FileNotFoundError):
            Point.read_points(str(tmp_path / "nonexistent.txt"))


class TestEllipseAnalyzer:

    def test_analyze_output(self, tmp_path, capsys):
        ellipse_file = tmp_path / "ellipse.txt"
        points_file = tmp_path / "points.txt"

        ellipse_file.write_text("0 0\n5 3\n")
        points_file.write_text("0 0\n5 0\n6 0\n")

        analyzer = EllipseAnalyzer(str(ellipse_file), str(points_file))
        analyzer.analyze()

        captured = capsys.readouterr()
        output_lines = captured.out.strip().split("\n")
        assert output_lines == ["1", "0", "2"]

    def test_analyze_file_not_found(self, tmp_path):
        ellipse_file = tmp_path / "ellipse.txt"
        points_file = tmp_path / "points.txt"

        ellipse_file.write_text("0 0\n5 3\n")
        with pytest.raises(FileNotFoundError):
            EllipseAnalyzer(str(ellipse_file), str(points_file))
