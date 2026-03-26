import logging

from unicorn.unicorn import Uc
from unicorn.x86_const import (
    UC_X86_REG_RCX,
    UC_X86_REG_RDX,
    UC_X86_REG_RIP,
    UC_X86_REG_RSP,
)

from unplayplay.seh.dispatcher import dispatch_cpp_exception
from unplayplay.seh.state import SehRuntimeState

logger = logging.getLogger(__name__)


def seh_hook(mu: Uc, address: int, _size: int, state: SehRuntimeState):
    exception_object_ptr = mu.reg_read(UC_X86_REG_RCX)
    throw_info_ptr = mu.reg_read(UC_X86_REG_RDX)

    logger.debug("=== CxxThrowException ===")
    logger.debug("VA: 0x%X", address)
    logger.debug("RVA: 0x%X", address - state.image_base)
    logger.debug("pExceptionObject: 0x%X", exception_object_ptr)
    logger.debug("pThrowInfo: 0x%X", throw_info_ptr)

    try:
        handled = dispatch_cpp_exception(state, mu, exception_object_ptr, throw_info_ptr)
    except Exception as exc:
        logger.error("dispatch error: %s", exc)
        raise

    if handled:
        logger.debug("exception handled")
        logger.debug("new RIP: 0x%X", mu.reg_read(UC_X86_REG_RIP))
        logger.debug("new RSP: 0x%X", mu.reg_read(UC_X86_REG_RSP))
        return

    raise RuntimeError("Unhandled C++ exception in Unicorn dispatcher")
