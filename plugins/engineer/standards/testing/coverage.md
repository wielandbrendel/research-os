# Test Coverage Standards

## Overview
Standards for test coverage in ML research projects.

## Coverage Requirements
- Core algorithms: 90%+ coverage
- Data processing pipelines: 85%+ coverage
- Utility functions: 80%+ coverage
- Experimental code: 70%+ coverage

## Testing Priorities
1. Data validation and preprocessing
2. Core model logic
3. Metrics and evaluation
4. I/O operations
5. Edge cases and error handling

## ML-Specific Testing
- Test with synthetic data
- Test dimension handling
- Test batch processing
- Test device placement (CPU/GPU)
- Test reproducibility with seeds

## Coverage Tools
- Use pytest-cov for Python projects
- Generate HTML reports for detailed analysis
- Track coverage trends over time
- Exclude experimental/prototype code from metrics

## Best Practices
- Write tests before or alongside implementation
- Test both expected behavior and edge cases
- Use parameterized tests for multiple scenarios
- Mock external dependencies appropriately
- Ensure tests are deterministic and reproducible