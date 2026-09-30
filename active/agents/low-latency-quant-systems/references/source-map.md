# Source map

## How to use this ledger

Use this file when a recommendation needs provenance, when a source may have changed, or when a maintainer is deciding whether a rule belongs in the skill. The dated research snapshot is in [`research/low-latency-quant-systems-2026-09-26`](../../../research/low-latency-quant-systems-2026-09-26/). Follow its dossier links to the original institutional, vendor, standards, or research source.

Do not turn a course example into a current deployment fact. Recheck protocol revisions, operating-system and framework documentation, compiler behavior, and processor guidance against the user's installed versions and target hardware.

## Evidence-to-module map

| Skill module | Main evidence families | What the evidence supports | Important limit |
|---|---|---|---|
| `measurement-contract.md` | ETH Fast Numerical Code; UT Austin LAFF-On PfHP; Stanford CS149; CMU 15-418/618; Berkeley CS267; Stanford CS244 | Reproducible baselines, hypothesis-driven tuning, scaling and capacity experiments, production-shaped evaluation | A course method does not prove a particular system is faster |
| `trading-correctness.md` | Chicago FINM 32700/37602; Oxford Market Microstructure; Stanford MS&E 448; NYU ULL; Cartea–Jaimungal; Kearns–Nevmyvaka; Nasdaq ITCH/OUCH | Event, order, fill, inventory, replay, point-in-time, and venue-protocol invariants | Course and research models cover bounded settings; venue specifications must be pinned by revision |
| `cpu-memory-compiler.md` | ETH; Cornell CS6120/6210; uops.info; LLVM MCA; Intel, AMD, and Arm manuals | Code-generation inspection, cache/data-layout reasoning, SIMD, instruction-resource hypotheses, target dispatch | Static models and instruction tables omit important application and system effects |
| `numerical-kernels.md` | UT Austin LAFF/ALAFF; Cornell CS6210; KIT NLA4HPC; Berkeley CS267; EPFL MATH-454; Illinois ECE408/CS598PA | Mathematical contracts, stable algorithms, arithmetic intensity, blocking, CPU/GPU decomposition | Performance depends on shapes, conditioning, libraries, transfer, and target hardware |
| `concurrency-realtime.md` | Stanford CS149; CMU 15-418/618; Illinois CS420; Stanford CS349F | Ownership, work partitioning, synchronization, false sharing, queueing, affinity, load and saturation | No universal lock-free, queue-count, or core-placement rule follows |
| `networking-time.md` | Stanford CS244/CS349F; Linux networking, timestamping, NAPI and scaling docs; DPDK; NYU ULL | Experimental network methods, timestamp boundaries, queue/core placement, poll-mode architecture and costs | Kernel, driver, NIC, DPDK, and API details are version-specific |
| `system-architecture.md` | NYU ULL; Stanford CS349F; Illinois accelerator courses; EPFL; DPDK; vendor guidance | CPU/GPU/FPGA and kernel/user-space tradeoffs, data movement, critical-path budgeting, operational costs | These are candidate-generation heuristics; deployment measurements decide |

## Dossier catalog

### CPU, compiler, and numerical coursework

- [`eth-fast-numerical-code.md`](../../../research/low-latency-quant-systems-2026-09-26/courses/eth-fast-numerical-code.md)
- [`ut-austin-laff-performance.md`](../../../research/low-latency-quant-systems-2026-09-26/courses/ut-austin-laff-performance.md)
- [`ut-austin-alaff.md`](../../../research/low-latency-quant-systems-2026-09-26/courses/ut-austin-alaff.md)
- [`cornell-cs6210.md`](../../../research/low-latency-quant-systems-2026-09-26/courses/cornell-cs6210.md)
- [`cornell-cs6120.md`](../../../research/low-latency-quant-systems-2026-09-26/courses/cornell-cs6120.md)
- [`kit-nla4hpc.md`](../../../research/low-latency-quant-systems-2026-09-26/courses/kit-nla4hpc.md)

### Parallel, accelerator, and systems coursework

- [`stanford-cs149.md`](../../../research/low-latency-quant-systems-2026-09-26/courses/stanford-cs149.md)
- [`cmu-15418.md`](../../../research/low-latency-quant-systems-2026-09-26/courses/cmu-15418.md)
- [`berkeley-cs267.md`](../../../research/low-latency-quant-systems-2026-09-26/courses/berkeley-cs267.md)
- [`illinois-cs420.md`](../../../research/low-latency-quant-systems-2026-09-26/courses/illinois-cs420.md)
- [`illinois-ece408.md`](../../../research/low-latency-quant-systems-2026-09-26/courses/illinois-ece408.md)
- [`illinois-cs598pa.md`](../../../research/low-latency-quant-systems-2026-09-26/courses/illinois-cs598pa.md)
- [`epfl-math454.md`](../../../research/low-latency-quant-systems-2026-09-26/courses/epfl-math454.md)

### Networking and trading-system coursework

- [`stanford-cs244.md`](../../../research/low-latency-quant-systems-2026-09-26/courses/stanford-cs244.md)
- [`stanford-cs349f.md`](../../../research/low-latency-quant-systems-2026-09-26/courses/stanford-cs349f.md)
- [`chicago-finm32700.md`](../../../research/low-latency-quant-systems-2026-09-26/courses/chicago-finm32700.md)
- [`chicago-finm37602.md`](../../../research/low-latency-quant-systems-2026-09-26/courses/chicago-finm37602.md)
- [`oxford-market-microstructure.md`](../../../research/low-latency-quant-systems-2026-09-26/courses/oxford-market-microstructure.md)
- [`stanford-msande448.md`](../../../research/low-latency-quant-systems-2026-09-26/courses/stanford-msande448.md)
- [`nyu-ull-architectures.md`](../../../research/low-latency-quant-systems-2026-09-26/courses/nyu-ull-architectures.md)

### Implementation and protocol references

- [`uops-info.md`](../../../research/low-latency-quant-systems-2026-09-26/implementation/uops-info.md)
- [`llvm-mca.md`](../../../research/low-latency-quant-systems-2026-09-26/implementation/llvm-mca.md)
- [`intel-optimization.md`](../../../research/low-latency-quant-systems-2026-09-26/implementation/intel-optimization.md)
- [`amd-optimization.md`](../../../research/low-latency-quant-systems-2026-09-26/implementation/amd-optimization.md)
- [`arm-simd.md`](../../../research/low-latency-quant-systems-2026-09-26/implementation/arm-simd.md)
- [`linux-networking.md`](../../../research/low-latency-quant-systems-2026-09-26/implementation/linux-networking.md)
- [`dpdk.md`](../../../research/low-latency-quant-systems-2026-09-26/implementation/dpdk.md)
- [`nasdaq-itch.md`](../../../research/low-latency-quant-systems-2026-09-26/implementation/nasdaq-itch.md)
- [`nasdaq-ouch.md`](../../../research/low-latency-quant-systems-2026-09-26/implementation/nasdaq-ouch.md)
- [`cartea-jaimungal.md`](../../../research/low-latency-quant-systems-2026-09-26/implementation/cartea-jaimungal.md)
- [`kearns-nevmyvaka.md`](../../../research/low-latency-quant-systems-2026-09-26/implementation/kearns-nevmyvaka.md)

## Provenance and reuse boundary

The skill paraphrases derived procedures; it does not redistribute course notes, proprietary manuals, or exchange specifications. Public accessibility is not an open-content license. Preserve links and attribution, respect the license stated by each source, and keep third-party wording out of the skill unless its license and quotation limit permit reuse.
