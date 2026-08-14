# Organization Model

## Goal

Organizations provide multi-tenancy.

Each customer's data is isolated from every other customer's data.

---

# Relationships

User

↓

OrganizationMember

↓

Organization

↓

Projects

---

# Organization Entity

Fields

- id
- name
- slug
- logo
- owner_id
- timezone
- plan
- created_at
- updated_at

---

# Membership Entity

Fields

- id
- organization_id
- user_id
- role
- status
- joined_at

Purpose

Represents the relationship between a User and an Organization.

A user may belong to many organizations.

An organization may contain many users.

---

# Project Entity

Fields

- id
- organization_id
- name
- description
- environment
- created_at
- updated_at

Examples

Acme Ltd

Projects

- Frontend
- Backend
- Payment API
- Mobile API

---

# Project Ownership

Every Project owns:

- Log Sources
- Logs
- Alert Rules
- API Keys
- Incidents
- AI Analysis
- Dashboard Metrics

Nothing operational belongs directly to the Organization.

The Organization acts as the tenant boundary.

---

# Organization Dashboard

Organization dashboards aggregate data from every project.

Example

Acme Ltd

Projects: 8

Open Incidents: 3

Critical Alerts: 5

Logs Today: 14M

Health Score: 91%

---

# Project Dashboard

Project dashboards show application-specific data.

Example

Payment API

Latency

Requests/sec

Top Errors

Open Incidents

Recent Deployments

AI Summary