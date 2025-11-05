# FastAPI Test Suite

This directory contains comprehensive tests for the Mergington High School API built with FastAPI.

## Test Structure

### Test Files

- **`test_api.py`** - Core API functionality tests
  - Root endpoint redirect
  - Activities endpoint (GET /activities)
  - Signup endpoint (POST /activities/{activity_name}/signup)
  - Unregister endpoint (DELETE /activities/{activity_name}/unregister)
  - Integration scenarios

- **`test_edge_cases.py`** - Edge cases and error scenarios
  - Special characters in inputs
  - Case sensitivity
  - Data integrity checks
  - Response format validation

- **`test_performance.py`** - Performance and load testing
  - Response time tests
  - Concurrent request handling
  - Stress testing scenarios
  - Load testing with multiple operations

- **`test_with_utilities.py`** - Examples using test utilities
  - Demonstrates helper functions
  - Shows test utility patterns

- **`test_utils.py`** - Test utilities and helper functions
  - ActivityTestHelper class
  - Test data generators
  - Validation helpers

### Configuration Files

- **`conftest.py`** - Pytest configuration and fixtures
  - Test client setup
  - Data reset fixtures
  - Shared test configuration

## Running Tests

### Run All Tests
```bash
pytest tests/ -v
```

### Run Specific Test Files
```bash
# Core API tests only
pytest tests/test_api.py -v

# Edge case tests only
pytest tests/test_edge_cases.py -v

# Performance tests only
pytest tests/test_performance.py -v
```

### Run Tests by Category
```bash
# Run only fast tests (exclude slow performance tests)
pytest tests/ -m "not slow" -v

# Run only slow tests
pytest tests/ -m "slow" -v
```

### Run Specific Test Classes
```bash
# Test only signup functionality
pytest tests/test_api.py::TestSignupEndpoint -v

# Test only performance scenarios
pytest tests/test_performance.py::TestPerformance -v
```

### Run Specific Test Methods
```bash
# Test specific signup scenario
pytest tests/test_api.py::TestSignupEndpoint::test_signup_for_existing_activity_success -v
```

## Test Coverage

The test suite covers:

✅ **Functionality Testing**
- All API endpoints (GET, POST, DELETE)
- Success and error scenarios
- Data validation and integrity

✅ **Edge Cases**
- Invalid inputs and parameters
- Special characters and encoding
- Case sensitivity
- Boundary conditions

✅ **Integration Testing**
- End-to-end workflows
- Multiple operation sequences
- Data persistence across requests

✅ **Performance Testing**
- Response time validation
- Concurrent request handling
- Load testing scenarios
- Stress testing

## Test Data Management

- Each test uses the `reset_activities` fixture to ensure clean state
- Original activity data is restored after each test
- No test interferes with others

## Test Utilities

The `test_utils.py` module provides:

- **ActivityTestHelper**: Helper class for common operations
- **generate_test_email()**: Generate unique test emails
- **assert_valid_activity_structure()**: Validate activity data structure
- **get_activity_names()**: Get list of all activities

Example usage:
```python
def test_with_helper(client, reset_activities):
    helper = ActivityTestHelper(client)
    email = generate_test_email()
    
    # Use helper methods
    response = helper.signup_student("Chess Club", email)
    assert helper.is_student_registered("Chess Club", email)
```

## Dependencies

The tests require these packages (already added to requirements.txt):
- `pytest` - Testing framework
- `httpx` - HTTP client for FastAPI testing
- `fastapi[all]` - FastAPI with test client support

## Test Configuration

Pytest configuration in `pytest.ini`:
- Custom markers for test categorization
- Python path configuration
- Test discovery settings