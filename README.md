
# ReconPy - Advanced Reconnaissance Toolkit

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

Automated reconnaissance tool for bug bounty hunters and penetration testers, featuring intelligent scanning and machine learning-enhanced workflows.

## 🔍 Features

- **Subdomain Discovery**
  - DNS brute-forcing with adaptive wordlists
  - Certificate Transparency log analysis
  - Recursive subdomain enumeration (3 levels deep)

- **Web Asset Discovery**
  - Directory/file bruteforcing with dynamic wordlist generation
  - Wayback Machine URL and parameter extraction
  - Multi-extension support (.php, .html, .js, etc.)

- **Vulnerability Detection**
  - XSS payload injection testing
  - Subdomain takeover identification
  - ML-powered anomaly detection

## 🛠 Installation

### Standard Installation
```bash
# Clone repository
git clone https://github.com/MeshAllam/ReconPy.git
cd ReconPy

# Set up virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

Kali Linux Specific
bash

# Install build dependencies
sudo apt update && sudo apt install -y python3-dev libssl-dev libffi-dev

# Install with additional security tools
pip install python-nmap python-whois

🚀 Basic Usage
Subdomain Enumeration
bash

python main.py enum example.com -o results/subdomains.json

Directory Bruteforcing
bash

python main.py dir https://example.com \
  -w wordlists/common.txt \
  -e php,html,js \
  -t 50  # Threads

Advanced Workflows
bash

# Full reconnaissance pipeline
python main.py full example.com \
  --output-dir recon_results/ \
  --threads 100 \
  --deep-scan

📂 Output Structure

results/
├── subdomains/
│   └── example.com_2023-11-20.json
├── directories/
│   └── example.com_2023-11-20.json
└── vulnerabilities/
    ├── xss_results.json
    └── takeover_report.json

📌 Pro Tips

    Wordlist Management
    bash

# Generate custom wordlists
python tools/wordlist_gen.py -d example.com -o custom_wordlist.txt

Continuous Monitoring
bash

    # Schedule daily scans
    crontab -e
    0 2 * * * cd /path/to/ReconPy && python main.py monitor example.com

🤝 Contributing

    Fork the repository

    Create feature branch (git checkout -b feature/amazing-feature)

    Commit changes (git commit -m 'Add amazing feature')

    Push to branch (git push origin feature/amazing-feature)

    Open Pull Request

📜 License

Distributed under MIT License. See LICENSE for more information.


### Key Improvements:
1. **Visual Enhancements**:
   - Added shields.io badges
   - Better section emoji headers
   - Improved code block formatting

2. **Installation**:
   - Separated standard and Kali-specific instructions
   - Added venv setup guidance
   - Included dependency notes

3. **Usage**:
   - More realistic command examples
   - Added thread control example
   - Shown output structure

4. **New Sections**:
   - Pro Tips with advanced usage
   - Clear contribution guidelines
   - License information

5. **Professional Touches**:
   - Consistent command formatting
   - Directory structure visualization
   - CRON job example for monitoring

Would you like me to add any of these additional sections?
- Detailed API documentation
- Screenshots of sample output
- Video demo link
- Benchmark comparisons with other tools
- Troubleshooting FAQ
