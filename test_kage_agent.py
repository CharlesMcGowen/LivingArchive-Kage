#!/usr/bin/env python3
"""
Test Script for Kage Agent
============================
Tests if the Kage agent can run and perform nmap scans against 127.0.0.1
"""

import sys
import os
import subprocess
import socket
import time
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Color codes for output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

def print_test(name):
    """Print test name"""
    print(f"\n{BLUE}━━━ Testing: {name} ━━━{RESET}")

def print_success(message):
    """Print success message"""
    print(f"{GREEN}✅ {message}{RESET}")

def print_error(message):
    """Print error message"""
    print(f"{RED}❌ {message}{RESET}")

def print_warning(message):
    """Print warning message"""
    print(f"{YELLOW}⚠️  {message}{RESET}")

def print_info(message):
    """Print info message"""
    print(f"{BLUE}ℹ️  {message}{RESET}")

def test_nmap_installed():
    """Test if nmap is installed and accessible"""
    print_test("Nmap Installation")
    try:
        result = subprocess.run(['nmap', '--version'], 
                              capture_output=True, 
                              text=True, 
                              timeout=5)
        if result.returncode == 0:
            version_line = result.stdout.split('\n')[0]
            print_success(f"Nmap is installed: {version_line}")
            return True
        else:
            print_error("Nmap command failed")
            return False
    except FileNotFoundError:
        print_error("Nmap is not installed or not in PATH")
        print_info("Install with: sudo apt-get install nmap (Debian/Ubuntu) or brew install nmap (macOS)")
        return False
    except Exception as e:
        print_error(f"Error checking nmap: {e}")
        return False

def test_nmap_scan_localhost():
    """Test if nmap can scan 127.0.0.1"""
    print_test("Nmap Scan Against 127.0.0.1")
    try:
        # Run a quick scan of common ports on localhost
        print_info("Running: nmap -p 22,80,443,8080 127.0.0.1")
        result = subprocess.run(
            ['nmap', '-p', '22,80,443,8080', '127.0.0.1'],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            print_success("Nmap scan completed successfully")
            print_info("Scan output:")
            # Print relevant lines from output
            for line in result.stdout.split('\n'):
                if 'PORT' in line or 'STATE' in line or 'open' in line.lower() or 'closed' in line.lower():
                    print(f"   {line}")
            
            # Check if any ports were found
            if 'open' in result.stdout.lower():
                print_success("Found open ports on 127.0.0.1")
            else:
                print_warning("No open ports found (this is normal if no services are running)")
            
            return True
        else:
            print_error(f"Nmap scan failed with return code {result.returncode}")
            print_error(f"Error: {result.stderr}")
            return False
    except subprocess.TimeoutExpired:
        print_error("Nmap scan timed out")
        return False
    except Exception as e:
        print_error(f"Error running nmap scan: {e}")
        return False

def test_socket_scan_localhost():
    """Test basic socket connectivity to 127.0.0.1"""
    print_test("Socket-based Port Scan (127.0.0.1)")
    test_ports = [22, 80, 443, 8080]
    open_ports = []
    
    for port in test_ports:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2.0)
            result = sock.connect_ex(('127.0.0.1', port))
            sock.close()
            
            if result == 0:
                open_ports.append(port)
                print_success(f"Port {port} is open")
            else:
                print_info(f"Port {port} is closed/filtered")
        except Exception as e:
            print_warning(f"Error checking port {port}: {e}")
    
    if open_ports:
        print_success(f"Found {len(open_ports)} open ports: {open_ports}")
    else:
        print_warning("No open ports found (this is normal if no services are running)")
    
    return True

