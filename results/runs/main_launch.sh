#!/bin/bash
# Confirmatory Phase 1 runs, as pre-registered in results/PREREGISTRATION.md.
cd "$(dirname "$0")/../.."
python3 -m acs.run --name main_dev --models claude-fable-5-1,claude-opus-5-5,grok-4.7,claude-haiku-5-5 \
  --scenarios all --conditions C0,C1,C2,C3 --repeats 1 --repeat-offset 1 --workers 6 \
  --monitor-model claude-sonnet-5-5 --require-claude-account author@example.invalid
python3 -m acs.run --name main_heldout --scenario-dir data/heldout --models claude-fable-5-1,claude-opus-5-5,grok-4.7,claude-haiku-5-5 \
  --scenarios all --conditions C0,C1,C2,C3 --repeats 2 --repeat-offset 0 --workers 6 \
  --monitor-model claude-sonnet-5-5 --require-claude-account author@example.invalid
