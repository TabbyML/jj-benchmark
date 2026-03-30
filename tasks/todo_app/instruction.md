# Wasp Todo List Application

## Background
Wasp is a declarative DSL for building full-stack web applications using React, Node.js, and Prisma. In this task, you will build a simple, multi-user Todo List application that demonstrates the core features of Wasp: Entities, Operations (Queries & Actions), and Authentication.

## Requirements
- **Authentication**: Implement username and password authentication.
- **Data Model**:
    - `User` entity to store user information.
    - `Task` entity with `description` (String) and `isDone` (Boolean) fields.
    - A one-to-many relationship between `User` and `Task`.
- **Operations**:
    - `getTasks` Query: Fetch only the tasks belonging to the logged-in user.
    - `createTask` Action: Create a new task for the logged-in user.
    - `updateTask` Action: Toggle the `isDone` status of a specific task.
- **Frontend**:
    - A login/signup page using Wasp's built-in Auth UI.
    - A main page (protected) that displays the user's tasks.
    - A form to add new tasks.
    - Checkboxes to mark tasks as completed.
    - A logout button.

## Implementation Guide
1. **Initialize Project**:
   - Create a new Wasp project in `/home/user/todo-app` using the minimal template: `wasp new todo-app -t minimal`.
2. **Define Schema**:
   - In `schema.prisma`, define the `User` and `Task` models with the appropriate relation.
3. **Configure App**:
   - In `main.wasp`, set up the `app` declaration with `auth` (using `usernameAndPassword`).
   - Define `route` and `page` for `MainPage`, `LoginPage`, and `SignupPage`.
   - Set `authRequired: true` for the `MainPage`.
4. **Implement Operations**:
   - Declare `query getTasks`, `action createTask`, and `action updateTask` in `main.wasp`.
   - Implement the logic in `src/queries.ts` and `src/actions.ts`, ensuring you use `context.user` for security.
5. **Build UI**:
   - Use Wasp's `LoginForm` and `SignupForm` for authentication pages.
   - Use `useQuery` and `useAction` hooks in `src/MainPage.tsx` to interact with the backend.
6. **Database Migration**:
   - Run `wasp db migrate-dev` to apply your schema changes.

## Constraints
- **Project Path**: `/home/user/todo-app`
- **Start Command**: `wasp start`
- **Port**: 3000
- **Database**: SQLite (default)
