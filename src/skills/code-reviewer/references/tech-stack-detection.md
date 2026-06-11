# Tech Stack Detection

## Overview

Before reviewing code, detect the tech stack to load appropriate rule sets. This ensures relevant, actionable feedback.

## Detection Strategy

### 1. Check package.json

**Always start here** - most reliable source:

```bash
cat package.json | jq '.dependencies, .devDependencies'
```

### 2. Examine File Paths

Framework-specific directories reveal tech stack:

- `src/**/*.module.ts`, `src/**/*.controller.ts`, `src/**/*.service.ts` → NestJS
- `routes/`, `middleware/` → Express
- `app/`, `components/`, `pages/` → Next.js/React
- `*.component.ts` → Angular
- `*.vue` → Vue.js

### 3. Check File Extensions

- `.ts`, `.tsx` → TypeScript
- `.jsx` → React
- `.vue` → Vue
- `.component.ts` → Angular
- `.graphql`, `.gql` → GraphQL

### 4. Review Imports

Check top of changed files:

```typescript
import { Injectable, Module } from '@nestjs/common';  // NestJS
import express from 'express';                         // Express
import { PrismaClient } from '@prisma/client';        // Prisma
```

### 5. Look for Config Files

- `nest-cli.json` → NestJS
- `angular.json` → Angular
- `next.config.js` → Next.js
- `vue.config.js` → Vue
- `tailwind.config.js` → Tailwind CSS
- `schema.prisma` → Prisma

## Backend Frameworks

### NestJS

**Detection Signals:**
- Dependencies: `@nestjs/core`, `@nestjs/common`, `@nestjs/platform-express`
- Files: `*.module.ts`, `*.service.ts`, `*.controller.ts`, `*.guard.ts`, `*.interceptor.ts`
- Config: `nest-cli.json`
- Patterns: `@Injectable()`, `@Controller()`, `@Module()` decorators

**Load Rules:**
- [rules-backend-nestjs.md](./rules-backend-nestjs.md)
- [rules-backend.md](./rules-backend.md)
- [rules-api-design.md](./rules-api-design.md) if REST/GraphQL endpoints

### Express

**Detection Signals:**
- Dependencies: `express`
- Files: Routes in `routes/`, middleware in `middleware/`
- Patterns: `app.get()`, `app.post()`, `router.use()`, `req`, `res`, `next`

**Load Rules:**
- [rules-backend.md](./rules-backend.md)
- [rules-api-design.md](./rules-api-design.md)

### Fastify

**Detection Signals:**
- Dependencies: `fastify`
- Patterns: `fastify.register()`, `fastify.route()`

**Load Rules:**
- [rules-backend.md](./rules-backend.md)
- [rules-api-design.md](./rules-api-design.md)

## Database & ORM

### TypeORM

**Detection Signals:**
- Dependencies: `typeorm`
- Files: `*.entity.ts`
- Patterns: `@Entity()`, `@Column()`, `@Repository()` decorators

**Load Rules:**
- [rules-data-integrity.md](./rules-data-integrity.md)
- [rules-performance.md](./rules-performance.md) (N+1 query checks)

### Prisma

**Detection Signals:**
- Dependencies: `@prisma/client`, `prisma`
- Files: `schema.prisma`
- Patterns: `prisma.model.findMany()`, `prisma.model.create()`

**Load Rules:**
- [rules-data-integrity.md](./rules-data-integrity.md)
- [rules-performance.md](./rules-performance.md)

### Sequelize

**Detection Signals:**
- Dependencies: `sequelize`
- Patterns: `sequelize.define()`, model inheritance from `Model`

**Load Rules:**
- [rules-data-integrity.md](./rules-data-integrity.md)

## API Patterns

### GraphQL

**Detection Signals:**
- Dependencies: `@nestjs/graphql`, `apollo-server`, `graphql`, `type-graphql`
- Files: `*.resolver.ts`, `*.graphql`, `*.gql`
- Patterns: `@Resolver()`, `@Query()`, `@Mutation()`, `@Field()` decorators

**Load Rules:**
- [rules-api-design.md](./rules-api-design.md)
- [rules-security.md](./rules-security.md) (GraphQL-specific: query depth, complexity)

