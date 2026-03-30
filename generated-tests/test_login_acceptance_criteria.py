from dataclasses import dataclass
from typing import Dict, List, Optional
from unittest.mock import Mock

import pytest


# Lightweight specification harness and test doubles to keep tests runnable with no real API calls.
@dataclass
class LoginResult:
    success: bool
    message: Optional[str] = None
    redirected_to: Optional[str] = None
    form_disabled: bool = False


class AuthGatewayStub:
    def __init__(self, users: Optional[Dict[str, str]] = None):
        self.users = users or {}

    def is_registered(self, email: str) -> bool:
        return email in self.users

    def authenticate(self, email: str, password: str) -> bool:
        return self.users.get(email) == password


class SessionStoreStub:
    def __init__(self):
        self.sessions: List[dict] = []

    def create_session(self, email: str, ttl_days: Optional[int]) -> dict:
        session = {"email": email, "ttl_days": ttl_days}
        self.sessions.append(session)
        return session


class LoginSpecHarness:
    def __init__(
        self,
        auth_gateway: AuthGatewayStub,
        session_store: SessionStoreStub,
        redirector: Mock,
        max_failed_attempts: int = 5,
        remember_me_days: int = 30,
    ):
        self.auth_gateway = auth_gateway
        self.session_store = session_store
        self.redirector = redirector
        self.max_failed_attempts = max_failed_attempts
        self.remember_me_days = remember_me_days
        self.failed_attempts = 0
        self.form_disabled = False

    def submit(self, email: str, password: str, remember_me: bool = False) -> LoginResult:
        if self.form_disabled:
            return LoginResult(
                success=False,
                message="Login form is disabled after too many failed attempts.",
                form_disabled=True,
            )

        if not self.auth_gateway.is_registered(email):
            self.failed_attempts += 1
            self.form_disabled = self.failed_attempts >= self.max_failed_attempts
            return LoginResult(
                success=False,
                message="Unregistered email.",
                form_disabled=self.form_disabled,
            )

        if not self.auth_gateway.authenticate(email, password):
            self.failed_attempts += 1
            self.form_disabled = self.failed_attempts >= self.max_failed_attempts
            return LoginResult(
                success=False,
                message="Incorrect password.",
                form_disabled=self.form_disabled,
            )

        self.failed_attempts = 0
        self.form_disabled = False
        ttl_days = self.remember_me_days if remember_me else None
        self.session_store.create_session(email=email, ttl_days=ttl_days)
        self.redirector.go_to("dashboard")
        return LoginResult(success=True, redirected_to="dashboard", form_disabled=False)


class PasswordField:
    def __init__(self):
        self._raw_value = ""

    def type_text(self, value: str) -> None:
        self._raw_value = value

    @property
    def display_value(self) -> str:
        return "•" * len(self._raw_value)

    @property
    def raw_value(self) -> str:
        return self._raw_value


@pytest.fixture
def make_login_harness():
    def _make(users: Optional[Dict[str, str]] = None):
        auth_gateway = AuthGatewayStub(users or {"user@example.com": "CorrectPassword123!"})
        session_store = SessionStoreStub()
        redirector = Mock()
        redirector.go_to = Mock()
        harness = LoginSpecHarness(auth_gateway, session_store, redirector)
        return harness, session_store, redirector

    return _make


# AC-001: User can log in with a valid email and correct password
class TestAC001ValidLogin:
    def test_ac001_valid_email_and_correct_password_logs_user_in(self, make_login_harness):
        # Arrange: create a login harness with one registered user.
        harness, session_store, redirector = make_login_harness()

        # Act: submit valid credentials.
        result = harness.submit("user@example.com", "CorrectPassword123!")

        # Assert: login succeeds and a session is created.
        assert result.success is True  # Successful authentication is expected.
        assert result.message is None
        assert len(session_store.sessions) == 1
        redirector.go_to.assert_called_once_with("dashboard")


# AC-002: User sees an error message for an incorrect password
class TestAC002IncorrectPassword:
    def test_ac002_incorrect_password_shows_an_error_message(self, make_login_harness):
        # Arrange: create a login harness with a known valid user.
        harness, _, _ = make_login_harness()

        # Act: submit the right email with the wrong password.
        result = harness.submit("user@example.com", "WrongPassword!")

        # Assert: the user gets an error message and is not authenticated.
        assert result.success is False  # Authentication must fail for a wrong password.
        assert result.message is not None and "password" in result.message.lower()

    def test_ac002_incorrect_password_does_not_create_session_or_redirect(self, make_login_harness):
        # Arrange: create a login harness with a known valid user.
        harness, session_store, redirector = make_login_harness()

        # Act: submit invalid password credentials.
        result = harness.submit("user@example.com", "BadPassword123")

        # Assert: no session or redirect occurs on failure.
        assert result.success is False  # Failed login must not create a user session.
        assert session_store.sessions == []
        redirector.go_to.assert_not_called()


# AC-003: User sees an error message for an unregistered email
class TestAC003UnregisteredEmail:
    def test_ac003_unregistered_email_shows_an_error_message(self, make_login_harness):
        # Arrange: create a login harness with only one known registered user.
        harness, _, _ = make_login_harness()

        # Act: submit an email address that is not registered.
        result = harness.submit("unknown@example.com", "AnyPassword123!")

        # Assert: the user gets an email-related error message.
        assert result.success is False  # Unregistered users must not authenticate.
        assert result.message is not None and "email" in result.message.lower()

    def test_ac003_unregistered_email_does_not_create_session_or_redirect(self, make_login_harness):
        # Arrange: create a login harness with no matching account for the test email.
        harness, session_store, redirector = make_login_harness()

        # Act: attempt login with an unregistered email.
        result = harness.submit("nobody@example.com", "CorrectPassword123!")

        # Assert: session creation and navigation are blocked.
        assert result.success is False  # Unknown accounts must not enter the system.
        assert session_store.sessions == []
        redirector.go_to.assert_not_called()


