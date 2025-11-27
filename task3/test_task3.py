import json
import pytest
from pathlib import Path

from task3 import TestTree, ValuesMap, TestMerger


@pytest.fixture
def temp_dir(tmp_path: Path):
    return tmp_path


def create_file(path: Path, content):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(content, f, ensure_ascii=False, indent=4)


class TestTestTree:
    def test_success(self, temp_dir):
        file = temp_dir / "tests.json"
        create_file(file, {"tests": [{"id": 1, "title": "Root"}]})
        result = TestTree.from_file(str(file))
        assert result == [{"id": 1, "title": "Root"}]

    def test_missing_tests_key(self, temp_dir):
        file = temp_dir / "bad.json"
        create_file(file, {"wrong": []})
        with pytest.raises(ValueError, match="нет обязательного поля 'tests'"):
            TestTree.from_file(str(file))

    def test_invalid_json(self, temp_dir):
        file = temp_dir / "broken.json"
        file.write_text("fbadskjfajknfkjsan kjfnakjfnkajdsnf kjakj", encoding="utf-8")
        with pytest.raises(ValueError, match="Некорректный JSON"):
            TestTree.from_file(str(file))


class TestValuesMap:
    def test_success(self, temp_dir):
        file = temp_dir / "values.json"
        create_file(
            file,
            {"values": [{"id": 5, "value": "passed"}, {"id": 10, "value": "failed"}]},
        )
        result = ValuesMap.from_file(str(file))
        assert result == {5: "passed", 10: "failed"}

    def test_file_not_found(self, temp_dir):
        with pytest.raises(FileNotFoundError):
            ValuesMap.from_file(str(temp_dir / "missing.json"))

    def test_missing_values_key(self, temp_dir):
        file = temp_dir / "incorrrect.json"
        create_file(file, {"fsdgdfsgdfsgdfs": []})
        with pytest.raises(ValueError, match="нет обязательного поля values"):
            ValuesMap.from_file(str(file))

    def test_values_not_list(self, temp_dir):
        file = temp_dir / "incorrect.json"
        create_file(file, {"values": "fdsa fads fsda a dsa"})
        with pytest.raises(ValueError, match="должно быть списком"):
            ValuesMap.from_file(str(file))


class TestTestMerger:
    def test_simple_tree_fills_values_correctly(self, temp_dir):
        tests_file = temp_dir / "tests.json"
        create_file(
            tests_file,
            {
                "tests": [
                    {"id": 1, "title": "Тест 1"},
                    {
                        "id": 2,
                        "title": "Группа",
                        "values": [{"id": 3, "title": "Вложенный"}],
                    },
                ]
            },
        )

        values_file = temp_dir / "values.json"
        create_file(
            values_file,
            {"values": [{"id": 1, "value": "passed"}, {"id": 3, "value": "failed"}]},
        )

        merger = TestMerger(str(tests_file), str(values_file))
        merger.merge()

        tests = merger.tests
        assert tests[0]["value"] == "passed"
        assert "value" not in tests[1]
        assert tests[1]["values"][0]["value"] == "failed"
