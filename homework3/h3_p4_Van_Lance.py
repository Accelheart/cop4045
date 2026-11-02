# Lance Van Z23504457
# a)

def ed_read(filename: str, from_: int = 0, to: int = -1) -> str:
    """Reads text from a file between two indices.

    Preconditions: from_ and to must be valid integer indices.
    Returns the selected text without modifying the file.
    Raises IndexError if an index exceeds the file length.
    """
    with open(filename, "r", encoding="utf-8") as file:
        content = file.read()

    if from_ < 0 or from_ > len(content):
        raise IndexError("Starting index is out of range")
    if to != -1 and (to < 0 or to > len(content)):
        raise IndexError("Ending index is out of range")

    if to == -1:
        return content[from_:]

    return content[from_:to]


def ed_find(filename: str, search_str: str) -> list[int]:
    """Find all starting positions of a substring in a file.

    Returns a list of indices, including overlapping matches.
    Returns an empty list when the substring is not found.
    Does not modify the file.
    """
    if not search_str:
        raise ValueError("Search string cannot be empty")

    with open(filename, "r", encoding="utf-8") as file:
        content = file.read()

    positions = []
    start = 0

    while True:
        index = content.find(search_str, start)
        if index == -1:
            break
        positions.append(index)
        start = index + 1

    return positions


def ed_replace(filename: str, search_str: str,
               replace_with: str, occurrence: int = -1) -> int:
    """Replaces all or one occurrence of a substring in a file.

    occurrence=-1 replaces all non-overlapping occurrences.
    Otherwise, occurrence is a zero-based match index.
    Returns the number of replacements performed.
    """
    if not search_str:
        raise ValueError("Search string cannot be empty")
    if occurrence < -1:
        raise ValueError("Invalid occurrence index")

    with open(filename, "r", encoding="utf-8") as file:
        content = file.read()

    if occurrence == -1:
        new_content = content.replace(search_str, replace_with)
        count = content.count(search_str)
    else:
        positions = []
        start = 0

        while True:
            index = content.find(search_str, start)
            if index == -1:
                break
            positions.append(index)
            start = index + len(search_str)

        if occurrence >= len(positions):
            return 0

        index = positions[occurrence]
        new_content = (content[:index] + replace_with
                       + content[index + len(search_str):])
        count = 1

    if count > 0:
        with open(filename, "w", encoding="utf-8") as file:
            file.write(new_content)

    return count


def ed_append(filename: str, string: str) -> int:
    """Appends a string to a file, creating it if necessary.

    Returns the number of characters appended.
    File I/O errors goes to the caller.
    """
    with open(filename, "a", encoding="utf-8") as file:
        file.write(string)

    return len(string)


# b)

def testif(condition: bool, success: str, failure: str) -> None:
    """Prints a success or failure message for a test."""
    if condition:
        print(success)
    else:
        print(failure)


def test_ed_find() -> None:
    """Tests substring searching and missing matches."""
    filename = "test_find.txt"

    with open(filename, "w", encoding="utf-8") as file:
        file.write("abc abc abc")

    testif(ed_find(filename, "abc") == [0, 4, 8],
           "ed_find multiple matches works",
           "ed_find multiple matches failed")

    testif(ed_find(filename, "xyz") == [],
           "ed_find missing string works",
           "ed_find missing string failed")

    testif(ed_find(filename, "bc") == [1, 5, 9],
           "ed_find substring works",
           "ed_find substring failed")


def test_ed_replace() -> None:
    """Tests replacing all, one, and nonexistent occurrences."""
    filename = "test_replace.txt"

    with open(filename, "w", encoding="utf-8") as file:
        file.write("cat dog cat dog")

    count = ed_replace(filename, "cat", "bird", 1)

    testif(count == 1 and ed_read(filename) == "cat dog bird dog",
           "ed_replace indexed replacement works",
           "ed_replace indexed replacement failed")

    count = ed_replace(filename, "dog", "fish")

    testif(count == 2 and ed_read(filename) == "cat fish bird fish",
           "ed_replace all works",
           "ed_replace all failed")

    count = ed_replace(filename, "xyz", "abc")

    testif(count == 0,
           "ed_replace missing string works",
           "ed_replace missing string failed")

    count = ed_replace(filename, "cat", "bird", 10)

    testif(count == 0,
           "ed_replace out-of-range occurrence works",
           "ed_replace out-of-range occurrence failed")


# c)

def main() -> None:
    """Demonstrates the editor functions and run their tests."""
    filename = "file1.txt"

    print("=== Text Editor Demonstration ===")

    ed_append(filename, "0123456789")
    ed_append(filename, "0123456789")

    print("Full file:", ed_read(filename))
    print("Read indices 3 to 9:", ed_read(filename, 3, 9))
    print("Read from index 3:", ed_read(filename, 3))

    print("Find 345:", ed_find(filename, "345"))
    print("Find 356:", ed_find(filename, "356"))

    print("Replacements:", ed_replace(filename, "345", "ABCDE", 1))
    print("After replacement:", ed_read(filename))

    print("Replacements:", ed_replace(filename, "345", "ABCDE"))
    print("After replacement:", ed_read(filename))

    print("\n=== Testing ed_find ===")
    test_ed_find()

    print("\n=== Testing ed_replace ===")
    test_ed_replace()


if __name__ == "__main__":
    main()
