# PrehistoricTux engine changes

The authoritative UHD engine modification is applied by:

    scripts/apply-uhd-engine-patch.py

The project previously stored a hand-written `.patch` file here. That patch
proved fragile against hunk metadata and produced `git apply: corrupt patch`
on the Garuda target machine, so the build no longer relies on it.

The patcher performs exact replacements against the pinned SuperTux 0.7.0
source tree and fails immediately if the expected upstream blocks do not
match. The build records the patcher's SHA-256 fingerprint beside the compiled
binary so a stale engine cannot be launched accidentally.
