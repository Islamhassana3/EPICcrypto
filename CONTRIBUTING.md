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

## Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Focus on what is best for the community
- Show empathy towards other contributors