class AuditOSError(Exception):
    """Base class for all domain errors. Never let raw exceptions leak to clients."""
    status_code: int = 400

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class InvalidCredentialsError(AuditOSError):
    status_code = 401

    def __init__(self):
        super().__init__("Invalid email or password.")


class TokenInvalidError(AuditOSError):
    status_code = 401

    def __init__(self, message: str = "Token is invalid, expired, or has been revoked."):
        super().__init__(message)


class EmailAlreadyExistsError(AuditOSError):
    status_code = 409

    def __init__(self):
        super().__init__("An account with this email already exists.")


class OrganizationSlugTakenError(AuditOSError):
    status_code = 409

    def __init__(self):
        super().__init__("An organization with a similar name already exists.")


class PermissionDeniedError(AuditOSError):
    status_code = 403

    def __init__(self, required_permission: str | None = None):
        message = "You do not have permission to perform this action."
        if required_permission:
            message += f" (requires '{required_permission}')"
        super().__init__(message)


class ResourceNotFoundError(AuditOSError):
    status_code = 404

    def __init__(self, resource: str = "Resource"):
        super().__init__(f"{resource} not found.")
