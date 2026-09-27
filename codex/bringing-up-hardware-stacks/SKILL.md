---
name: bringing-up-hardware-stacks
description: Use when connecting, diagnosing, or validating physical sensors, instruments, embedded devices, acquisition hardware, drivers, telemetry pipelines, or hardware-backed dashboards.
---

# Bringing Up Hardware Stacks

## Principle

Prove one boundary at a time from the physical device to the user-visible result. The first unproven boundary is the current problem; higher layers cannot compensate for it.

## Layered Bring-Up

| Layer | Evidence required |
|---|---|
| Safety and physical setup | Correct power, grounding, connectors, limits, and safe operating conditions |
| Host detection | Device, port, interface, or bus appears with the expected identity |
| Driver and runtime | Correct driver, permissions, architecture, and library load successfully |
| Raw acquisition | Minimal vendor tool or probe returns plausible raw values |
| Framing and parsing | Units, timestamps, channel mapping, endianness, and invalid-value handling are verified |
| Processing | Filters and transformations preserve known signals and declare latency |
| Service/API | Fresh data crosses the process boundary with health and error state |
| UI or consumer | The displayed value traces back to the same timestamped sample |
| Stability | Reconnect, timeout, stale-data, and sustained-run behavior are tested |

At each layer, capture the exact command or action, expected result, observed result, and conclusion. Stop climbing when a layer fails; isolate it with the smallest probe available.

## Diagnosis Rules

- Distinguish “not detected,” “detected but inaccessible,” “accessible but invalid,” and “valid but stale.”
- Compare against a known input or simulator before tuning filters.
- Preserve raw samples when possible so processing defects can be reproduced offline.
- Reject or label impossible sensor values; do not silently graph them.
- When multiple processes may own a port or device, identify the active process before restarting anything.
- Never bypass electrical, laser, RF, biomedical, or machinery safety limits for convenience.

## Output Contract

Report the first failing boundary, supporting evidence, the next minimal test, and the exact success condition. Once the full path works, provide a compact runbook for reconnecting it.

## Example

If a dashboard graph is flat, first confirm the host sees the device, then obtain changing raw samples, then compare API timestamps with the UI. Editing chart code before proving acquisition is not diagnosis.

## Common Mistakes

- Changing several layers before re-testing.
- Treating a connected cable as proof of detection.
- Filtering before validating raw units and timing.
- Restarting processes without identifying which instance owns the hardware.
