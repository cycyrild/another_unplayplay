class EmulationError(RuntimeError):
    """Raised when Unicorn emulator fails during execution."""


class KeyExtractionError(RuntimeError):
    """Raised when AES key extraction fails."""
