# Contributing to EPICcrypto

Thank you for your interest in contributing to EPICcrypto! This document provides guidelines and instructions for contributing.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Making Changes](#making-changes)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Pull Request Process](#pull-request-process)
- [Issue Guidelines](#issue-guidelines)

## Code of Conduct

### Our Pledge

We are committed to providing a welcoming and inclusive environment for all contributors.

### Expected Behavior

- Be respectful and considerate
- Welcome newcomers and help them get started
- Focus on constructive criticism
- Respect differing viewpoints

### Unacceptable Behavior

- Harassment or discrimination
- Trolling or inflammatory comments
- Publishing others' private information
- Any other unethical or unprofessional conduct

## Getting Started

### Prerequisites

- Python 3.11 or higher
- Git
- Basic knowledge of Flask and machine learning
- Understanding of REST APIs

### First-Time Contributors

Look for issues labeled:
- `good first issue` - Good for newcomers
- `help wanted` - We need help with these
- `documentation` - Documentation improvements

## Development Setup

### 1. Fork and Clone

```bash
# Fork the repository on GitHub
# Then clone your fork
git clone https://github.com/YOUR_USERNAME/EPICcrypto.git
cd EPICcrypto
```

### 2. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

```bash
cp .env.example .env
# Edit .env with your settings
```

### 5. Run the Application

```bash
python app.py
```

Visit `http://localhost:5000` to verify it's working.

## Making Changes

### 1. Create a Branch

Always create a new branch for your changes:

```bash
git checkout -b feature/your-feature-name
```

Branch naming conventions:
- `feature/` - New features
- `fix/` - Bug fixes
- `docs/` - Documentation changes
- `refactor/` - Code refactoring
- `test/` - Test additions/changes

### 2. Make Your Changes

- Write clean, readable code
- Follow existing code style
- Add comments for complex logic
- Update documentation if needed

### 3. Test Your Changes

```bash
# Run tests
pytest

# Run specific test file
pytest tests/test_api.py

# Run with coverage
pytest --cov=backend tests/
```

### 4. Commit Your Changes

Write clear, descriptive commit messages:

```bash
git add .
git commit -m "feat: add support for new cryptocurrency"
```

Commit message format:
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation
- `style:` - Code style changes
- `refactor:` - Code refactoring
- `test:` - Test changes
- `chore:` - Maintenance tasks

### 5. Push to Your Fork

```bash
git push origin feature/your-feature-name
```

## Coding Standards

### Python Style Guide

Follow PEP 8 with these additions:

#### Imports

```python
# Standard library imports
import os
import sys

# Third-party imports
import numpy as np
import pandas as pd
from flask import Flask, jsonify

# Local imports
from backend.data.crypto_api import CryptoDataFetcher
from backend.models.predictor import CryptoPricePredictor
```

#### Naming Conventions

```python
# Classes: PascalCase
class CryptoPricePredictor:
    pass

# Functions/methods: snake_case
def calculate_technical_indicators():
    pass

# Constants: UPPER_SNAKE_CASE
MAX_RETRIES = 3
API_TIMEOUT = 30

# Variables: snake_case
current_price = 43250.50
```

#### Documentation

```python
def predict_price(data: List[dict], timeframe: str) -> Dict:
    """
    Predict cryptocurrency price for given timeframe.
    
    Args:
        data: Historical price data
        timeframe: Prediction timeframe ('1h', 'daily', etc.)
    
    Returns:
        Dictionary with prediction results
    """
    pass
```

### JavaScript Style Guide

#### Naming Conventions

```javascript
// Classes: PascalCase
class PredictionService {
}

// Functions: camelCase
function loadPrediction() {
}

// Constants: UPPER_SNAKE_CASE
const API_BASE = '/api';

// Variables: camelCase
let currentPrice = 43250.50;
```

#### Modern JavaScript

Use modern ES6+ features:

```javascript
// Arrow functions
const fetchData = async (coinId) => {
  const response = await fetch(`${API_BASE}/price/${coinId}`);
  return response.json();
};

// Destructuring
const { price, change_24h } = data;

// Template literals
const url = `${API_BASE}/predict/${coinId}?timeframe=${timeframe}`;
```

### CSS Style Guide

```css
/* Use kebab-case for class names */
.prediction-card {
  /* Properties in alphabetical order (optional) */
  background: white;
  border-radius: 10px;
  padding: 20px;
}

/* Use meaningful, semantic names */
.action-strong_buy {
  background: #10b981;
}
```

## Testing

### Writing Tests

#### Backend Tests

```python
# tests/test_feature.py
import pytest
from backend.module import function

def test_function_success():
    """Test successful function execution"""
    result = function(valid_input)
    assert result['status'] == 'success'

def test_function_error():
    """Test function error handling"""
    result = function(invalid_input)
    assert 'error' in result
```

#### API Tests

```python
def test_api_endpoint(client):
    """Test API endpoint"""
    response = client.get('/api/endpoint')
    assert response.status_code == 200
    data = response.get_json()
    assert 'expected_key' in data
```

### Running Tests

```bash
# All tests
pytest

# Specific test file
pytest tests/test_api.py

# Specific test function
pytest tests/test_api.py::test_health_check

# With coverage
pytest --cov=backend --cov-report=html

# Verbose output
pytest -v
```

### Test Coverage

Aim for:
- 80%+ overall coverage
- 100% for critical functions
- All new features should have tests

## Pull Request Process

### Before Submitting

Checklist:
- [ ] Code follows style guidelines
- [ ] All tests pass
- [ ] New tests added for new features
- [ ] Documentation updated
- [ ] Commit messages are clear
- [ ] Branch is up to date with main

### Submitting PR

1. Push your branch to your fork
2. Go to the original repository
3. Click "New Pull Request"
4. Select your branch
5. Fill out the PR template

### PR Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Code refactoring

## Testing
How has this been tested?

## Screenshots (if applicable)
Add screenshots for UI changes

## Checklist
- [ ] Tests pass
- [ ] Documentation updated
- [ ] Code follows style guide
```

### Review Process

1. Maintainers will review your PR
2. Address any requested changes
3. Once approved, PR will be merged
4. Your contribution will be credited

## Issue Guidelines

### Creating Issues

#### Bug Reports

```markdown
**Describe the bug**
Clear description of the bug

**To Reproduce**
1. Go to '...'
2. Click on '...'
3. See error

**Expected behavior**
What should happen

**Screenshots**
If applicable

**Environment**
- OS: [e.g., Ubuntu 20.04]
- Python version: [e.g., 3.11]
- Browser: [e.g., Chrome 120]
```

#### Feature Requests

```markdown
**Is your feature request related to a problem?**
Description of the problem

**Describe the solution**
How should it work?

**Describe alternatives**
Other solutions you've considered

**Additional context**
Any other information
```

### Issue Labels

- `bug` - Something isn't working
- `enhancement` - New feature or request
- `documentation` - Documentation improvements
- `good first issue` - Good for newcomers
- `help wanted` - Extra attention needed
- `question` - Further information requested

## Areas for Contribution

### High Priority

1. **More Cryptocurrencies**
   - Add support for additional coins
   - Improve coin data fetching

2. **Advanced ML Models**
   - Implement LSTM/GRU models
   - Add ensemble techniques
   - Improve prediction accuracy

3. **Real-time Updates**
   - WebSocket implementation
   - Live price updates
   - Real-time predictions

4. **Testing**
   - Increase test coverage
   - Add integration tests
   - Performance testing

### Medium Priority

1. **Documentation**
   - Improve API documentation
   - Add tutorials
   - Create video guides

2. **UI/UX Improvements**
   - Better mobile experience
   - Dark mode
   - Accessibility improvements

3. **Performance**
   - Optimize caching
   - Reduce API calls
   - Faster predictions

### Low Priority

1. **Internationalization**
   - Multi-language support
   - Localized formatting

2. **Analytics**
   - User behavior tracking
   - Performance metrics
   - Prediction accuracy tracking

## Development Tips

### Debugging

```python
# Use Python debugger
import pdb; pdb.set_trace()

# Or use breakpoint() (Python 3.7+)
breakpoint()

# Logging
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.debug("Debug message")
```

### Testing API Locally

```bash
# Using curl
curl http://localhost:5000/api/health

# Using httpie
http GET localhost:5000/api/health

# Using Python
python -c "import requests; print(requests.get('http://localhost:5000/api/health').json())"
```

### Database Migrations (Future)

When we add a database:

```bash
# Create migration
flask db migrate -m "description"

# Apply migration
flask db upgrade
```

## Questions?

- Check existing issues
- Read documentation
- Ask in discussions
- Contact maintainers

## Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md
- Mentioned in release notes
- Credited in commit history

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to EPICcrypto! 🚀
