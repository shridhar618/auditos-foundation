export interface AuthenticatedUser {
  id: string;
  full_name: string;
  email: string;
  organization_id: string;
  organization_name: string;
  role: string;
  permissions: string[];
}

export interface TokenResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
}

export interface LoginPayload {
  email: string;
  password: string;
}

export interface RegisterOrganizationPayload {
  organization_name: string;
  full_name: string;
  email: string;
  password: string;
}
