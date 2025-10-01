# Contributing to EPICcrypto

Thank you for your interest in contributing to EPICcrypto! This document provides guidelines for contributing to the project.

## Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Focus on what is best for the community
- Show empathy towards other contributors

## How to Contribute

### Reporting Bugs

Before submitting a bug report:
1. Check if the issue already exists
2. Verify it's reproducible
3. Collect relevant information (logs, screenshots)

**Bug Report Template**:
```markdown
**Describe the bug**
A clear description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Go to '...'
2. Click on '...'
3. See error

**Expected behavior**
What you expected to happen.

**Screenshots**
If applicable, add screenshots.

**Environment**
- OS: [e.g., Windows, macOS, Linux]
- Browser: [e.g., Chrome, Firefox]
- Python version: [e.g., 3.11]
```

### Suggesting Features

Feature requests are welcome! Please:
1. Check if it's already suggested
2. Explain the use case
3. Describe expected behavior
4. Consider implementation complexity

**Feature Request Template**:
```markdown
**Feature Description**
Clear description of the feature.

**Use Case**
Why this feature would be useful.

**Proposed Solution**
How you think it could be implemented.

**Alternatives**
Other approaches you've considered.
```

### Code Contributions

#### Setup Development Environment

1. **Fork the repository**
```bash
# Click "Fork" on GitHub
```

2. **Clone your fork**
```bash
git clone https://github.com/YOUR_USERNAME/EPICcrypto.git
cd EPICcrypto
```

3. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

4. **Install dependencies**
```bash
pip install -r requirements.txt
```

5. **Create a branch**
```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

#### Making Changes

**Before coding**:
- Understand the existing architecture
- Read related code
- Plan your changes
- Keep changes minimal and focused

**While coding**:
- Follow Python PEP 8 style guide
- Write clear, self-documenting code
- Add comments for complex logic
- Update documentation as needed

**Code Style Guidelines**:

```python
# Good: Clear function with docstring
def calculate_rsi(prices, period=14):
    """
    Calculate Relative Strength Index
    
    Args:
        prices: List of price values
        period: RSI period (default: 14)
    
    Returns:
        float: RSI value between 0 and 100
    """
    # Implementation...
    pass

# Bad: No docstring, unclear
def calc(p, n=14):
    # Implementation...
    pass
```

**Project Structure**:
```
EPICcrypto/
├── app.py                 # Main Flask application
├── services/              # Business logic layer
│   ├── crypto_data.py    # Data fetching & indicators
│   └── ai_predictor.py   # AI/ML predictions
├── templates/            # HTML templates
├── static/               # CSS, JS, images
│   ├── css/
│   └── js/
├── tests/                # Test files
└── docs/                 # Documentation
```

#### Testing Your Changes

1. **Run existing tests**
```bash
python tests/test_basic.py
```

2. **Test manually**
```bash
python app.py
# Visit http://localhost:5000
# Test your changes thoroughly
```

3. **Test different scenarios**
- Different cryptocurrencies
- Different timeframes
- Error cases
- Edge cases

4. **Check for regressions**
- Ensure existing features still work
- Verify no new errors in console

#### Commit Guidelines

**Commit Message Format**:
```
<type>: <subject>

<body (optional)>

<footer (optional)>
```

**Types**:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

**Examples**:
```bash
# Good commits
git commit -m "feat: add support for XRP cryptocurrency"
git commit -m "fix: correct RSI calculation for edge cases"
git commit -m "docs: update deployment guide for Railway.app"

# Bad commits
git commit -m "fixed stuff"
git commit -m "update"
```

#### Submitting Pull Request

1. **Update your fork**
```bash
git fetch upstream
git merge upstream/main
```

2. **Push your changes**
```bash
git push origin feature/your-feature-name
```

3. **Create Pull Request**
- Go to GitHub
- Click "New Pull Request"
- Select your branch
- Fill in the template

**Pull Request Template**:
```markdown
## Description
Brief description of changes.

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Code refactoring

