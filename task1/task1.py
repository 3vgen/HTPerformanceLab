import sys
from concurrent.futures import (
    ProcessPoolExecutor,
)  # Для обработки двух массивов одновременно в разных процессах


def circular_traversal(n, m):

    if n <= 0 or m <= 0:
        return []

    arr = [i + 1 for i in range(n)]
    result = []

    start = 0
    while True:

        result.append(arr[start])

        last = (start + m - 1) % n
        if last == 0:
            break

        start = last

    return result


def main():
    if len(sys.argv) != 5:
        print("Корректное использование: python task1.py n1 m1 n2 m2")
        return

    try:
        n1 = int(sys.argv[1])
        m1 = int(sys.argv[2])
        n2 = int(sys.argv[3])
        m2 = int(sys.argv[4])
    except ValueError:
        print("Аргументы должны быть целыми числами")
        return

    with ProcessPoolExecutor(max_workers=2) as executor:
        future1 = executor.submit(circular_traversal, n1, m1)
        future2 = executor.submit(circular_traversal, n2, m2)
        path1 = future1.result()
        path2 = future2.result()

    print("".join(str(x) for x in (path1 + path2)))


if __name__ == "__main__":
    main()
