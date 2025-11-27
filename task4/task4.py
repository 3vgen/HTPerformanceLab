import sys


def min_moves(nums, max_moves=20):
    if not nums:
        return 0

    nums_sorted = sorted(nums)  # в случае, еси массив не отсортирован
    n = len(nums_sorted)
    median = nums_sorted[n // 2]  # медиана

    total_moves = 0
    for num in nums:
        total_moves += abs(num - median)

    if total_moves <= max_moves:
        return total_moves
    else:
        return None


def main():
    if len(sys.argv) != 2:
        print("Использование: python task4.py <имя_файла>")
        sys.exit(1)

    filename = sys.argv[1]

    try:
        with open(filename, "r", encoding="utf-8") as f:
            nums = []
            for line in f:
                line = line.strip()
                if line:
                    nums.append(int(line))

        if not nums:
            print("Файл пустой")
            return

        result = min_moves(nums, max_moves=20)

        if result is not None:
            print(result)
        else:
            print(
                "20 ходов недостаточно для приведения всех элементов массива к одному числу"
            )

    except FileNotFoundError:
        print(f"Файл {filename} не найден")
    except ValueError:
        print("В файле должны быть только целые числа")
    except Exception as e:
        print(f"Ошибка {e}")


if __name__ == "__main__":
    main()
