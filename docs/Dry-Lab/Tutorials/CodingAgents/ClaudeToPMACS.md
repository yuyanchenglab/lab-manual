---
layout: default
title: Claude to PMACS
parent: Coding Agents
nav_order: 42
---

<!-- NEW — written from the working setup used on prj2601 (X-SPEAR), Sep 2026. Sister page to Claude to PARCC; the two clusters differ in scheduler (LSF here, SLURM there) and in login (password here, key + Kerberos there). -->

# {{page.title}}

**Owner:** Rushil

## What is happening, in one minute

You run **Claude Code on your laptop**. Nothing is installed on PMACS, and the agent never holds your password. Instead:

1. Your password is stored **once** in your operating system's credential store — the macOS Keychain, or Windows' DPAPI-encrypted user store. Not in a file, not in a `.env`, not in the chat.
2. A tiny helper script, `~/bin/pmacs-connect`, opens one SSH connection to the PMACS head node (`consign.pmacs.upenn.edu`), pulls the password out of the store just long enough to answer the prompt, and leaves the connection open in the background (an SSH *ControlMaster* socket in `~/.ssh/`).
3. **Claude** reuses that open connection for every command — `ssh pmacs 'bjobs'`, `ssh pmacs 'bsub < job.sh'`. When the connection dies (VPN drop, laptop sleep), Claude runs the helper again and carries on. If the helper reports the VPN is down or the password was refused, Claude stops and tells you.

Claude is allowed to run the helper. Claude is **not** allowed to run the command inside it that reads the credential store, or to read any credential file — that is enforced with a deny-list (Section 3), not just a polite request. The password is never printed by anything, so it cannot land in a transcript, a log, a memory file, or a commit.

**Where your files live**

| Where | What goes there | Who touches it |
|---|---|---|
| Your laptop, e.g. `~/Desktop/<project-id>/` | the git repo: code, configs, notes, small result tables, figures | you + Claude, directly |
| PMACS `/project/hipaa_ycheng11lab/<project-id>/<pennkey>/` | a clone of the same repo, plus the **data**, big intermediates, job logs, environments | Claude, only through `ssh pmacs '...'` |
| PMACS `~` (your home) | almost nothing — it is small; keep it to dotfiles | — |
| `/tmp` on the head node | nothing — it is **not** shared with compute nodes | — |

Code moves between the two clones with **git** (push from the laptop, `git pull` on the server), never with copy-paste or `scp`. Data and anything HIPAA-tagged stay on the server: Claude must not `scp` data down, and you must not paste patient-level rows into the chat.

**Compute** never runs on the head node. Everything that does work is submitted with `bsub` to LSF, and Claude checks on it with `bjobs` / `bpeek` / `bkill`. The head node exists to submit jobs, look at small files, and run git.

{: .note-title }
> Why not just an SSH key?
>
> Because PMACS ignores it. Our home directories are provisioned **owned by root and group-writable** (`drwxrwx--- root <pennkey> /home/<pennkey>`), and sshd's `StrictModes` refuses to read `authorized_keys` out of a home directory anyone but the owner can write to. You can `ssh-copy-id` all you like; the server lists `publickey` as an option and then silently falls through to password. There is no `sudo` to fix it yourself.
>
> If you email [psom-pmacshpc@pennmedicine.upenn.edu](mailto:psom-pmacshpc@pennmedicine.upenn.edu) and they agree to make your home directory owner-only-writable (`chmod 750 /home/<pennkey>`), keys will work: add `IdentityFile` to the ssh config below, delete the `password` lines, and skip the credential-store steps entirely. Until then, the setup below is the way.

You need a PMACS account ([Server Access](../../../ServerAccess)) and, off campus, the Global Protect VPN ([PMACS Usage](../Access/PMACS)).

## 1. macOS setup (one time, ~5 minutes)

Paste each block into **your own** Terminal, in order.

**a. SSH config** — appended to `~/.ssh/config` (created if missing):

```bash
mkdir -p ~/.ssh ~/bin && chmod 700 ~/.ssh
cat >> ~/.ssh/config <<'EOF'

Host pmacs
    HostName consign.pmacs.upenn.edu
    User <pennkey>
    PubkeyAuthentication no
    PreferredAuthentications password
    NumberOfPasswordPrompts 1
    StrictHostKeyChecking accept-new
    ControlMaster auto
    ControlPath ~/.ssh/cm-pmacs
    ControlPersist 3d
    ServerAliveInterval 60
    ServerAliveCountMax 3

Host mercury
    HostName mercury.pmacs.upenn.edu
    User <pennkey>
    PubkeyAuthentication no
    PreferredAuthentications password
    NumberOfPasswordPrompts 1
    ControlMaster auto
    ControlPath ~/.ssh/cm-mercury
    ControlPersist 3d
EOF
chmod 600 ~/.ssh/config
```

