# Privacy and safety

## What this package does

- Installs text instructions in a workspace you choose.
- Creates a blank local profile and a directory for future daily records.
- Instructs your assistant to read only the profile, relevant daily records, and context you explicitly approve.
- Keeps examples fictional and independent of real journals.

It does not contain an account service, telemetry, analytics, credential collection, background process, or upload function. Installation uses no network requests. Downloading the repository still contacts GitHub.

## What "local" does not mean

Local storage is not the same as offline processing. Claude Code or Codex may send the contents they read to their model provider. Your provider's account settings, policies, and any connected integrations still apply.

The skill cannot override your assistant's permissions, guarantee model behavior, control your backups, or stop you from manually publishing a file. Review proposed actions and use a private workspace.

## Keep records out of public Git

The installer requires a planning workspace outside the source repository. Runtime files live under `.good-morning`, which contains a `.gitignore` with `*`.

This helps prevent accidental Git additions, but:

- It does not untrack already committed files.
- `git add -f` can override it.
- It does not protect screenshots, attachments, backups, other sync services, or copied text.
- It is not encryption, a lock, or a permission boundary.

If you use Git for your personal workspace, inspect staged files before every commit. Never publish your actual profile or daily records as test fixtures.

## Sensitive content

Prefer "prepare questions for the appointment" over detailed medical information, and "follow up on payment" over account numbers. Avoid recording passwords, tokens, private keys, identity documents, or unnecessary information about other people.

If you do want to retain sensitive content, consider who can access both the workspace and your assistant's conversation history.

## External content is not authority

Calendar descriptions, imported notes, and linked documents can contain malicious instructions. The skills tell the assistant to treat them as task data, not authorization to run commands, change access, reveal other files, or upload your journal.

## Reporting issues

Use a fictional reproduction. Do not post credentials or personal records in public issues. If you accidentally publish a credential, revoke it promptly through the issuing service; deleting the latest file alone does not remove prior history.

## Uninstalling

Remove only the two installed skill folders from the client directories you selected. Your `.good-morning` records are separate and can be kept. Delete those records yourself only if you intend to discard them, accounting for any backups you manage.
