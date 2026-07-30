# Fault Lens Frontend Architecture

Here is a graph representing the architectural directory structure of the `fault_lens_fe` application. It follows a modular architecture.

```mermaid
graph TD
    src[src] --> app[app - Next.js App Router]
    src --> components[components - Shared UI Components]
    src --> lib[lib - Shared Libraries & Configs]
    src --> modules[modules - Feature Modules]
    src --> providers[providers - React Context Providers]
    src --> theme[theme - Design System]
    src --> types[types - Global TypeScript Types]
    
    app --> auth_routes["(auth) - Login/Register pages"]
    app --> dev_routes["(dev) - Development pages"]
    app --> protected_routes["(protected) - Authenticated pages"]
    
    modules --> auth[auth module]
    
    auth --> auth_api[api - API Definitions]
    auth --> auth_components[components - Auth UI Components]
    auth --> auth_guards[guards - Route Guards]
    auth --> auth_hooks[hooks - React Query Hooks]
    auth --> auth_schemas[schemas - Validation Schemas]
    auth --> auth_services[services - Business Logic]
    auth --> auth_store[store - Zustand State]
    auth --> auth_types[types - Module Types]
    auth --> auth_utils[utils - Auth Utilities]
```

## Directory Tree

```
src/
├── app/                  # Next.js 13+ App Router entry points
│   ├── (auth)/           # Authentication routes (login, register)
│   ├── (dev)/            # Development-only routes
│   └── (protected)/      # Authenticated/Protected routes
├── components/           # Global shared UI components
├── constants/            # Global constants and env config
├── lib/                  # Library configurations (e.g., Axios setup)
├── modules/              # Feature-driven modular architecture
│   └── auth/             # Authentication feature module
│       ├── api/          # Network requests to backend
│       ├── components/   # Specific UI components for auth
│       ├── guards/       # Route protection guards
│       ├── hooks/        # Data-fetching and logic hooks
│       ├── schemas/      # Zod validation schemas
│       ├── services/     # Business logic layer
│       ├── store/        # Zustand state management
│       ├── types/        # TypeScript interfaces for auth
│       └── utils/        # Auth helper functions
├── providers/            # React context providers (e.g. AuthProvider)
├── theme/                # UI theme and styling definitions
└── types/                # Global TypeScript definitions
```
