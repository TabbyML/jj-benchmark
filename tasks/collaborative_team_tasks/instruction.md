# Collaborative Task Manager with Role-Based Access

## Background
Wasp is a full-stack framework that uses a declarative DSL to define application structure, combined with React and Node.js. This task involves building a multi-user task management system where users can belong to teams, and access is controlled based on membership.

## Requirements
1.  **Data Model**:
    *   `User`: Standard auth user.
    *   `Team`: Has a `name` and a list of `members` (Users).
    *   `Task`: Has a `description`, `isDone` status, and belongs to a `Team`.
2.  **Authentication**:
    *   Use `usernameAndPassword` authentication.
    *   Customize the signup process to include a `fullName` field on the `User` entity.
3.  **Operations**:
    *   **Query** `getMyTeams`: Returns all teams the logged-in user belongs to.
    *   **Action** `createTeam`: Creates a new team and adds the creator as the first member.
    *   **Action** `createTask`: Creates a task for a specific team. **Constraint**: Only team members can create tasks for that team.
    *   **Query** `getTeamTasks`: Returns all tasks for a specific team. **Constraint**: Only team members can view tasks for that team.
4.  **Frontend**:
    *   A Dashboard page showing the user's teams.
    *   A Team Detail page (using dynamic routes `/team/:id`) showing tasks and a form to add new tasks.
    *   Use Wasp's `useQuery` and `useAction` hooks for data fetching and mutations.

## Implementation Guide
1.  **Project Setup**:
    *   Initialize a new Wasp project: `wasp new team_manager -t minimal`.
    *   Base path: `/home/user/team_manager`.
2.  **Schema Definition**:
    *   Define `User`, `Team`, and `Task` in `schema.prisma`.
    *   Ensure proper relations (Many-to-Many between User and Team, One-to-Many between Team and Task).
3.  **Auth Configuration**:
    *   In `main.wasp`, configure `auth` with `userSignupFields` to capture `fullName`.
    *   Implement `userSignupFields` in `src/auth.ts`.
4.  **Backend Logic**:
    *   Implement queries and actions in `src/queries.ts` and `src/actions.ts`.
    *   Use `context.user` to verify identity and `context.entities` for database access.
    *   Throw `HttpError(403)` if a user tries to access/modify a team they don't belong to.
5.  **Frontend Implementation**:
    *   Create `src/pages/Dashboard.tsx` and `src/pages/TeamPage.tsx`.
    *   Use `wasp/client/operations` to call your queries and actions.

## Constraints
- Project path: `/home/user/team_manager`
- Start command: `wasp start`
- Port: 3000
- Database: SQLite (default)
- Use TypeScript for all implementation files.
