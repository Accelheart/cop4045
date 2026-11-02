"""Estimate storage usage for files and nested folders."""

from __future__ import annotations


class Entry:
	"""Base class for an item in a storage hierarchy."""

	def __init__(self, name: str, parent: Entry | None = None) -> None:
		"""Initialize an entry with its name and optional parent."""
		self.name: str = name
		self._parent: Entry | None = parent

	def parent(self) -> Entry | None:
		"""Return this entry's parent, or None when it is a root."""
		return self._parent

	def absolute_path(self) -> list[Entry]:
		"""Return this entry and its ancestors, ending at the root."""
		parent = self.parent()
		if parent is None:
			return [self]
		return [self] + parent.absolute_path()

	def size(self) -> int:
		"""Return this entry's size in bytes."""
		raise NotImplementedError("Entry subclasses must implement size")


class File(Entry):
	"""A file occupying a fixed number of bytes."""

	def __init__(self, name: str, parent: Entry | None,
				 bytes_used: int) -> None:
		"""Initialize a file and reject negative or non-integer sizes."""
		super().__init__(name, parent)
		if not isinstance(bytes_used, int):
			raise TypeError("bytes_used must be an integer")
		if bytes_used < 0:
			raise ValueError("bytes_used cannot be negative")
		self.bytes_used: int = bytes_used

	def size(self) -> int:
		"""Return the number of bytes used by this file."""
		return self.bytes_used


class Folder(Entry):
	"""A folder containing files and other folders."""

	def __init__(self, name: str, parent: Entry | None = None) -> None:
		"""Initialize an empty folder with an optional parent."""
		super().__init__(name, parent)
		self._children: list[Entry] = []

	def add(self, entry: Entry) -> None:
		"""Add an entry to this folder and set its parent to this folder."""
		if not isinstance(entry, Entry):
			raise TypeError("entry must be an Entry")
		entry._parent = self
		self._children.append(entry)

	def children(self) -> tuple[Entry, ...]:
		"""Return this folder's children as an immutable tuple."""
		return tuple(self._children)

	def size(self) -> int:
		"""Return the combined size of all files in this folder tree."""
		return sum(entry.size() for entry in self._children)


def find_large_files(entry: Entry, minimum_size: int) -> list[File]:
	"""Find files at least minimum_size bytes starting at entry.

	For a File, return a one-item list if it meets the threshold, or an
	empty list otherwise. For a Folder, recursively search its children
	and return only matching File objects; folders are never returned.
	"""
	if isinstance(entry, File):
		return [entry] if entry.size() >= minimum_size else []
	if isinstance(entry, Folder):
		return [file for child in entry.children()
				for file in find_large_files(child, minimum_size)]
	raise TypeError("entry must be a File or Folder")


def total_size(entries: list[Entry]) -> int:
	"""Sum entry sizes through the common Entry interface."""
	return sum(entry.size() for entry in entries)


def main() -> None:
	"""Demonstrate recursive sizes and polymorphic size calculation."""
	root = Folder("university")
	documents = Folder("documents", root)
	documents.add(File("catalog.pdf", documents, 1_200_000))
	documents.add(File("schedule.csv", documents, 18_000))
	root.add(documents)

	research = Folder("research", root)
	archive = Folder("archive", research)
	dataset = File("dataset.bin", archive, 8_500_000)
	archive.add(dataset)
	archive.add(File("notes.txt", archive, 4_000))
	research.add(archive)
	root.add(research)
	root.add(File("readme.txt", root, 2_000))

	entries: list[Entry] = [root]
	print(f"University folder: {root.size():,} bytes")
	print(f"All entries: {total_size(entries):,} bytes")
	path_names = [entry.name for entry in dataset.absolute_path()]
	print("Dataset absolute path (entry to root):", " -> ".join(path_names))


if __name__ == "__main__":
	main()
