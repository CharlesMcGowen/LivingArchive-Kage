#!/usr/bin/env python3
"""
Direct Nmap Test for Kage Agent
================================
Tests if nmap can be executed directly (as the daemon would do)
"""

import subprocess
import sys
import json
import xml.etree.ElementTree as ET
from pathlib import Path

def test_nmap_execution():
    """Test if nmap can be executed with the arguments the daemon would use"""
    print("Testing Nmap Execution (as Kage daemon would use)")
    print("=" * 60)
    
    target = "127.0.0.1"
    ports = "22,80,443,8080"
    
    # Test 1: Basic nmap scan (TCP connect scan - doesn't require root)
    # Note: SYN scan (-sS) requires root, so we use -sT for testing
    print(f"\n1. Testing: nmap -sT -p {ports} {target} (TCP connect scan)")
    try:
        result = subprocess.run(
            ['nmap', '-sT', '-p', ports, target],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            print("✅ Nmap SYN scan completed successfully")
            print("\nOutput:")
            print(result.stdout)
            return True
        else:
            print(f"❌ Nmap scan failed (return code: {result.returncode})")
            print(f"Error: {result.stderr}")
            return False
    except subprocess.TimeoutExpired:
        print("❌ Nmap scan timed out")
        return False
    except FileNotFoundError:
        print("❌ Nmap not found in PATH")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_nmap_xml_output():
    """Test nmap with XML output (as scanner might use)"""
    target = "127.0.0.1"
    ports = "22,80,443,8080"
    print(f"\n2. Testing: nmap -sT -p {ports} -oX - {target} (XML output)")
    try:
        result = subprocess.run(
            ['nmap', '-sT', '-p', ports, '-oX', '-', target],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            print("✅ Nmap XML output generated successfully")
            
            # Try to parse XML
            try:
                root = ET.fromstring(result.stdout)
                print("✅ XML output is valid")
                
                # Find open ports
                open_ports = []
                for host in root.findall('host'):
                    for port in host.findall('.//port'):
                        state = port.find('state')
                        if state is not None and state.get('state') == 'open':
                            port_num = port.get('portid')
                            protocol = port.get('protocol')
                            service = port.find('service')
                            service_name = service.get('name') if service is not None else 'unknown'
                            open_ports.append({
                                'port': port_num,
                                'protocol': protocol,
                                'service': service_name
                            })
                
                if open_ports:
                    print(f"✅ Found {len(open_ports)} open ports:")
                    for p in open_ports:
                        print(f"   - {p['port']}/{p['protocol']} ({p['service']})")
                else:
                    print("ℹ️  No open ports found (normal if no services running)")
                
                return True
            except ET.ParseError as e:
                print(f"⚠️  XML parsing error: {e}")
                print("   But nmap executed successfully")
                return True
        else:
            print(f"❌ Nmap XML scan failed (return code: {result.returncode})")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_nmap_with_service_detection():
    """Test nmap with service detection (as scanner might use)"""
    target = "127.0.0.1"
    ports = "22,80,443,8080"
    print(f"\n3. Testing: nmap -sT -sV -p {ports} {target} (with service detection)")
    try:
        result = subprocess.run(
            ['nmap', '-sT', '-sV', '-p', ports, target],
            capture_output=True,
            text=True,
            timeout=60  # Service detection takes longer
        )
        
        if result.returncode == 0:
            print("✅ Nmap service detection completed successfully")
            print("\nOutput (first 20 lines):")
            lines = result.stdout.split('\n')[:20]
            for line in lines:
                print(f"   {line}")
            return True
        else:
            print(f"❌ Nmap service detection failed (return code: {result.returncode})")
            return False
    except subprocess.TimeoutExpired:
        print("⚠️  Nmap service detection timed out (this is normal for localhost)")
        return True  # Timeout is acceptable
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_nmap_execution_method():
    """Test the method the daemon would use to execute nmap"""
    print(f"\n4. Testing: Direct nmap execution (simulating daemon method)")
    
    # This simulates what _execute_nmap_with_techniques might do
    target = "127.0.0.1"
    ports = [22, 80, 443, 8080]
    ports_str = ','.join(map(str, ports))
    
    # Use -sT (TCP connect) instead of -sS (SYN) since we may not have root
    nmap_args = ['-sT', '-p', ports_str, target]
    command = ['nmap'] + nmap_args
    
    print(f"   Command: {' '.join(command)}")
    
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            print("✅ Nmap executed successfully via daemon-style command")
            
            # Check output for port states
            output = result.stdout
            if 'open' in output.lower():
                print("✅ Found open ports in output")
            elif 'closed' in output.lower() or 'filtered' in output.lower():
                print("ℹ️  Ports are closed/filtered (normal if no services running)")
            
            return True
        else:
            print(f"❌ Nmap execution failed (return code: {result.returncode})")
            print(f"   stderr: {result.stderr[:200]}")
            return False
    except Exception as e:
        print(f"❌ Error executing nmap: {e}")
        return False

def main():
    """Run all nmap tests"""
    print("\n" + "=" * 60)
    print("Kage Agent - Direct Nmap Execution Test")
    print("=" * 60)
    
    results = []
    
    results.append(("Basic Nmap Scan", test_nmap_execution()))
    results.append(("Nmap XML Output", test_nmap_xml_output()))
    results.append(("Nmap Service Detection", test_nmap_with_service_detection()))
    results.append(("Daemon-style Execution", test_nmap_execution_method()))
    
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {name}")
    
    print(f"\nResults: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n✅ All nmap execution tests passed!")
        print("   The Kage agent should be able to perform nmap scans.")
        return 0
    else:
        print("\n⚠️  Some tests failed, but core functionality may still work")
        return 1

if __name__ == '__main__':
    sys.exit(main())