## Testing
- [ ] Tested locally
- [ ] Tested different scenarios
- [ ] No regressions found

## Checklist
- [ ] Code follows project style
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] Tests pass
```

4. **Respond to feedback**
- Be open to suggestions
- Make requested changes
- Update PR as needed

---

## Development Guidelines

### Adding New Cryptocurrency

1. Update supported coins in `app.py`:
```python
@app.route('/api/coins')
def get_supported_coins():
    coins = [
        # ... existing coins ...
        {'symbol': 'NEW-USD', 'name': 'New Coin'},
    ]
```

2. Ensure Yahoo Finance supports it:
```python
import yfinance as yf
ticker = yf.Ticker("NEW-USD")
data = ticker.history(period="1d")
```

### Adding New Technical Indicator

1. Add calculation in `services/crypto_data.py`:
```python
def calculate_technical_indicators(self, data):
    # ... existing indicators ...
    
    # New indicator
    indicators['new_indicator'] = calculate_new_metric(data)
    
    return indicators
```

2. Update AI predictor if needed:
```python
# services/ai_predictor.py
def prepare_features(self, data):
    df['new_feature'] = # calculation
    return df
```

### Adding New Timeframe

1. Update timeframe map in `services/crypto_data.py`:
```python
timeframe_map = {
    # ... existing ...
    '2h': {'period': '1mo', 'interval': '1h'},
}
```

2. Update frontend selector in `templates/index.html`:
```html
<select id="timeframeSelect">
    <!-- ... existing ... -->
    <option value="2h">2 Hours</option>
</select>
```

### Improving AI Model

1. Add features in `services/ai_predictor.py`:
```python
def prepare_features(self, data):
    # Add new calculated features
    df['new_feature'] = your_calculation(data)
    return df
```

2. Update scoring logic:
```python
def predict(self, data, timeframe='1d'):
    # Modify score calculation
    new_score = calculate_new_signal(df)
    overall_score += new_score
```

3. Test thoroughly with historical data

---

## Documentation

### When to Update Documentation

Update docs when you:
- Add new features
- Change API endpoints
- Modify behavior
- Fix significant bugs

### Documentation Files

- `README.md` - Overview and quick start
- `API_DOCS.md` - API reference
- `DEPLOYMENT.md` - Deployment guides
- `ARCHITECTURE.md` - System architecture
- `QUICKSTART.md` - Quick start guide
- `CONTRIBUTING.md` - This file

### Documentation Style

- Use clear, concise language
- Include code examples
- Add screenshots when helpful
- Keep formatting consistent

---

## Review Process

### What Reviewers Look For

1. **Code Quality**
   - Readable and maintainable
   - Follows project conventions
   - Properly documented

2. **Functionality**
   - Works as intended
   - Handles edge cases
   - No regressions

3. **Testing**
   - Adequately tested
   - All tests pass
   - No new bugs

4. **Documentation**
   - Updated as needed
   - Clear and accurate
   - Examples provided

### Getting Your PR Merged

- **Be patient**: Reviews take time
- **Be responsive**: Address feedback quickly
- **Be understanding**: Changes may be requested
- **Be collaborative**: Work with reviewers

---

## Community

### Getting Help

- **GitHub Issues**: For bugs and features
- **Discussions**: For questions and ideas
- **Code Review**: Learn from feedback

### Recognition

Contributors are recognized in:
- Git commit history
- GitHub contributors page
- Release notes (for significant contributions)

---

## License

By contributing to EPICcrypto, you agree that your contributions will be licensed under the MIT License.

---

## Questions?

If you have questions about contributing:
1. Check existing documentation
2. Search closed issues
3. Open a new issue with your question

---

Thank you for contributing to EPICcrypto! 🚀

Every contribution, no matter how small, helps make this project better for everyone.
