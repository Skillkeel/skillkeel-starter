# Skillkeel Starter

Guard hooks and repo skills for [Claude Code](https://claude.com/claude-code). Free, MIT.

[![Listed on ClaudePluginHub](https://www.claudepluginhub.com/badge/skillkeel-skillkeel-starter)](https://www.claudepluginhub.com/plugins/skillkeel-skillkeel-starter?ref=badge)

Claude Code is fast. It will also run `rm -rf` in the wrong directory, force-push over a teammate's branch, or write an API key straight into `config.py` if nothing stops it. This plugin blocks the commands and writes listed below (it is a guard, not a sandbox; the tamper-cases corpus shows what it catches and what it does not), and adds eight small skills for the boring parts of repo work.

## Hooks

![guard-bash refusing rm -rf /, git push --force and find -exec rm -rf; secret-scan refusing an AWS key; git status allowed](docs/guard-bash.gif)

Every call in the recording is the real hook fed the JSON Claude Code sends. Still image: [docs/guard-bash.png](docs/guard-bash.png).


| Hook | What it does |
|---|---|
| `guard-bash` | Blocks destructive shell commands before they run: `rm -rf /`, `git push --force` without `--force-with-lease`, `git reset --hard`, `git clean -f`, `DROP DATABASE`, `terraform destroy`, `curl \| bash`, `dd` and `mkfs`, and since 0.1.4 git settings that run commands (`core.fsmonitor`, hooks paths, shell aliases) plus writes into `.git/`. Claude sees the reason and asks you instead. |
| `secret-scan` | Blocks a file write that contains an AWS, OpenAI, Anthropic, GitHub or Slack key, a private key, a JWT, or a hard-coded password. |
| `session-start` | Gives Claude two lines of context at session start: the current git state and the list of skills. Nothing is printed to you; ask Claude what Skillkeel says and it answers from that brief. |

## Skills

| Skill | What it does |
|---|---|
| `commit-message` | Writes a Conventional Commits message from the staged diff. It reads the diff; it does not guess. |
| `pr-description` | Writes a PR body from the branch diff, with a test plan that uses commands that exist in the repo, and a risk section. |
| `claude-md-init` | Generates a short CLAUDE.md. Every command in it was checked against the repo first. |
| `changelog` | Adds Keep a Changelog entries from git history since the last tag. |
| `readme-refresh` | Checks every command and link in your README against the repo and fixes the ones that are wrong. |
| `dependency-audit` | Runs the audit tool for your ecosystem, sorts fixes into safe and needs-approval, and never uses `--force`. |
| `secret-audit` | Finds credentials in git history, masks them, and gives you a plan that starts with rotating the key. |
| `test-gap-finder` | Lists untested modules ranked by recent churn and proposes specific test cases. |

## How it is tested

The hooks have 64 unit tests in `tests/test-hooks.sh`. Each skill has a folder under `evals/` with a fixture repo, a list of expected results, and the unedited transcript of a real Claude Code run. The evals are rerun on every Claude Code release; the pass counts per version are in [docs/compat.md](docs/compat.md), and the run records and transcripts sit next to each case. You can read them before you install anything.

[docs/compat.md](docs/compat.md) lists every Claude Code version the evals ran on, with the pass counts, generated from the results in this repo. Since 2026-09-18 the runner also has a trigger mode (`bash evals/run.sh --trigger`): the same eight cases with a request that never names the skill, such as "Commit the staged changes.", so the table shows whether the descriptions fire on a plain request and not only whether the invocation path works (first run: 8/8 on 2.1.276). Since 0.1.3 the eval runner also writes a run record per case (`evals/<skill>/record-<date>.json`: exit code, every tool call, skill invocations, grader verdicts that need no model) and `evals/cluster.py` groups failed cases by their first mechanical mismatch, so a runner or grader fault shows up as one bucket instead of eight transcript reads. The skill texts call four external CLIs (gitleaks, trufflehog, pip-audit, gh); `tests/test-cli-verbs.py` checks every subcommand and flag they name against `tests/cli-verbs.json`, a snapshot read from the latest release of each CLI, so a renamed subcommand fails the test before it fails for you.

External test set: u/Far_Business4773 runs 52 evasion cases against a guard of this shape in [lumis-skills/examples/tamper_cases.py](https://github.com/momonanq/lumis-skills/blob/main/examples/tamper_cases.py) (MIT). Cases 41 to 52 came out of the r/ClaudeCode thread with this project; case 42 (`find -exec rm -rf`) is the one fixed in 0.1.1. That file targets a guard with protected paths, which guard-bash does not have, so it is a reference, not part of this test suite. The shared corpus [skillkeel/tamper-cases](https://github.com/skillkeel/tamper-cases) carries those 52 cases plus the destructive and git-config families from this suite (105 cases) with a runner for any hook; its RESULTS.md has the numbers for guard-bash 0.1.0 and 0.1.5.

This plugin does not overlap with the `superpowers` plugin. That one covers process (planning, TDD, debugging). This one covers guardrails and repo chores.

## Install

```
/plugin marketplace add skillkeel/skillkeel-starter
/plugin install skillkeel-starter@skillkeel
```

Or clone the repo and start Claude Code with `claude --plugin-dir ./skillkeel-starter`.

To try it for one session without installing anything, load the release archive by URL (Claude Code fetches it at startup and forgets it when the session ends):

```
claude --plugin-url https://github.com/skillkeel/skillkeel-starter/archive/refs/tags/v0.1.7.zip
```

The eight skills alone, without the three hooks, also install through `npx skills add skillkeel/skillkeel-starter -g -a claude-code`; that route copies `SKILL.md` folders and never a plugin's `hooks/hooks.json`, so guard-bash and secret-scan are not part of it.

## Check it is on

Nothing prints after the install. Two ways to see the plugin working:

In Claude Code, ask: what does Skillkeel say in this session? The answer comes from the session brief: "Skillkeel Starter active: guard-bash (blocks destructive shell), secret-scan (blocks credentials in writes)", followed by the eight skill names.

From a clone, feed the hook one command by hand:

```
echo '{"tool_input":{"command":"git push --force origin main"}}' | bash hooks/guard-bash
```

It prints `skillkeel guard-bash: blocked (git push --force (use --force-with-lease)). Command: git push --force origin main` and exits 2. The same line with `--force-with-lease` exits 0 and prints nothing.

## Turning a guard off for one session

```
SKILLKEEL_ALLOW_DANGEROUS=1 claude   # guard-bash off
SKILLKEEL_ALLOW_SECRETS=1 claude     # secret-scan off
```

## Run the tests

```
bash tests/test-hooks.sh            # 64 hook cases
python3 tests/test-cli-verbs.py     # skill texts vs the CLI snapshot
python3 tests/test-evals-record.py  # eval record and cluster tools
```

## Paid version

Skillkeel Kit (€49 plus VAT where it applies, added at checkout) adds a ten-chapter playbook, 24 more skills in six packs, five more guard hooks, five subagents, three checklists, and CLAUDE.md templates for eight stacks: https://skillkeel.gumroad.com/l/skillkeel-kit
