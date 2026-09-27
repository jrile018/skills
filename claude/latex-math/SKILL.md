---
name: latex-math
description: Write math-heavy LaTeX documents, solution sets, proofs, and homework. Use when creating LaTeX, .tex files, or math assignments.
---

When writing LaTeX math documents:

1. Answers-only format — minimal prose, maximum math
2. Use \implies chains and symbolic notation for proofs, not paragraph explanations
3. Wrap all math in proper environments: align*, cases, bmatrix, equation*
4. For DSP topics (Z-transforms, DTFT, DFT, convolution, pole-zero):
   - Always show intermediate algebraic steps
   - Include ROC for Z-transforms
   - Draw pole-zero plots when relevant
5. Use \boxed{} for final answers
6. Include MATLAB code blocks when computational verification helps
7. Standard preamble unless told otherwise:
   \documentclass[11pt]{article}
   \usepackage{amsmath,amssymb,mathtools,geometry,listings,graphicx}
   \geometry{margin=1in}

For compiled PDF output, always produce both the .tex source and compiled PDF.
