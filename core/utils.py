from typing import List, Optional
import socket
import re
from pathlib import Path

def is_valid_domain(domain: str) -> bool:
    """Validate domain format with improved regex"""
    pattern = r'^(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z]{2,}$'
    return re.match(pattern, domain, re.IGNORECASE) is not None

def resolve_ip(domain: str, timeout: float = 3.0) -> List[str]:
    """Resolve domain to IP addresses with timeout"""
    try:
        socket.setdefaulttimeout(timeout)
        return list({addr[4][0] for addr in socket.getaddrinfo(domain, 80)})
    except (socket.gaierror, socket.timeout):
        return []
    except Exception as e:
        print(f"[!] IP resolution error for {domain}: {e}")
        return []

def ensure_directory(path: str) -> Path:
    """Ensure directory exists and return Path object"""
    path_obj = Path(path).absolute()
    try:
        path_obj.mkdir(parents=True, exist_ok=True)
        return path_obj
    except Exception as e:
        print(f"[!] Directory creation failed: {e}")
        raise
