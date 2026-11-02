"""Test storage entries using printed success and failure messages."""

if __package__:
	from .h3_p6_Van_Lance import File, Folder, find_large_files
else:
	from h3_p6_Van_Lance import File, Folder, find_large_files


def testif(b: bool, testname: str, msgOK: str = "",
		   msgFailed: str = "") -> bool:
	"""Print a test result and return whether the condition passed.

	Args:
		b: True when the tested condition passes.
		testname: Name of the test being reported.
		msgOK: Message printed when the test passes.
		msgFailed: Message printed when the test fails.

	Returns:
		The value of b.
	"""
	if b:
		print("Success: " + testname + "; " + msgOK)
	else:
		print("Failed: " + testname + "; " + msgFailed)
	return b


def test_file_thresholds() -> bool:
	"""Test find_large_files() when the starting entry is a File."""
	matching_file = File("matching.bin", None, 100)
	small_file = File("small.bin", None, 99)
	checks = [
		testif(find_large_files(matching_file, 100) == [matching_file],
			   "File meets threshold", "matching file returned",
			   "matching file was not returned"),
		testif(find_large_files(small_file, 100) == [],
			   "File below threshold", "no file returned",
			   "small file was returned"),
	]
	return all(checks)


def test_nested_folder_search() -> bool:
	"""Test recursive file search and result order in a folder."""
	root = Folder("root")
	nested = Folder("nested")
	first_file = File("first.bin", None, 200)
	small_file = File("small.bin", None, 10)
	last_file = File("last.bin", None, 100)
	root.add(first_file)
	root.add(nested)
	nested.add(small_file)
	nested.add(last_file)
	return testif(
		find_large_files(root, 100) == [first_file, last_file],
		"Nested folder search", "matching files returned in order",
		"search results did not match",
	)


def test_empty_folder_search() -> bool:
	"""Test that searching an empty folder returns no files."""
	return testif(
		find_large_files(Folder("empty"), 0) == [],
		"Empty folder search", "no files returned",
		"unexpected files returned",
	)


def test_deep_folder_size_and_search() -> bool:
	"""Test recursive size and two search thresholds in nested folders."""
	outer = Folder("outer")
	middle = Folder("middle")
	inner = Folder("inner")
	outer_file = File("outer.bin", None, 50)
	middle_file = File("middle.bin", None, 250)
	inner_file = File("inner.bin", None, 750)
	largest_file = File("largest.bin", None, 1_500)
	outer.add(outer_file)
	outer.add(middle)
	middle.add(middle_file)
	middle.add(inner)
	inner.add(inner_file)
	inner.add(largest_file)
	checks = [
		testif(outer.size() == 2_550, "Deep folder size",
			   "outer size includes all descendants",
			   "outer size did not include all descendants"),
		testif(find_large_files(outer, 250) ==
			   [middle_file, inner_file, largest_file],
			   "Search at 250 bytes", "expected files returned",
			   "unexpected files returned"),
		testif(find_large_files(outer, 750) == [inner_file, largest_file],
			   "Search at 750 bytes", "expected files returned",
			   "unexpected files returned"),
		testif(largest_file.absolute_path() ==
			   [largest_file, inner, middle, outer],
			   "Deep absolute path", "entry-to-root order is correct",
			   "entry-to-root order is incorrect"),
	]
	return all(checks)


def test_absolute_paths() -> bool:
	"""Test absolute_path() for a root and a nested file."""
	root = Folder("root")
	nested = Folder("nested")
	file_entry = File("report.txt", None, 20)
	root.add(nested)
	nested.add(file_entry)
	checks = [
		testif(root.absolute_path() == [root], "Root absolute path",
			   "root is the only path entry",
			   "root path contains unexpected entries"),
		testif(file_entry.absolute_path() == [file_entry, nested, root],
			   "File absolute path", "file and ancestors returned in order",
			   "file path order is incorrect"),
	]
	return all(checks)


def run_tests() -> bool:
	"""Run all storage-entry tests and return whether they all passed."""
	results = [
		test_file_thresholds(),
		test_nested_folder_search(),
		test_empty_folder_search(),
		test_deep_folder_size_and_search(),
		test_absolute_paths(),
	]
	passed = all(results)
	print("All tests passed." if passed else "Some tests failed.")
	return passed


if __name__ == "__main__":
	if not run_tests():
		raise SystemExit(1)