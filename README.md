# ReconPy
Advanced Reconnaissance Toolkit for Bug Bounty &amp; Pentesting


![Python](https://img.shields.io/badge/python-3.8+-blue.svg)

ReconPy is an automated reconnaissance tool designed for bug bounty hunters and penetration testers.

## Features

- Subdomain enumeration (DNS brute-forcing, CT logs)
- Directory/file bruteforcing with dynamic wordlist generation
- Wayback Machine historical URL scraping
- Vulnerability scanning (XSS, subdomain takeover)
- Machine learning-enhanced wordlist generation

## Installation

```bash
git clone https://github.com/MeshAllam/ReconPy.git
cd ReconPy
pip install -r requirements.txt
```

## Usage
```bash
# 1. Subdomain Enumeration
python reconpy.py enum example.com -o subs.json

# 2. Directory Bruteforcing  
python reconpy.py dir http://example.com -w wordlists/common.txt -e php,html

# 3. Wayback Machine Scraping
python reconpy.py wayback example.com -o wayback.json

# 4. Vulnerability Scanning
# XSS Test
python reconpy.py vuln xss "http://example.com/search?q=test" -o xss_results.json

# Subdomain Takeover Check  
python reconpy.py vuln takeover dev.example.com

# 5. Full Recon Workflow
python reconpy.py full example.com --output-dir recon_results/
```
