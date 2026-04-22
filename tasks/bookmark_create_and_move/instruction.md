# Manage Bookmarks in Jujutsu

## Background
In Jujutsu (`jj`), bookmarks are named pointers to revisions (similar to Git branches). They are used to mark specific commits, especially when integrating with Git remotes. This task tests your ability to create a bookmark and then move it to a different revision.

## Requirements
- You have a Jujutsu repository initialized at `/home/user/my-project`.
- Create a new bookmark named `feature-x` pointing to the initial working copy commit.
- Create a new commit on top of it with the description `add feature y`.
- Move the `feature-x` bookmark to point to this new commit.

## Implementation
1. Navigate to `/home/user/my-project`.
2. Create the bookmark `feature-x` on the current working copy.
3. Run `jj new -m "add feature y"` to create a new commit.
4. Move the `feature-x` bookmark to the new working copy commit.

## Constraints
- Project path: `/home/user/my-project`
- Use only `jj` commands.