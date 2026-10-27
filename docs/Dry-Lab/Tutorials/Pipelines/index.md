---
layout: default
title: Pipelines
parent: Tutorials
grand_parent: Dry Lab
has_children: true
has_toc: false
nav_order: 30
---

# {{page.title}}

The content here is undergoing transition as we adjust to LLM-assisted development.

In general, the typical cycle of analysis is as such:

1) Processing - Take the data and perform some transformation or calculation on it.

2) Check Assumptions for the Process - Analyze the result of the processing in terms of the goal of the processing: Does the output indicate that the process was done "correctly" for some specific definition of "correct".

* One specific example is spatial transcriptomic segmentation. Do the resulting cell calls resemble proper cells with a single nucleus and a spherical or neuronal shape?

* If the process "failed", either return to step (1) with parameters that address the underlying cause of failure if the failure could be procedural or continue forward without this process.

3) Calculate QC of the Processed Data - If the algorithm was correct, what does the result say about the data? Is there a threshold we want to reach? Does it match well with previous results?

* If the QC fails a threshold or is incongruous with previous results, report this fact and either continue analysis, omit the portion that failed or repeat (1) with an updated procedure to address this.

4) Compile the results of each step into a report for review.

5) With the review as context, adjust as necessary and as specified previously. Otherwise, proceed to the next analysis of the pipeline.
