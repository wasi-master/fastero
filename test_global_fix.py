#!/usr/bin/env python3
"""Test script to verify the global variable fix in fastero."""

from fastero.utils import _Timer
import time

def test_normal_code():
    """Test that normal code without globals still works."""
    print("Testing normal code...")
    stmt = '''
x = 42
y = x * 2
result = y + 10
'''
    timer = _Timer(stmt=stmt, setup='pass')
    result = timer.timeit(number=1000)
    print(f"✓ Normal code works: {result:.6f}s")
    return True

def test_global_conflict():
    """Test code with global variable conflicts."""
    print("Testing global variable conflicts...")
    stmt = '''R = 8.314

def calling_global():
    global R
    R * 10

calling_global()'''
    
    timer = _Timer(stmt=stmt, setup='pass')
    result = timer.timeit(number=1000)
    print(f"✓ Global conflict resolved: {result:.6f}s")
    return True

def test_no_conflict_globals():
    """Test globals that don't conflict with assignments."""
    print("Testing non-conflicting globals...")
    # This should use standard timeit since there's no conflict
    stmt = '''
x = 10  # This doesn't conflict with the global in the function

def use_global():
    global SOME_VAR  # This global doesn't exist in assignments
    return x * 2  # Use the local x instead

result = use_global()
'''
    
    timer = _Timer(stmt=stmt, setup='pass')
    result = timer.timeit(number=1000)
    print(f"✓ Non-conflicting globals work: {result:.6f}s")
    return True

def test_complex_case():
    """Test a more complex case with multiple variables."""
    print("Testing complex case with multiple variables...")
    stmt = '''
A = 1.0
B = 2.0

def calculate():
    global A, B
    return A * B + 5

result = calculate()
'''
    
    timer = _Timer(stmt=stmt, setup='pass')
    result = timer.timeit(number=1000)
    print(f"✓ Complex case works: {result:.6f}s")
    return True

def test_regression_simple():
    """Test that simple cases without any globals still work."""
    print("Testing regression - simple case...")
    stmt = 'x = 1; y = x + 2'
    timer = _Timer(stmt=stmt, setup='pass')
    result = timer.timeit(number=1000)
    print(f"✓ Simple case works: {result:.6f}s")
    return True

if __name__ == "__main__":
    print("Running global variable fix tests...\n")
    
    tests = [
        test_normal_code,
        test_global_conflict,  # This is the main fix
        test_no_conflict_globals,
        test_complex_case,
        test_regression_simple,
    ]
    
    passed = 0
    for test in tests:
        try:
            if test():
                passed += 1
            print()
        except Exception as e:
            print(f"✗ Test failed: {e}")
            import traceback
            traceback.print_exc()
            print()
    
    print(f"Results: {passed}/{len(tests)} tests passed")
    if passed == len(tests):
        print("🎉 All tests passed!")
        exit(0)
    else:
        print("❌ Some tests failed!")
        exit(1)