Edit the two `<pennkey>` lines. `mercury` is only for file transfer (`rsync`/`scp` of code or small results); it has no `bsub`.

**b. Store the password in the Keychain** — this prompts you; nothing is echoed and nothing is written to disk in the clear:

```bash
security add-generic-password -a "$USER" -s pmacs-password -U -w
```

(If you ever change your PMACS password, run the same line again.)

**c. The helper** — `~/bin/pmacs-connect`:

```bash
cat > ~/bin/pmacs-connect <<'EOF'
#!/bin/bash
# Open (or confirm) the SSH ControlMaster to PMACS using the password in the macOS Keychain
# (item "pmacs-password"). Prints exactly one word: MASTER_OK, GOT_IT, AUTH_FAILED, VPN_DOWN,
# TIMED_OUT, EOF_EARLY or NO_KEYCHAIN_ITEM. Never prints the password. Safe for an agent to run.
set -u
HOST=${PMACS_HOST:-pmacs}

if ssh -O check "$HOST" >/dev/null 2>&1; then echo MASTER_OK; exit 0; fi

# A dead socket makes ssh report "Permission denied" forever; clear it first.
ssh -O exit "$HOST" >/dev/null 2>&1
sock=$(ssh -G "$HOST" | awk '$1=="controlpath"{print $2}')
[ -n "${sock:-}" ] && rm -f "$sock"
pkill -f "expect.*pmacs-connect" 2>/dev/null

PW=$(security find-generic-password -a "$USER" -s pmacs-password -w 2>/dev/null) || { echo NO_KEYCHAIN_ITEM; exit 46; }
export PW HOST

expect <<'EXP'
set timeout 45
log_user 0
spawn ssh -T -o ControlMaster=yes -o ControlPersist=yes $env(HOST) "echo MASTER_ESTABLISHED"
expect {
    -nocase -re {password[: ]*$}      { send -- "$env(PW)\r"; exp_continue }
    "MASTER_ESTABLISHED"              { puts "GOT_IT";      exit 0 }
    -nocase "denied"                  { puts "AUTH_FAILED"; exit 44 }
    -re {timed out|No route|refused}  { puts "VPN_DOWN";    exit 42 }
    timeout                           { puts "TIMED_OUT";   exit 43 }
    eof                               { puts "EOF_EARLY";   exit 45 }
}
EXP
rc=$?
unset PW
exit $rc
EOF
chmod 700 ~/bin/pmacs-connect
```

**d. Test it** (VPN on if you are off campus):

```bash
~/bin/pmacs-connect      # → GOT_IT   (first time; may take ~10 s)
~/bin/pmacs-connect      # → MASTER_OK
ssh pmacs 'hostname'     # → hpclogin1, no password prompt
```

`expect` ships with macOS. If the first run pops a Keychain dialog, click **Always Allow** so the agent never sees one.

## 2. Windows setup (one time, ~10 minutes)

Windows' built-in OpenSSH cannot multiplex connections (no `ControlMaster`), so the shared-connection trick does not work from PowerShell or Git Bash. Use **WSL2**: Claude Code, `ssh`, and the helper all live inside the Linux side; only the password store is Windows-native (DPAPI — encrypted with your Windows login, readable only by your account on this machine).

**a. WSL2 + tools** — in an *Administrator* PowerShell, once:

```powershell
wsl --install -d Ubuntu     # reboot if asked, then open "Ubuntu" from the Start menu
```

Then, inside the Ubuntu terminal:

```bash
sudo apt-get update && sudo apt-get install -y expect openssh-client
curl -fsSL https://claude.ai/install.sh | bash      # Claude Code, inside WSL
```

**b. Store the password (DPAPI)** — in a normal **PowerShell** window (not Ubuntu). It prompts; nothing is echoed; the file it writes is ciphertext bound to your Windows account:

```powershell
Read-Host -AsSecureString "PMACS password" | ConvertFrom-SecureString | Set-Content "$env:USERPROFILE\.pmacs-cred"
```

(Re-run when your PMACS password changes.)

