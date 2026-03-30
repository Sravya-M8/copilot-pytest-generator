## Feature: User Login

**User Story US-001:**
As a registered user,
I want to log in with my email and password,
So that I can access my account dashboard.

**Acceptance Criteria:**
- AC-001: User can log in with a valid email and correct password
- AC-002: User sees an error message for an incorrect password
- AC-003: User sees an error message for an unregistered email
- AC-004: Login form is disabled after 5 consecutive failed attempts
- AC-005: User is redirected to dashboard after successful login
- AC-006: "Remember Me" checkbox keeps the session for 30 days
- AC-007: Password field masks the input characters

**Edge Cases:**
- Empty email field submission
- Empty password field submission
- Email with invalid format (missing @, no domain)
- SQL injection attempt in input fields
- Extremely long input strings (>255 characters)

**Non-Functional:**
- Login response time must be under 2 seconds
- Must work on Chrome, Firefox, Safari, Edge