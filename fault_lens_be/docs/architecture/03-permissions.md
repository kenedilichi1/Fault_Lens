# Permissions

## Philosophy

Permissions should remain simple.

Avoid enterprise-style permission matrices until required.

Roles should be understandable by developers.

---

# Roles

Owner

Admin

Developer

Viewer

---

# Owner

Can

- Manage organization
- Delete organization
- Transfer ownership
- Invite users
- Remove users
- Create projects
- Delete projects
- Manage API Keys
- Manage Alerts
- Manage Billing

Cannot

- Remove themselves unless ownership is transferred.

---

# Admin

Can

- Invite users
- Remove users
- Create projects
- Delete projects
- Manage Alerts
- Manage API Keys
- View everything

Cannot

- Delete organization
- Transfer ownership

---

# Developer

Can

- View logs
- Create alerts
- Resolve incidents
- View AI analysis
- Create projects

Cannot

- Invite users
- Remove users
- Manage billing
- Delete organization

---

# Viewer

Can

- View dashboards
- View logs
- View incidents
- View alerts

Cannot

- Create projects
- Create alerts
- Invite users
- Modify settings

---

# Authentication

Every request requires:

Authorization: Bearer <access_token>

Every authenticated request must also be scoped to an Organization.

The active organization determines which resources are accessible.

---

# Authorization

Access checks happen in this order:

1. User authenticated?
2. User belongs to Organization?
3. User has required role?
4. Resource belongs to Organization?

Only then is the request executed.

---

# Future Permissions

Potential additions

- Custom Roles
- Teams
- Project-level Roles
- Service Accounts
- Read-only API Keys

These are intentionally excluded from the MVP.