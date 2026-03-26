import time
from pathlib import Path

from unplayplay import KeyEmu

# obfuscated_key linked to "02b785ef12f5046c21411a778a932c0d"

TEST_VECTORS = [
    (
        # spotify:track:69kOkLUCkxIZYexIgSG8rq (ogg-vorbis-160)
        "2f43127d80edc9cd9f12f441e1cb7904b680f9da",  # file_id
        "b5feb4e01f9c1b668abcaebc721774fc",  # obfuscated_key
        "a503a84c1dc9271460cc13f142e0bae2",  # aes_key
    ),
    (
        "1a8e5b04837957617162724232b0c96922222447",  # file_id
        "1198d1e82d685fbdb6ed583a691e0781",  # obfuscated_key
        "c3206271b4c70fff8e4ac3993c4dae8a",  # aes_key
    ),
    (
        "cf1bd197a6f5d613fc856bd689e43c0f4069b800",
        "d97f61d454cafdb132b97dd196900c21",
        "8d86fb522c00729f35b34d60b165b922",
    ),
    (
        "71df45edb4748a8b1bd4126ded06063674745182",
        "09bac7c2add68fd0897aa147b3801564",
        "0fd3998b706247b3474b2d3cf6d8e31f",
    ),
    (
        "894813d0a3113c97ab601b0f65afb9543d96ec32",
        "d021cc4efb3cc23be8b1d68f09420e21",
        "4d442c155f9a95258f613a89be957be9",
    ),
]


def test_keyemu():
    key_emu = KeyEmu(Path("Spotify.dll"))

    for file_id, obfuscated_key, expected_key in TEST_VECTORS:
        print(f"Testing file_id={file_id}")
        start = time.perf_counter()
        decrypted = key_emu.get_aes_key(bytes.fromhex(obfuscated_key)).hex()
        elapsed = time.perf_counter() - start

        # fmt: off
        assert decrypted == expected_key,   f"Mismatch\n" \
                                            f"file_id={file_id}\n" \
                                            f"expected={expected_key}\n" \
                                            f"got={decrypted}"
        # fmt: on
        print(f"{file_id[:8]}... OK ({elapsed * 1000:.2f} ms)")


if __name__ == "__main__":
    test_keyemu()
