import logging
from collections.abc import Sequence

from unicorn.unicorn import Uc

from unplayplay.consts import RT_HOOKS
from unplayplay.emu.addressing import rebase
from unplayplay.emu.heap_allocator import HeapAllocator
from unplayplay.emu.hooks.hook_amd64 import hook_amd64

logger = logging.getLogger(__name__)


def hook_malloc(mu: Uc, image_base: int, heap: HeapAllocator):
    addr = rebase(image_base, RT_HOOKS.MALLOC_VA)

    def _cb(_mu: Uc, args: Sequence[int]) -> int:
        size = args[0]

        chunk = heap.alloc(size)

        logger.debug("size=0x%X -> 0x%X (chunk size=0x%X)", size, chunk.ptr, chunk.size)

        return chunk.ptr

    hook_amd64(mu, addr, _cb)

    logger.debug("j__malloc_base -> 0x%X", addr)