**c. SSH config** — back in **Ubuntu**:

```bash
mkdir -p ~/.ssh ~/bin && chmod 700 ~/.ssh
cat >> ~/.ssh/config <<'EOF'

Host pmacs
    HostName consign.pmacs.upenn.edu
    User <pennkey>
    PubkeyAuthentication no
    PreferredAuthentications password
    NumberOfPasswordPrompts 1
    StrictHostKeyChecking accept-new
    ControlMaster auto
    ControlPath ~/.ssh/cm-pmacs
    ControlPersist 3d
    ServerAliveInterval 60
    ServerAliveCountMax 3

Host mercury
    HostName mercury.pmacs.upenn.edu
    User <pennkey>
    PubkeyAuthentication no
    PreferredAuthentications password
    NumberOfPasswordPrompts 1
    ControlMaster auto
    ControlPath ~/.ssh/cm-mercury
    ControlPersist 3d
EOF
chmod 600 ~/.ssh/config
```

Edit the two `<pennkey>` lines.

**d. The helper** — `~/bin/pmacs-connect` (Ubuntu). Identical to the macOS one except for the line that fetches the password, which asks Windows to decrypt the DPAPI file:

```bash
cat > ~/bin/pmacs-connect <<'EOF'
#!/bin/bash
# Open (or confirm) the SSH ControlMaster to PMACS using the DPAPI-encrypted password in
# %USERPROFILE%\.pmacs-cred (written by ConvertFrom-SecureString). Prints exactly one word:
# MASTER_OK, GOT_IT, AUTH_FAILED, VPN_DOWN, TIMED_OUT, EOF_EARLY or NO_CREDENTIAL.
# Never prints the password. Safe for an agent to run.
set -u
HOST=${PMACS_HOST:-pmacs}

if ssh -O check "$HOST" >/dev/null 2>&1; then echo MASTER_OK; exit 0; fi

ssh -O exit "$HOST" >/dev/null 2>&1
sock=$(ssh -G "$HOST" | awk '$1=="controlpath"{print $2}')
[ -n "${sock:-}" ] && rm -f "$sock"
pkill -f "expect.*pmacs-connect" 2>/dev/null

PW=$(powershell.exe -NoProfile -NonInteractive -Command \
  '$s = Get-Content "$env:USERPROFILE\.pmacs-cred" | ConvertTo-SecureString;
   [Runtime.InteropServices.Marshal]::PtrToStringAuto([Runtime.InteropServices.Marshal]::SecureStringToBSTR($s))' \
  2>/dev/null | tr -d '\r')
[ -n "${PW:-}" ] || { echo NO_CREDENTIAL; exit 46; }
export PW HOST

expect <<'EXP'
set timeout 45
log_user 0
spawn ssh -T -o ControlMaster=yes -o ControlPersist=yes $env(HOST) "echo MASTER_ESTABLISHED"
expect {
    -nocase -re {password[: ]*$}      { send -- "$env(PW)\r"; exp_continue }
    "MASTER_ESTABLISHED"              { puts "GOT_IT";      exit 0 }
    -nocase "denied"                  { puts "AUTH_FAILED"; exit 44 }
    -re {timed out|No route|refused}  { puts "VPN_DOWN";    exit 42 }
    timeout                           { puts "TIMED_OUT";   exit 43 }
    eof                               { puts "EOF_EARLY";   exit 45 }
}
EXP
rc=$?
unset PW
exit $rc
EOF
chmod 700 ~/bin/pmacs-connect
```

**e. Test it** (VPN on if you are off campus):

```bash
~/bin/pmacs-connect      # → GOT_IT
~/bin/pmacs-connect      # → MASTER_OK
ssh pmacs 'hostname'     # → hpclogin1
```

Run Claude Code from the Ubuntu terminal (`cd` to your project, then `claude`), not from PowerShell, so it uses WSL's `ssh`.

## 3. Guard rails for Claude Code (do this)

