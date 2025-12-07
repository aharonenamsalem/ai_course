# GitHub Copilot Custom Instructions

## 1. Python Naming Conventions
- **Files and modules**: Use lowercase with underscores (snake_case): `data_processor.py`, `aws_db_utils.py`
- **Functions and variables**: Use snake_case: `calculate_total()`, `user_name`, `student_count`
- **Classes**: Use PascalCase: `DatabaseConnection`, `StudentRecord`, `DataProcessor`
- **Constants**: Use UPPER_SNAKE_CASE: `MAX_RETRIES`, `API_TIMEOUT`, `DEFAULT_PORT`
- **Private attributes**: Prefix with single underscore: `_internal_cache`, `_validate_input()`

## 2. JavaScript/TypeScript Naming Conventions
- **Variables and functions**: Use camelCase: `userName`, `calculateScore()`, `fetchData()`
- **Classes and components**: Use PascalCase: `UserProfile`, `DataTable`, `ApiClient`
- **Constants**: Use UPPER_SNAKE_CASE: `API_BASE_URL`, `MAX_ITEMS`
- **Files**: Use kebab-case for modules: `user-profile.js`, `data-utils.js`

## 3. Code Documentation Requirements
- Every function must include a docstring or JSDoc comment explaining:
  - Purpose and what it does
  - Parameters with types
  - Return value with type
  - Exceptions that may be raised
- Use clear, concise language
- Include examples for complex functions
- Keep documentation updated when code changes

**Python Example:**
```python
def fetch_user_data(user_id: int, include_history: bool = False) -> dict:
    """
    Retrieve user data from the database.
    
    Args:
        user_id: Unique identifier for the user
        include_history: Whether to include transaction history
        
    Returns:
        Dictionary containing user information
        
    Raises:
        ValueError: If user_id is negative
        DatabaseError: If connection fails
    """
```

## 4. Error Handling Best Practices
- Always use specific exception types, never bare `except:` clauses
- Provide meaningful error messages that help debugging
- Use try-finally or context managers for resource cleanup
- Log errors before handling or re-raising them
- Fail fast - validate inputs early
- Don't silently ignore exceptions

**Good:**
```python
try:
    result = process_data(input_file)
except FileNotFoundError as e:
    logger.error(f"Input file not found: {input_file}")
    raise
except ValueError as e:
    logger.warning(f"Invalid data format: {e}")
    return default_value
```

## 5. Code Organization and Structure
- **Single Responsibility**: Each function/class should do one thing well
- **Function length**: Keep functions under 50 lines; refactor if longer
- **File organization**: Group related functionality together
- **Import order**:
  1. Standard library imports
  2. Third-party library imports
  3. Local application imports
- **Separation of concerns**: Keep business logic, data access, and presentation separate
- **DRY principle**: Don't Repeat Yourself - extract common code into reusable functions

## 6. Type Hints and Static Typing
- Use type hints for all function parameters and return values in Python
- Leverage TypeScript for JavaScript projects
- Use typing module for complex types: `List`, `Dict`, `Optional`, `Union`, `Tuple`
- Enable static type checking with mypy or similar tools
- Type hints improve code clarity and catch errors early

**Example:**
```python
from typing import List, Optional, Dict, Any

def process_students(
    student_ids: List[int],
    filters: Optional[Dict[str, Any]] = None
) -> List[Dict[str, Any]]:
    """Process and return student records."""
    filters = filters or {}
    # implementation
    return results
```

## 7. Testing Standards
- Write unit tests for all business logic
- Aim for minimum 80% code coverage
- Use descriptive test names: `test_calculate_average_returns_correct_value()`
- Follow Arrange-Act-Assert pattern
- Use fixtures and mocks to isolate tests
- Test edge cases and error conditions
- Run tests before committing code

## 8. Version Control Practices
- Write clear commit messages in present tense: "Add user authentication feature"
- Keep commits atomic - one logical change per commit
- Never commit sensitive data (API keys, passwords, tokens)
- Use meaningful branch names: `feature/user-auth`, `fix/database-connection`
- Review your own changes before creating pull requests
- Keep `.gitignore` updated

## 9. Code Comments and Clarity
- Write self-documenting code with clear names
- Use comments to explain "why", not "what"
- Avoid obvious comments that just restate the code
- Remove commented-out code before committing
- Use TODO comments sparingly and track them
- Keep inline comments concise and relevant

**Bad:** `x = x + 1  # increment x`
**Good:** `# Retry count starts at 1 to match user-facing display`

## 10. Security and Best Practices
- Never hardcode credentials or API keys
- Use environment variables for configuration
- Validate and sanitize all user inputs
- Use parameterized queries to prevent SQL injection
- Keep dependencies updated and scan for vulnerabilities
- Follow principle of least privilege
- Handle sensitive data appropriately (encryption, secure deletion)