### REST

**Detection Signals:**
- Controllers with HTTP method decorators: `@Get()`, `@Post()`, `@Put()`, `@Delete()`
- Route definitions: `app.get('/api/users', ...)`
- OpenAPI/Swagger files: `swagger.yaml`, `openapi.json`

**Load Rules:**
- [rules-api-design.md](./rules-api-design.md)
- [rules-security.md](./rules-security.md)

## Frontend Frameworks

### React

**Detection Signals:**
- Dependencies: `react`, `react-dom`
- Files: `*.tsx`, `*.jsx`
- Patterns: `useState`, `useEffect`, `React.Component`, JSX syntax

### Next.js

**Detection Signals:**
- Dependencies: `next`
- Config: `next.config.js`
- Directories: `pages/`, `app/`
- Files: `_app.tsx`, `_document.tsx`, API routes in `pages/api/`

### Vue

**Detection Signals:**
- Dependencies: `vue`
- Files: `*.vue`
- Patterns: `<template>`, `<script>`, `<style>` blocks

## Testing Frameworks

### Jest

**Detection Signals:**
- Dependencies: `jest`, `@types/jest`
- Files: `*.spec.ts`, `*.test.ts`
- Config: `jest.config.js`

**Load Rules:**
- [rules-testing.md](./rules-testing.md)

### Playwright

**Detection Signals:**
- Dependencies: `@playwright/test`
- Files: `*.spec.ts` in `tests/` or `e2e/`
- Config: `playwright.config.ts`

### Vitest

**Detection Signals:**
- Dependencies: `vitest`
- Config: `vitest.config.ts`

## Loading Strategy

### Always Load (Universal Rules)

These apply to ALL code regardless of tech stack:

- [rules-programming-principles.md](./rules-programming-principles.md) (SOLID, DRY, KISS, YAGNI)
- [rules-design-patterns.md](./rules-design-patterns.md) (anti-patterns)
- [rules-security.md](./rules-security.md) (universal security)
- [rules-performance.md](./rules-performance.md) (algorithm complexity)
- [rules-testing.md](./rules-testing.md) (if tests present)
- [rules-readability.md](./rules-readability.md) (naming, complexity)

### Conditionally Load Based on Detection

- **Backend detected?** → Load [rules-backend.md](./rules-backend.md)
- **NestJS detected?** → Load [rules-backend-nestjs.md](./rules-backend-nestjs.md)
- **API endpoints detected?** → Load [rules-api-design.md](./rules-api-design.md)
- **Database/ORM detected?** → Load [rules-data-integrity.md](./rules-data-integrity.md)
- **Business logic detected?** → Load [rules-business-logic.md](./rules-business-logic.md)

## Detection Output Template

Document what you detected:

```markdown
## Tech Stack Detected

**Category:** Backend API (NestJS + REST + Prisma)

**Framework:** NestJS 10.x
**Database:** PostgreSQL via Prisma
**API Style:** REST
**Testing:** Jest

**Loaded Rule Sets:**

- ✅ Programming Principles
- ✅ Design Patterns & Anti-Patterns
- ✅ Security Best Practices
- ✅ Performance Optimization
- ✅ Testing Best Practices
- ✅ Code Readability & Complexity
- ✅ General Backend Rules
- ✅ NestJS-Specific Rules
- ✅ API Design Rules (REST)
- ✅ Data Integrity & Validation (Prisma detected)

**Files to Review:**

- `src/users/users.service.ts` (NestJS service)
- `src/users/users.controller.ts` (NestJS REST controller)
- `src/users/dto/create-user.dto.ts` (DTO with validation)
- `src/users/users.service.spec.ts` (Jest tests)

**Detected Patterns:**

- Dependency injection via constructor
- Guards for authentication/authorization
- DTOs with class-validator decorators
- Prisma ORM for database access
```

## Progressive Loading

**Start broad, narrow down:**

1. Load universal rules (always)
2. Detect backend vs frontend vs fullstack
3. Detect specific framework (NestJS, React, etc.)
4. Detect additional patterns (GraphQL, TypeORM, etc.)
5. Load corresponding rule sets

**Don't overload:** Only load what's relevant to the changes being reviewed.
