import logging

from unicorn.unicorn import Uc
from unicorn.unicorn_const import UC_HOOK_CODE
from unicorn.x86_const import (
    UC_X86_REG_RAX,
    UC_X86_REG_RIP,
    UC_X86_REG_RSP,
)

from unplayplay.consts import RT_HOOKS
from unplayplay.emu.addressing import rebase

logger = logging.getLogger(__name__)


def apply_stubs(mu: Uc, image_base: int):

    def hook_ret0(mu: Uc, address, size, user_data):
        mu.reg_write(UC_X86_REG_RAX, 0)

        rsp = mu.reg_read(UC_X86_REG_RSP)
        ret_addr = int.from_bytes(mu.mem_read(rsp, 8), "little")

        mu.reg_write(UC_X86_REG_RSP, rsp + 8)
        mu.reg_write(UC_X86_REG_RIP, ret_addr)

    targets = [
        RT_HOOKS.MTX_LOCK_VA,
        RT_HOOKS.CND_WAIT_VA,
        RT_HOOKS.MTX_UNLOCK_VA,
    ]

    for ida_va in targets:
        addr = rebase(image_base, ida_va)
        mu.hook_add(UC_HOOK_CODE, hook_ret0, begin=addr, end=addr)
        logger.debug("hook -> 0x%X", addr)
