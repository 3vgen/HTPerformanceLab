import json
import argparse
import sys
from typing import List, Dict, Any


class TestTree:
    @classmethod
    def from_file(cls, path: str):
        if (
            not sys.path.__contains__(path)
            and not open(path, "r", encoding="utf-8").__enter__()
        ):
            raise FileNotFoundError(f"Файл не найден: {path}")
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            return data["tests"]
        except json.JSONDecodeError as e:
            raise ValueError(f"Некорректный JSON в {path}: {e}")
        except KeyError:
            raise ValueError(f"В {path} нет обязательного поля 'tests'")


class ValuesMap:
    @classmethod
    def from_file(cls, path: str):
        if not open(path, "r", encoding="utf-8").__enter__():
            raise FileNotFoundError(f"Файл не найден")
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            return {
                item["id"]: item["value"] for item in data["values"]
            }  # из спика словарей делаю единый словарь
        except json.JSONDecodeError as e:
            raise ValueError(f"Некорректный JSON в {path}: {e}")
        except KeyError:
            raise ValueError(f"В {path} нет обязательного поля values")
        except TypeError:
            raise ValueError(f"Поле values в {path} должно быть списком")


class TestMerger:
    def __init__(self, tests_file: str, values_file: str):
        self.tests = TestTree.from_file(tests_file)
        self.values_dict = ValuesMap.from_file(values_file)

    def merge(self):
        stack = [self.tests]
        while stack:
            current_level = stack.pop()
            for obj in current_level:

                if obj.get("id") in self.values_dict:
                    obj["value"] = self.values_dict[obj["id"]]

                if "values" in obj:
                    stack.append(obj["values"])

    def save(self, output_file: str):
        result = {"tests": self.tests}
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=4)


def main():
    parser = argparse.ArgumentParser(
        description="Заполняет value в tests.json по values.json"
    )
    parser.add_argument("--tests", default="tests.json", help="тесты любой вложенности")
    parser.add_argument("--values", default="values.json", help="результаты тестов")
    parser.add_argument("--output", default="output.json", help="куда сохранить")
    args = parser.parse_args()

    try:
        merger = TestMerger(args.tests, args.values)
        merger.merge()
        merger.save(args.output)
    except Exception as e:
        print(f"Ошибка: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
