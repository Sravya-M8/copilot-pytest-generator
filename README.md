# Test Automation Workspace

A lightweight, GitHub-ready project for turning **user stories and acceptance criteria** into both **automated Pytest test cases** and **manual test cases**.

This workspace currently focuses on a **Login** feature and demonstrates how to:
- derive test scenarios from requirements,
- generate automated tests with `pytest`,
- maintain reusable prompt templates for GitHub Copilot, and
- convert automated tests into manual QA test cases.

---

##  Project Overview

The project is organized around a sample login workflow with clearly defined acceptance criteria such as:
- valid login behavior,
- incorrect password handling,
- unregistered email validation,
- account lockout after repeated failures,
- dashboard redirection,
- remember-me session persistence,
- password masking.

It is useful as a starter workspace for:
- QA engineers,
- SDETs,
- test automation learners,
- teams exploring AI-assisted test generation.

---

##  Features

- **User story driven testing**
- **Pytest-based automated test suite**
- **Manual test case documentation in Markdown and CSV**
- **Reusable Copilot prompt templates** for generating tests faster
- **Mock/stub-based test design** with no real API dependency

---

##  Project Structure

```text
test-automation-workspace/
├── generated-tests/
│   └── test_login_acceptance_criteria.py
├── prompts/
│   └── copilot_prompt_templates.md
├── requirements/
│   ├── user_stories.md
│   ├── manual_test_cases.md
│   └── manual_test_cases.csv
└── README.md
```

---

##  Tech Stack

- **Python**
- **Pytest**
- **unittest.mock**
- **Markdown / CSV** for manual QA artifacts

---

##  Current Test Coverage

The automated suite covers these acceptance criteria for the login feature:

- `AC-001` User can log in with valid credentials
- `AC-002` Error shown for incorrect password
- `AC-003` Error shown for unregistered email
- `AC-004` Form disabled after 5 failed attempts
- `AC-005` Redirect to dashboard after successful login
- `AC-006` Remember Me keeps the session for 30 days
- `AC-007` Password input is masked

---

## How to Run the Tests

### 1. Create and activate a virtual environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 2. Install dependencies

```powershell
pip install pytest
```

### 3. Run the test suite

```powershell
pytest generated-tests/test_login_acceptance_criteria.py
```

---

##  Copilot Prompt Templates

The file `prompts/copilot_prompt_templates.md` contains reusable prompts for tasks like:
- generating a full test suite from a user story,
- expanding edge cases,
- creating parameterized test data,
- converting manual test cases to Pytest,
- converting Pytest tests into manual test cases.

This makes the repo a practical reference for **AI-assisted QA workflows**.

---

##  Manual Test Cases

Manual test cases for the login feature are available here:
- `requirements/manual_test_cases.md`
- `requirements/manual_test_cases.csv`

The CSV version can be opened directly in Excel for QA review or reporting.

---

##  Suggested Use Cases

- Practice writing acceptance-criteria-based tests
- Demonstrate test design in interviews or portfolios
- Prototype QA automation workflows with Copilot
- Maintain traceability from requirements to test cases

---

##  Possible Enhancements

- Add API/UI automation examples
- Include edge-case automation for invalid email formats and empty fields
- Add `requirements.txt`
- Integrate CI with GitHub Actions
- Extend the project with signup, forgot password, and MFA scenarios

---

##  License

This project is for learning, demonstration, and test automation practice.

If you want, you can update this section with your preferred license such as **MIT**.