Put this in `~/.claude/settings.json` (or the project's `.claude/settings.json`). It lets Claude run the helper but forbids it from touching the credential store or any credential file directly, and makes it pause before anything destructive on the cluster:

```json
{
  "permissions": {
    "deny": [
      "Read(./.env)",
      "Read(./**/.env)",
      "Read(~/.ssh/**)",
      "Read(~/.netrc)",
      "Read(~/.pmacs-cred)",
      "Bash(security find-generic-password*)",
      "Bash(security *pmacs*)",
      "Bash(powershell.exe *pmacs-cred*)",
      "Bash(powershell.exe *SecureString*)",
      "Bash(cat *.env*)",
      "Bash(cat *~/.ssh/*)",
      "Bash(cat *pmacs-cred*)",
      "Bash(sshpass*)",
      "Bash(expect*)"
    ],
    "ask": [
      "Bash(ssh pmacs *bkill*)",
      "Bash(ssh pmacs *rm -r*)",
      "Bash(ssh pmacs *git push*)",
      "Bash(scp *)",
      "Bash(rsync *)"
    ]
  }
}
```

`Bash(expect*)` blocks Claude from writing its own password-typing script; the helper's internal `expect` is a child process and is unaffected.

## 4. The prompt to paste into Claude Code

Copy the block below into the first message of a conversation, or save it as `CLAUDE.md` in the project repo so every conversation gets it. Replace the three `<...>` placeholders. Everything else is deliberate — including the parts that tell the agent what **not** to do.

````markdown
# PMACS (Penn Medicine HPC) — how you reach the cluster from this laptop

## Who I am
- PennKey / cluster username: <pennkey>
- Project ID: <project-id>
- Project directory on the cluster: /project/hipaa_ycheng11lab/<project-id>/<pennkey>/

## The access model (read this before running anything remote)
- All cluster commands go through ONE shared SSH connection (an ssh ControlMaster
  for the host alias `pmacs`). Use it exactly like this, one command at a time,
  non-interactive:
      ssh -o ConnectTimeout=20 pmacs '<command>'
- Before the first remote command in a session, and after any remote command that
  fails with "Permission denied", "Broken pipe", "Connection closed", or
  "Operation timed out", run the helper:
      ~/bin/pmacs-connect
  It prints one word. Act on it:
      MASTER_OK / GOT_IT   -> connection is up; continue.
      VPN_DOWN / TIMED_OUT -> STOP. Tell me: "PMACS is unreachable — is the VPN
                              connected?" and wait. Do not retry on your own.
      AUTH_FAILED          -> STOP. Do not run the helper again (repeated failed
                              logins rate-limit my account). Tell me the stored
                              password was refused and wait.
      NO_KEYCHAIN_ITEM / NO_CREDENTIAL -> STOP. Tell me the credential store is
                              empty and wait.
- The helper is the ONLY way you open a connection. Never open an interactive ssh
  session, never run `ssh pmacs` without a command, never pass -t, never write
  your own expect/sshpass wrapper, never supply a password yourself.

## Secrets — hard rules
- You never need my password, and I will never give it to you. Never ask for it.
- Never run `security find-generic-password`, never read `~/.pmacs-cred`, never
  call powershell to decrypt anything. The helper does that; you do not.
- Never read, cat, grep, tail, or open: any .env file, ~/.ssh/*, ~/.netrc,
  keychain output, VPN config, or anything named *secret*, *token*, *credential*.
- If a secret ever appears in command output, do not repeat it, do not save it,
  and tell me it was exposed so I can rotate it.
- Never write a credential into any file: not CLAUDE.md, not your memory or notes,
  not a script, not a commit, not a comment.
- The only things you should ask me for are: my PennKey, the project ID, and which
  dataset / script to work on. Ask for nothing else about my account.

## Where things live
- Laptop repo (edit here):        ./  (this directory)
- Cluster clone (run here):       /project/hipaa_ycheng11lab/<project-id>/<pennkey>/<repo>/
- Data, intermediates, job logs:  under the cluster clone or a sibling data/ folder —
  never in git, never copied to the laptop.
- Code travels ONLY via git: commit and push from the laptop, `git pull` on the
  cluster. Do not scp/rsync code or data in either direction unless I ask.
- Cluster home (~) is small; do not install or write anything sizeable there.
- /tmp on the head node is NOT visible to compute nodes; never stage files there.
- HIPAA: nothing patient-level leaves the cluster, and do not paste raw data rows
  into this conversation. Summaries, counts, and metrics are fine.

## Compute — LSF, never the head node
- The head node (consign) is for submitting jobs, git, and reading small files.
  Never run python/R, a pipeline, or anything that loads data on it. Our venvs'
  numpy will not even import there (old GLIBC) — that is a feature, not a bug.
- Submit everything with bsub. Template:
      ssh pmacs 'cd /project/hipaa_ycheng11lab/<project-id>/<pennkey>/<repo> && \
        bsub -q rhel9 -n 8 -R "rusage[mem=16000]" -W 24:00 \
             -J <jobname> -o logs/<jobname>/o.out -e logs/<jobname>/o.err \
             "source <path-to-venv>/bin/activate && python -u <script>.py <args>"'
  Adjust -n / mem / -W to the job; mkdir the log dir first; rm the old log dir
  before resubmitting under the same name so stale output cannot be mistaken
  for new output.
- Check on work with: bjobs -w | bjobs -l <id> | bpeek <id> (live output; the
  -o file is only written at exit) | bhist -l <id> (finished jobs).
- Ask me before: bkill, rm -r, git push from the cluster, or anything that
  overwrites results.
- Poll patiently: a job that has not finished is not a job that failed. Check
  bjobs no more than every few minutes, and read the log tail before diagnosing.

## Git on the cluster
- Results produced on the cluster may be committed FROM the cluster; code is
  committed from the laptop. Because both sides commit, always
  `git pull --rebase origin main` before pushing from either side, and after a
  `git pull` on the cluster, verify the file you changed actually has the change
  (grep for the new flag) before submitting a job that depends on it.

## Etiquette
- Keep everything under my project subfolder; do not touch other users' folders.
- Prefer small, checked steps over long unattended chains; report exact job IDs,
  paths, and log locations so I can verify.
````

## 5. What a good session looks like

```
you:     [paste the block above]  Check whether my job "align_run3" finished.
claude:  ~/bin/pmacs-connect        → MASTER_OK
         ssh pmacs 'bjobs -w'       → align_run3 RUN, 2h13m
         ssh pmacs 'bpeek 9871234 | tail -20'
         "Still running, at sample 41/60. Log is logs/align_run3/…"
```

and what a good recovery looks like (laptop woke from sleep, VPN reconnected):

```
claude:  ssh pmacs 'bjobs -w'       → mux_client_request_session: read from master failed: Broken pipe
         ~/bin/pmacs-connect        → GOT_IT
         ssh pmacs 'bjobs -w'       → align_run3 DONE
```

and what a good stop looks like:

```
claude:  ~/bin/pmacs-connect        → VPN_DOWN
         "PMACS is unreachable — is the VPN connected?"
you:     [reconnect VPN]  ok
claude:  ~/bin/pmacs-connect        → GOT_IT
```

If Claude instead asks for your password, runs `security find-generic-password`, or writes its own `expect` script — stop it and re-paste the block. Those are exactly the behaviours the prompt and the deny-list forbid.

## Troubleshooting

* **`AUTH_FAILED` from the helper:** the stored password is wrong or expired. Re-run the store step (1b or 2b). Do **not** keep retrying — a few bad logins rate-limit the account for 10–15 minutes.
* **`VPN_DOWN` / `connect: Operation timed out`:** VPN. Not an auth problem.
* **`Permission denied` on `ssh pmacs …` without running the helper:** stale socket after a VPN drop. The helper's first job is to remove it; just run it.
* **`NO_KEYCHAIN_ITEM` (mac):** step 1b was skipped, or was run as a different user. `security find-generic-password -a "$USER" -s pmacs-password` (no `-w`) should list the item.
* **`NO_CREDENTIAL` (Windows):** `%USERPROFILE%\.pmacs-cred` is missing, or `powershell.exe` is not on WSL's PATH (`which powershell.exe`; interop is on by default — if it's off, `sudo sh -c 'echo 1 > /proc/sys/fs/binfmt_misc/WSLInterop'`).
* **A Keychain dialog appears every time (mac):** click **Always Allow** once; if it keeps asking, the item was created by a different tool — delete it in Keychain Access and re-run 1b so `security` is on its access list.
* **`ImportError: numpy C-extensions failed` / `GLIBC_2.27 not found`:** someone ran Python on the head node. Submit it with `bsub`.
* **Job log is empty while the job runs:** normal — LSF writes `-o`/`-e` at exit. Use `bpeek <jobid>`.
* **A file written to `/tmp` "disappeared":** it is on a different node. Write under the project directory.
* **Helper hangs:** two masters/expects fighting over one socket. `pkill -f pmacs-connect; ssh -O exit pmacs; rm -f ~/.ssh/cm-pmacs`, then run it once.

See also: [Claude to PARCC](ClaudeToPARCC) for the SLURM/Betty equivalent, [Claude to Git](ClaudeToGit), [PMACS Usage](../Access/PMACS).
