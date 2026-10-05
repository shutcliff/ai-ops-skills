# How a process agent is built, so an operator can run it

A **process agent** runs a recurring business process: it fetches from a few systems, writes to one or two, and repeats on a schedule or on demand. Read this when judging an Operability criterion. The pass and fail lines live in `criteria.md`; this file shows the build shape behind them.

## 1. Every automatic behaviour is a module with a switch

One setting per behaviour, not per agent: a daily fill, a weekly summary and a webhook listener are three switches, so turning off the noisy one leaves the useful one running. The switch is an environment variable or config key read once at the top of the runner, never a comment, a renamed file or a commented-out scheduler line.

```sh
: "${RECON_DAILY_FILL:=off}"          # default off, documented in SETUP
if [ "$RECON_DAILY_FILL" != "on" ]; then
  echo "daily fill is off (RECON_DAILY_FILL=$RECON_DAILY_FILL); nothing to do"
  exit 0                               # no fetch, no write, no state change
fi
```

## 2. One leg per source, and each leg can fail alone

Split the run by source: one leg per system it reads. Each leg reports its own outcome, and a failure in one leg does not silently truncate the others. This is what makes a partial day readable afterwards and re-runnable in isolation.

## 3. Code owns every number, Claude orchestrates

A mapping that lives in a config file is named in that file, not described in prose in two places. A prompt that tells Claude to "cross-check whatever mapping you use" hands a decision to the model.

## 4. One write helper

Every write goes through one function. An inline write done "just this once" bypasses the check, the dry run and the trace at the same time. A dry run reaches the same decisions as a real run.

## 5. The done marker is never guessed

A run that finished half way must be safe to re-run, so write the done marker last, only when every leg reached a definite outcome. A missing marker costs one harmless re-run; a wrongly written one leaves the work half done forever.

## 6. One entry per run, outside git

The trace lives in the operator's own state directory (`$XDG_STATE_HOME` or `~/.local/state/<agent>/`); nothing about a run is committed. Record what was written as addresses and counts, not the values themselves when they are financial or personal. A raw model transcript is not a trace: it loses the difference between a quiet day and a broken query.

## 7. A probe writes down what only the live systems know

Some facts exist only at run time: the number format the sheet renders, whether the service account really has editor access, whether a card returns rows today. The probe writes into the same state directory, one named check per line: pass or fail, and the value it read back. It runs before the work does, and the runbook makes it the first question asked of any failed run. It cannot say whether a value is the right one; proof cases do that.
