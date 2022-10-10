from typing import Optional


def get_entry_type(int) -> str:
    """Returns the type of the fat entry

    Based on Carrier's Table 10.6.

    Anything that is not lfn, dir, or vol is returned as
    a hex string (e.g., 0x20) beacuse it's unimportant
    to this assignment.

    returns:
        str: type of the FAT entry
    """
    # We must check for lfn first.
    types = {0x0F: "lfn", 0x10: "dir", 0x08: "vol"}
    for flag in types:
        if int & flag == flag:
            return types[flag]
    return hex(int)


def _parse_lfn(data: bytes) -> str:
    """Parse a long file name (lfn) entry

    Based on Carrier's Table 10.7.

    returns:
        str: log file name entry convered to string
    """
    assert len(data) == 32, f"data arg is {len(data)} bytes; expected 32 bytes."

    # strip off 0xff padding, concatenate, and then try to decode
    lfn_bytes = (
        data[1:11].strip(b"\xff")
        + data[14:26].strip(b"\xff")
        + data[28:32].strip(b"\xff")
    )
    try:
        # unicode 16 little endian
        lfn_str = lfn_bytes.decode("utf-16-le")
    except UnicodeDecodeError:
        # Not an LFN entry or you have the wrong bytes
        print("Invalid unicode.")
        raise

    # remove null bit, if it exists
    if lfn_str[-1] == "\x00":
        lfn_str = lfn_str[:-1]
    return lfn_str


def parse_name(entry: bytes) -> Optional[str]:
    """Decode the name of a directory entry

    Returns the name of an entry, accounting for LFN entries
    and unicode. If the entry type is 0x0, it is unallocated
    and we return None. If a non-LFN name starts with 0xE5, then it is
    a deleted file and we return "_" as the first character of the name
    since 0xE5 is not printable ascii.

    returns:
        str: name of the entry (or None if unallocated)
    """
    entry_type = get_entry_type(entry[11])

    if entry_type == "lfn":
        # long file name
        name = _parse_lfn(entry)
    else:
        # everything else
        name = entry[0:11].strip()
        if entry[0] == 0xE5:
            name = b"_" + name[1:]
    if entry_type in ["vol", "dir", "lfn"]:
        result = name
    elif entry_type == "0x0":
        result = None
    else:
        result = name[0:8].strip() + b"." + name[8:11].strip()
    _name = result.decode("utf-8") if type(result) == bytes else result

    return _name
