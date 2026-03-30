# Customizing Wasp Signup with Extra Fields

## Background
Wasp provides a powerful authentication system out of the box. While the default setup handles email/password or social logins, many real-world applications require collecting additional information during registration, such as a user's full name or organization. This task involves extending the Wasp `User` entity and the built-in `SignupForm` to collect and save a `fullName` field.

## Requirements
- **Database Schema**: Update the `User` entity to include a `fullName` string field.
- **Backend Logic**: Implement a `userSignupFields` function to process and validate the `fullName` from the signup data.
- **Frontend UI**: Customize the `SignupForm` component to include a "Full Name" input field with basic validation.
- **Display**: Show the `fullName` of the logged-in user on the main page.

## Implementation Guide

### 1. Project Setup
Initialize a new Wasp project in `/home/user/my-auth-app`:
```bash
wasp new my-auth-app
cd my-auth-app
```

### 2. Update Schema (`main.wasp`)
Modify the `User` entity to add `fullName`: 
```wasp
entity User {
  id       Int     @id @default(autoincrement())
  username String  @unique
  password String
  fullName String  // Add this field
}
```

### 3. Configure Auth (`main.wasp`)
In the `auth` section of your `app` declaration, add the `userSignupFields` import:
```wasp
app myAuthApp {
  wasp: { version: "^0.15.0" },
  title: "My Auth App",
  auth: {
    userEntity: User,
    methods: { usernameAndPassword: {} },
    onAuthFailedRedirectTo: "/login",
    userSignupFields: import { userSignupFields } from "@src/auth/signup.js"
  }
}
```

### 4. Backend Logic (`src/auth/signup.js`)
Create `src/auth/signup.js` and export `userSignupFields`. Use `defineUserSignupFields` to map the incoming data to your entity fields:
```javascript
import { defineUserSignupFields } from 'wasp/server/auth'

export const userSignupFields = defineUserSignupFields({
  fullName: (data) => {
    if (!data.fullName) {
      throw new Error('Full name is required')
    }
    return data.fullName
  },
})
```

### 5. Frontend UI (`src/SignupPage.jsx`)
Customize the `SignupForm` by passing the `additionalFields` prop:
```javascript
import { SignupForm } from 'wasp/client/auth'

export const SignupPage = () => {
  return (
    <SignupForm
      additionalFields={[
        {
          name: 'fullName',
          label: 'Full Name',
          type: 'input',
          validations: {
            required: 'Full name is required',
          },
        },
      ]}
    />
  )
}
```
Remember to update `main.wasp` to use this custom `SignupPage` component for the `/signup` route.

### 6. Display User Info (`src/MainPage.jsx`)
Update the `MainPage` to display the user's full name:
```javascript
export const MainPage = ({ user }) => {
  return (
    <div>
      <h1>Hello, {user.fullName}!</h1>
      {/* ... logout button ... */}
    </div>
  )
}
```

## Constraints
- Project path: `/home/user/my-auth-app`
- Start command: `wasp start` (Note: You'll need to run `wasp db migrate-dev` first)
- Port: 3000