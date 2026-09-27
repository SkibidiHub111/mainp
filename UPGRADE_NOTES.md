# Deep-VM / Termux upgrade

## Changes

- Added a native Termux installer that builds both `luau` and `luau-ast`.
- Added `LUAU_BIN` and `LUAU_AST_BIN` overrides and actionable missing-binary errors.
- Added `--deep` for larger trace, rerun, constant-decode, and CFG budgets.
- Lifted mixed-key VM tables instead of stopping with
  `storing a non-empty VM table into a register`.
- Lifted opaque VM functions through shared-function references instead of
  rejecting them as expression values.
- Disabled the unsafe CFG plateau cutoff by default; `DEVIRT_WALK_LIMIT` still
  provides a hard state bound.
- Added explicit partial-output reports for unresolved VM successor markers.
- Fixed `--no-devirt --debug` so it always writes the requested trace output.

## Verification

- JavaScript, Python, and shell syntax checks pass.
- `luau` and `luau-ast` build and start successfully.
- Bundled Luraph v15 regression sample lifts with 0 unlifted blocks and passes
  `luau-ast` validation.
- The current `kaitun_levi.lua` URL is detected as Luraph v15, produces 14
  offline Path2D model answers, and reaches its loadstring VM chunk. Its native
  environment anti-tamper branch can still require exact Roblox-side Path2D
  behavior; the tool reports partial output instead of claiming completeness.

Only analyze scripts you own or are authorized to inspect.
