# Networking and time

## Purpose and loading boundary

Use this module for sockets, multicast, packet loss, kernel/NIC queues, IRQs, timestamping, PTP, busy polling, AF_XDP, DPDK, or network-path latency. Do not load it when the measured bottleneck is wholly inside a compute kernel.

## Map the path and clocks

Draw the receive and transmit path across NIC, driver, kernel or user-space stack, socket/queue, parser, application stages, and remote endpoint. Name the start/end timestamps, clock domains, synchronization method, resolution, conversion, and measurement overhead. Distinguish wire, hardware, driver, scheduler, system-call, application, and acknowledgment latency.

Record NIC/firmware/driver, link settings, kernel, queue counts, interrupt moderation, RSS/RPS/RFS/XPS, IRQ and process affinity, NUMA placement, socket options, batching, and topology. Test gaps, duplicates, reordering, reconnect, snapshots/recovery, and burst loss as part of correctness.

## Diagnose before bypassing

Measure queueing, interrupt/scheduling, copies, parsing, and application work separately where possible. Busy polling exchanges CPU and power for latency. Queue/core placement can reduce cache movement but depends on load and topology. Test tail latency and goodput across offered load rather than applying a universal queue-count rule.

Treat DPDK or another bypass as an architecture candidate only after the kernel path is characterized. For DPDK, define queue ownership, logical-core layout, NUMA and memory-pool placement, burst size, run-to-completion versus pipeline behavior, CPU reservation, and recovery/operability. Verify API concurrency assumptions against the installed version.

## Acceptance

Apply the parent acceptance gate. Additionally require identical protocol/application semantics and documented timestamp boundaries. Include packet loss, deadline misses, queue occupancy, CPU/power cost, and behavior near saturation. Do not infer network improvement from a local packet-loop microbenchmark alone.
