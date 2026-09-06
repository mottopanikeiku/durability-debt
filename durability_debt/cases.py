"""Authored synthetic cases; none is evidence of a real application bug."""
from .model import Claim, Instruction as I, Program


def cases() -> tuple[Program, ...]:
    initial = (("source", 0), ("manifest", 0))
    unsafe = (I("write", "source", 1), I("signal", "ready"), I("flush", "source"))
    safe = (I("write", "source", 1), I("flush", "source"), I("signal", "ready"))
    consumer = (I("wait", "ready"), I("read", "source", "seen"),
                I("copy", "manifest", "seen"), I("flush", "manifest"))
    claim = (Claim("source", "manifest"),)
    return (
        Program("publish_before_flush", initial, (unsafe, consumer), claim),
        Program("flush_before_publish", initial, (safe, consumer), claim),
        # A dirty read does not make a later independent log a semantic bug.
        Program("independent_logger", (("source", 0), ("log", 0)),
                (unsafe, (I("wait", "ready"), I("read", "source", "unused"),
                          I("write", "log", 1), I("flush", "log"))), ()),
        # This is a declared finite recovery policy, not real cache code.
        Program("self_validating_cache", initial, (unsafe, consumer),
                (Claim("source", "manifest", discard_invalid=True),)),
        # Ordinary single-process missing-flush loss must not be credited as
        # a new concurrency capability; the seed baseline already detects it.
        Program("single_process_missing_flush", initial,
                ((I("write", "source", 1), I("write", "manifest", 1), I("flush", "manifest")),), claim),
        # Noise probes projection and the elementary extrema null only. An
        # improvement on this authored case is not a research efficiency win.
        Program("independent_noise", initial + (("noise", 0),),
                ((I("write", "noise", 1), I("write", "source", 1), I("signal", "ready"),
                  I("write", "noise", 2), I("flush", "source")), consumer), claim),
    )
