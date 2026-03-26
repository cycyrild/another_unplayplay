from dataclasses import dataclass

from unicorn.unicorn import Uc

from unplayplay.emu.heap_chunk import HeapChunk


@dataclass(slots=True)
class EmuSession:
    mu: Uc

    vm_obj: HeapChunk
    obfuscated_key: HeapChunk
    init_value: HeapChunk
    derived_key: HeapChunk

    captured_aes_key: bytearray | None
