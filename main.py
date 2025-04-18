#!/usr/bin/env python3
import argparse
import yaml
import json
import datetime
from pathlib import Path
from typing import Optional
from core.enumerator import DomainEnumerator
from core.directory_bruteforcer import DirectoryBruteforcer
from core.wayback_scraper import WaybackScraper
from core.vulnerability_scanner import VulnerabilityScanner
from core.reporter import ReportGenerator

def load_config() -> dict:
    """Load configuration with safe defaults"""
    default_config = {
        'default': {
            'threads': 50,
            'rate_limit': 100,
            'recursive_depth': 3
        },
        'dns': {
            'default_servers': ['1.1.1.1', '8.8.8.8'],
            'timeout': 2
        },
        'wayback': {
            'timeout': 30,
            'max_urls': 10000,
            'request_delay': 1
        },
        'vulnerability': {
            'xss_payload_file': 'wordlists/xss_payloads.txt'
        }
    }
    
    try:
        config_path = Path(__file__).parent / "config.yaml"
        with open(config_path) as f:
            user_config = yaml.safe_load(f) or {}
        # Deep merge with defaults
        for key in default_config:
            if key in user_config:
                default_config[key].update(user_config[key])
        return default_config
    except Exception as e:
        print(f"⚠️ Config loading error: {e}. Using defaults")
        return default_config

def validate_path(path_str: str) -> Path:
    """Convert string to absolute Path and ensure parent exists"""
    path = Path(path_str).absolute()
    path.parent.mkdir(parents=True, exist_ok=True)
    return path

def setup_parsers() -> argparse.ArgumentParser:
    config = load_config()
    parser = argparse.ArgumentParser(
        description="ReconPy - Ultimate Reconnaissance Toolkit",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    subparsers = parser.add_subparsers(dest='command', required=True)

    # Enum parser
    enum_parser = subparsers.add_parser('enum', help='Subdomain enumeration')
    enum_parser.add_argument('domain', help='Target domain')
    enum_parser.add_argument('--dns-servers', nargs='+', 
                          default=config['dns']['default_servers'],
                          help='DNS servers to use')
    enum_parser.add_argument('--recursive-depth', type=int, 
                          default=config['default']['recursive_depth'],
                          help='Recursion depth for subdomain discovery')
    enum_parser.add_argument('-o', '--output', type=validate_path,
                          help='Output file path')
    enum_parser.add_argument('-t', '--threads', type=int,
                          default=config['default']['threads'],
                          help='Number of threads to use')

    # Dir parser
    dir_parser = subparsers.add_parser('dir', help='Directory brute-forcing')
    dir_parser.add_argument('url', help='Base URL to scan')
    dir_parser.add_argument('-w', '--wordlist', required=True, type=Path,
                         help='Path to wordlist file')
    dir_parser.add_argument('-e', '--extensions', nargs='+',
                         default=[''], help='File extensions to try')
    dir_parser.add_argument('-t', '--threads', type=int, default=20,
                         help='Number of threads to use')
    dir_parser.add_argument('-o', '--output', type=validate_path,
                         help='Output file path')

    # Wayback parser
    wayback_parser = subparsers.add_parser('wayback', help='Wayback Machine scraping')
    wayback_parser.add_argument('domain', help='Domain to scrape')
    wayback_parser.add_argument('-o', '--output', type=validate_path,
                             help='Output file path')
    wayback_parser.add_argument('--max-urls', type=int,
                             default=config['wayback']['max_urls'],
                             help='Maximum URLs to fetch')

    # Vulnerability parser
    vuln_parser = subparsers.add_parser('vuln', help='Vulnerability scanning')
    vuln_subparsers = vuln_parser.add_subparsers(dest='vuln_command', required=True)

    # XSS testing
    xss_parser = vuln_subparsers.add_parser('xss', help='Test for XSS vulnerabilities')
    xss_parser.add_argument('url', help='URL to test (with parameters)')
    xss_parser.add_argument('-o', '--output', type=validate_path,
                          help='Output file path')

    # Subdomain takeover
    takeover_parser = vuln_subparsers.add_parser('takeover', 
                                              help='Check for subdomain takeovers')
    takeover_parser.add_argument('subdomain', help='Subdomain to check')
    takeover_parser.add_argument('-o', '--output', type=validate_path,
                              help='Output file path')

    return parser

def handle_enum(args, config: dict) -> None:
    """Handle subdomain enumeration command"""
    enumerator = DomainEnumerator(
        dns_servers=args.dns_servers,
        recursive_depth=args.recursive_depth,
        max_threads=args.threads
    )
    subdomains = enumerator.enumerate(args.domain)
    if args.output:
        ReportGenerator.save_report(subdomains, args.domain, args.output, 'json')

def handle_dir(args, config: dict) -> None:
    """Handle directory bruteforce command"""
    bruteforcer = DirectoryBruteforcer()
    try:
        with open(args.wordlist, 'r') as f:
            wordlist = [line.strip() for line in f if line.strip()]
        results = bruteforcer.bruteforce(args.url, wordlist, args.extensions, args.threads)
        if args.output:
            ReportGenerator.save_report(results, args.url, args.output, 'json')
    except FileNotFoundError:
        print(f"❌ Wordlist not found: {args.wordlist}")
        exit(1)

def handle_wayback(args, config: dict) -> None:
    """Handle Wayback Machine scraping"""
    scraper = WaybackScraper(config['wayback'])
    urls = scraper.get_all_urls(args.domain)
    params = scraper.extract_parameters(urls)
    if args.output:
        ReportGenerator.save_report(params, args.domain, args.output, 'json')

def handle_vuln(args, config: dict) -> None:
    """Handle vulnerability scanning"""
    try:
        scanner = VulnerabilityScanner(config['vulnerability']['xss_payload_file'])
    except FileNotFoundError:
        print(f"❌ XSS payload file not found: {config['vulnerability']['xss_payload_file']}")
        exit(1)

    if args.vuln_command == 'xss':
        results = scanner.test_xss(args.url)
        if args.output:
            ReportGenerator.save_report(results, args.url, args.output, 'json')
        else:
            print(json.dumps(results, indent=2))
    elif args.vuln_command == 'takeover':
        is_vulnerable = scanner.check_subdomain_takeover(args.subdomain)
        result = {
            'subdomain': args.subdomain,
            'vulnerable': is_vulnerable,
            'timestamp': datetime.datetime.now().isoformat()
        }
        if args.output:
            ReportGenerator.save_report(result, args.subdomain, args.output, 'json')
        else:
            print(json.dumps(result, indent=2))

def main() -> None:
    parser = setup_parsers()
    args = parser.parse_args()
    config = load_config()

    try:
        if args.command == 'enum':
            handle_enum(args, config)
        elif args.command == 'dir':
            handle_dir(args, config)
        elif args.command == 'wayback':
            handle_wayback(args, config)
        elif args.command == 'vuln':
            handle_vuln(args, config)
    except KeyboardInterrupt:
        print("\n🛑 Scan interrupted by user")
        exit(0)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        exit(1)

if __name__ == "__main__":
    main()