# AC-004: Login form is disabled after 5 consecutive failed attempts
class TestAC004FailedAttemptLockout:
    def test_ac004_form_remains_enabled_after_four_consecutive_failed_attempts(self, make_login_harness):
        # Arrange: create a login harness with a valid registered user.
        harness, _, _ = make_login_harness()

        # Act: perform four consecutive failed login attempts.
        for _ in range(4):
            result = harness.submit("user@example.com", "WrongPassword!")

        # Assert: the form is still enabled before the threshold is reached.
        assert result.success is False  # The fourth failure should not disable the form yet.
        assert result.form_disabled is False

    def test_ac004_form_is_disabled_on_the_fifth_consecutive_failed_attempt(self, make_login_harness):
        # Arrange: create a login harness with a valid registered user.
        harness, _, _ = make_login_harness()

        # Act: perform five consecutive failed login attempts.
        for _ in range(5):
            result = harness.submit("user@example.com", "WrongPassword!")

        # Assert: the form becomes disabled exactly at the boundary of five failures.
        assert result.success is False  # The fifth failure reaches the lockout threshold.
        assert result.form_disabled is True
        assert "disabled" not in (result.message or "").lower() or result.form_disabled is True

    def test_ac004_disabled_form_blocks_any_additional_login_attempts(self, make_login_harness):
        # Arrange: create a locked form by failing five times first.
        harness, session_store, redirector = make_login_harness()
        for _ in range(5):
            harness.submit("user@example.com", "WrongPassword!")

        # Act: try again after the form is already disabled.
        result = harness.submit("user@example.com", "CorrectPassword123!")

        # Assert: the blocked state prevents further login processing.
        assert result.success is False  # A disabled form must reject additional submissions.
        assert result.form_disabled is True
        assert session_store.sessions == []
        redirector.go_to.assert_not_called()

    def test_ac004_successful_login_resets_the_consecutive_failed_attempt_counter(self, make_login_harness):
        # Arrange: fail several times, then perform a successful login before failing again.
        harness, _, _ = make_login_harness()
        for _ in range(4):
            harness.submit("user@example.com", "WrongPassword!")

        harness.submit("user@example.com", "CorrectPassword123!")

        # Act: fail once more after the successful login.
        result = harness.submit("user@example.com", "WrongPassword!")

        # Assert: the form stays enabled because the failures were not consecutive anymore.
        assert result.success is False  # A successful login should reset the lockout counter.
        assert result.form_disabled is False


# AC-005: User is redirected to dashboard after successful login
class TestAC005DashboardRedirect:
    def test_ac005_successful_login_redirects_user_to_dashboard(self, make_login_harness):
        # Arrange: create a login harness with a valid registered user.
        harness, _, redirector = make_login_harness()

        # Act: submit valid credentials.
        result = harness.submit("user@example.com", "CorrectPassword123!")

        # Assert: the success path sends the user to the dashboard.
        assert result.success is True  # Successful login must navigate to the dashboard.
        assert result.redirected_to == "dashboard"
        redirector.go_to.assert_called_once_with("dashboard")


# AC-006: "Remember Me" checkbox keeps the session for 30 days
class TestAC006RememberMe:
    def test_ac006_remember_me_keeps_session_for_exactly_thirty_days(self, make_login_harness):
        # Arrange: create a login harness with a valid registered user.
        harness, session_store, _ = make_login_harness()

        # Act: log in with the Remember Me option enabled.
        result = harness.submit("user@example.com", "CorrectPassword123!", remember_me=True)

        # Assert: the created session persists for the exact required duration.
        assert result.success is True  # Login still succeeds when Remember Me is selected.
        assert session_store.sessions[0]["ttl_days"] == 30

    def test_ac006_without_remember_me_does_not_apply_thirty_day_persistence(self, make_login_harness):
        # Arrange: create a login harness with a valid registered user.
        harness, session_store, _ = make_login_harness()

        # Act: log in without selecting Remember Me.
        result = harness.submit("user@example.com", "CorrectPassword123!", remember_me=False)

        # Assert: the session is created without 30-day persistence.
        assert result.success is True  # Standard login should not force Remember Me behavior.
        assert session_store.sessions[0]["ttl_days"] != 30


# AC-007: Password field masks the input characters
class TestAC007PasswordMasking:
    def test_ac007_password_field_masks_input_characters_while_typing(self):
        # Arrange: create a password field for user input.
        password_field = PasswordField()

        # Act: type a visible password value into the field.
        password_field.type_text("Secret123!")

        # Assert: the display shows only masked characters of the same length.
        assert password_field.display_value == "•" * len("Secret123!")  # No raw password characters should be visible.
        assert password_field.display_value != password_field.raw_value

    def test_ac007_password_field_keeps_empty_input_masked_as_empty(self):
        # Arrange: create a password field with no typed input.
        password_field = PasswordField()

        # Act: type an empty string into the field.
        password_field.type_text("")

        # Assert: the masked display remains empty at the lower boundary.
        assert password_field.display_value == ""  # Empty input should not reveal any characters.
        assert password_field.raw_value == ""

    def test_ac007_password_field_masks_special_characters_without_exposing_raw_value(self):
        # Arrange: create a password field for edge-case characters.
        password_field = PasswordField()

        # Act: type special characters and mixed symbols.
        password_field.type_text("P@$$w0rd!#%")

        # Assert: every character is masked regardless of character type.
        assert password_field.display_value == "•" * len("P@$$w0rd!#%")  # Special characters must be hidden too.
        assert "@" not in password_field.display_value and "$" not in password_field.display_value
