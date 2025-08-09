# Tests Directory

This directory contains test files for the Cyclistic bike-share analysis project.

## Test Structure

- `test_cyclistic_analysis.py` - Main test suite covering all analysis modules

## Running Tests

To run the tests:

```bash
# Run all tests
python -m pytest tests/

# Run with verbose output
python -m pytest tests/ -v

# Run specific test file
python tests/test_cyclistic_analysis.py

# Run with coverage
python -m pytest tests/ --cov=src --cov-report=html
```

## Test Coverage

The tests cover:
- Data loading and preparation
- Analysis functions
- Visualization components
- Data validation
- Integration testing

## Adding New Tests

When adding new functionality, please include corresponding tests:

1. Create test cases for new functions
2. Test both success and failure scenarios
3. Include edge cases
4. Ensure good test coverage