#!/usr/bin/env python3
"""Offline evidence-display regression checks, not external-source verification.

The previous 32-candidate regression is superseded by the expanded tests for 33
candidates, field-level room evidence, blank unsupported hotel/route numbers,
menu arithmetic, prior-session provenance and all 15 generated pages.
"""
from pathlib import Path
import subprocess
import sys

if __name__=='__main__':
    root=Path(__file__).resolve().parent.parent
    result=subprocess.run([sys.executable,'-m','unittest','discover','-s','tests','-v'],cwd=root)
    if result.returncode==0:
        print('PASS: evidence-display regression. LIMIT: offline checks do not verify external availability or future prices.')
    raise SystemExit(result.returncode)
