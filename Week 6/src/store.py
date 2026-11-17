"""Week 6: Text and binary file I/O examples with context managers."""


def test_write() -> None:
    """Write and read UTF-8 text lines using context managers."""
    with open("store.txt", "wt", encoding="utf-8") as file:
        file.write("Hello\n")
        file.write("World\n")

    lines = []
    with open("store.txt", "rt", encoding="utf-8") as file2:
        for line in file2:
            cleaned = line.strip()
            print(cleaned)
            lines.append(cleaned)

    assert lines == ["Hello", "World"]


def test_nums() -> None:
    """Write fixed-width binary integers and read via random-access seek."""
    with open("nums.bin", "wb") as file:
        for i in range(1_000_000, 1_000_010):
            file.write(i.to_bytes(4, byteorder="little"))

    with open("nums.bin", "rb") as file2:
        file2.seek(8)  # Skip first two 4-byte integers (2 * 4 = 8 bytes)
        b = file2.read(4)
        i = int.from_bytes(b, byteorder="little")
        print(i)
        print(file2.tell())
        assert i == 1_000_002
        assert file2.tell() == 12


def test_strings() -> None:
    """Store and recover variable-length strings via 2-byte length prefixes."""
    messages = ["UCL", "ENGF0034", "Persistence"]
    with open("strings.bin", "wb") as file:
        for msg in messages:
            raw = msg.encode("utf-8")
            file.write(len(raw).to_bytes(2, byteorder="little"))
            file.write(raw)

    recovered = []
    with open("strings.bin", "rb") as file2:
        while True:
            length_bytes = file2.read(2)
            if not length_bytes:
                break
            length = int.from_bytes(length_bytes, byteorder="little")
            raw = file2.read(length)
            assert len(raw) == length
            recovered.append(raw.decode("utf-8"))

    assert recovered == messages


if __name__ == "__main__":
    test_write()
    test_nums()
    test_strings()
    print("All store.py tests passed successfully!")