def test_kage_scanner_import():
    """Test if Kage scanner can be imported"""
    print_test("Kage Scanner Import")
    try:
        # Try to import the scanner
        from kage.nmap_scanner import get_kage_scanner, KageNmapScanner
        print_success("Kage scanner module imported successfully")
        return True
    except ImportError as e:
        print_error(f"Failed to import Kage scanner: {e}")
        print_info("This may be due to missing dependencies or Django setup")
        return False
    except Exception as e:
        print_error(f"Unexpected error importing scanner: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_kage_scanner_init():
    """Test if Kage scanner can be initialized"""
    print_test("Kage Scanner Initialization")
    try:
        from kage.nmap_scanner import get_kage_scanner
        
        # Try to get scanner instance (may fail due to Django dependencies)
        try:
            scanner = get_kage_scanner(parallel_enabled=False)
            print_success("Kage scanner initialized successfully")
            return True, scanner
        except Exception as e:
            # Check if it's a Django-related error
            error_str = str(e).lower()
            if 'django' in error_str or 'settings' in error_str:
                print_warning(f"Scanner initialization requires Django setup: {e}")
                print_info("This is expected in standalone mode - scanner needs Django for full functionality")
                return False, None
            else:
                print_error(f"Scanner initialization failed: {e}")
                import traceback
                traceback.print_exc()
                return False, None
    except Exception as e:
        print_error(f"Error during scanner initialization test: {e}")
        return False, None

def test_kage_scanner_scan():
    """Test if Kage scanner can perform a scan (if initialized)"""
    print_test("Kage Scanner Direct Scan Test")
    
    # First check if scanner can be initialized
    init_success, scanner = test_kage_scanner_init()
    
    if not init_success or scanner is None:
        print_warning("Skipping scan test - scanner not initialized")
        return False
    
    try:
        # Try to perform a direct scan using the scanner's internal methods
        # We'll use the _scan_single_port method if available
        if hasattr(scanner, '_scan_single_port'):
            print_info("Testing _scan_single_port method on 127.0.0.1:80")
            result = scanner._scan_single_port('127.0.0.1', 80, '127.0.0.1')
            
            if result:
                print_success(f"Port scan completed: {result.get('status', 'unknown')}")
                print_info(f"   Port: {result.get('port')}")
                print_info(f"   Status: {result.get('status')}")
                return True
            else:
                print_warning("Port scan returned no result")
                return False
        else:
            print_warning("Scanner doesn't have _scan_single_port method")
            return False
    except Exception as e:
        print_error(f"Error during scan test: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_flask_app_running():
    """Test if Flask app is running"""
    print_test("Flask App Status")
    try:
        import requests
        response = requests.get('http://127.0.0.1:5000/api/kage/status/', timeout=5)
        if response.status_code == 200:
            data = response.json()
            print_success(f"Flask app is running: {data.get('message', 'OK')}")
            return True
        else:
            print_warning(f"Flask app responded with status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print_warning("Flask app is not running (connection refused)")
        print_info("Start Flask app with: python app.py")
        return False
    except ImportError:
        print_warning("requests library not available")
        return False
    except Exception as e:
        print_error(f"Error checking Flask app: {e}")
        return False

def test_daemon_import():
    """Test if daemon can be imported"""
    print_test("Kage Daemon Import")
    try:
        # Check if daemon file exists
        daemon_file = project_root / 'daemons' / 'kage_daemon.py'
        if not daemon_file.exists():
            print_error(f"Daemon file not found: {daemon_file}")
            return False
        
        print_success("Daemon file exists")
        
        # Try to import (may fail due to dependencies)
        try:
            sys.path.insert(0, str(project_root / 'daemons'))
            # Don't actually import - just check syntax
            with open(daemon_file, 'r') as f:
                compile(f.read(), str(daemon_file), 'exec')
            print_success("Daemon file syntax is valid")
            return True
        except SyntaxError as e:
            print_error(f"Daemon file has syntax errors: {e}")
            return False
        except Exception as e:
            print_warning(f"Could not fully validate daemon (may need dependencies): {e}")
            return True  # Syntax is OK, dependencies may be missing
        
    except Exception as e:
        print_error(f"Error checking daemon: {e}")
        return False

def main():
    """Run all tests"""
    print(f"\n{BLUE}{'='*60}")
    print("Kage Agent Test Suite")
    print("="*60 + RESET)
    
    results = {}
    
    # Test 1: Nmap installation
    results['nmap_installed'] = test_nmap_installed()
    
    # Test 2: Nmap scan against localhost
    if results['nmap_installed']:
        results['nmap_scan'] = test_nmap_scan_localhost()
    else:
        results['nmap_scan'] = False
        print_warning("Skipping nmap scan test - nmap not installed")
    
    # Test 3: Socket-based scan
    results['socket_scan'] = test_socket_scan_localhost()
    
    # Test 4: Scanner import
    results['scanner_import'] = test_kage_scanner_import()
    
    # Test 5: Scanner initialization
    results['scanner_init'] = test_kage_scanner_init()[0]
    
    # Test 6: Scanner scan (if initialized)
    if results['scanner_init']:
        results['scanner_scan'] = test_kage_scanner_scan()
    else:
        results['scanner_scan'] = False
        print_warning("Skipping scanner scan test - scanner not initialized")
    
    # Test 7: Flask app
    results['flask_app'] = test_flask_app_running()
    
    # Test 8: Daemon import
    results['daemon_import'] = test_daemon_import()
    
    # Summary
    print(f"\n{BLUE}{'='*60}")
    print("Test Summary")
    print("="*60 + RESET)
    
    total = len(results)
    passed = sum(1 for v in results.values() if v)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {test_name}")
    
    print(f"\n{BLUE}Results: {passed}/{total} tests passed{RESET}")
    
    if passed == total:
        print_success("All tests passed! 🎉")
        return 0
    elif passed >= total * 0.7:
        print_warning("Most tests passed, but some issues detected")
        return 1
    else:
        print_error("Multiple test failures detected")
        return 2

if __name__ == '__main__':
    sys.exit(main())

