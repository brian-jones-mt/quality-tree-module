# Module 5: Operationalizing the Tree

![Module 5 Overview](module-5-mindmap.svg)

---

## Operationalizing the Tree

### *Integration with CI/CD and Product Roadmaps*

**Duration:** 1.5 hours

**Format:** Theory + Implementation Planning

---

## Learning Objectives

By the end of this module, you will be able to:

- **Connect** quality tree leaves to measurable metrics in your monitoring systems (Datadog, Prometheus, etc.)
- **Define** "done" criteria based on quality attribute thresholds, not just feature completion
- **Implement** quality gates in your CI/CD pipeline aligned with ASRs
- **Create** alerts and dashboards that reflect architectural priorities
- **Integrate** your quality tree into product roadmap planning
- **Measure** whether your architecture actually delivers on its promises
- **Use** quality metrics to make data-driven architectural evolution decisions

---

## Why You Need to Know This

- A quality tree locked in a design doc is useless.
- A quality tree without metrics is a wish list.

As a lead developer responsible for delivery, you will face:

- **"Are we actually meeting our SLAs?"**
    - Without monitoring, you don't know
- **"The code is done, why can't we ship?"**
    - because you haven't defined "done"
- **"Performance regressed"**
    - because there's no automated gate preventing it
- **"Our architecture is degrading"**
    - because quality metrics aren't tracked over time
- **"What should the product team prioritize next?"**
    - roadmaps without architectural context make bad choices

**This module closes the loop from design intent to operational reality.**

By operationalizing your quality tree
— connecting it to
    - CI/CD pipelines,
    - alerts,
    - roadmap planning
  
You transform it from a theoretical exercise into an active guard against architectural decay. You'll know in real-time whether your system is living up to its architectural promises.

---

## From "Leaves" to "Logs"

### *Connecting Scenarios to Real-World Telemetry*

A Quality Attribute Scenario (QAS) is a requirement. To operationalize it, you must map it to a **Metric Name**.

### The Mapping Process:

1. **Identify the Indicator:** (e.g., Latency, Error Rate, CPU Saturation).
2. **Locate the Source:** (e.g., Application logs, Prometheus metrics, AWS CloudWatch).
3. **Define the Measurement:** (e.g., "p95 of `http_request_duration_seconds` over a 5-minute window").

Example:

- **Scenario:** "Under normal load, the payment API must respond in < 200ms."
- **Metric:** `avg:trace.payment_gateway.request.duration{env:prod}.p95`

---

## Defining "Done" with Quality Gates

### *Architecture is not a "Side Quest"*

If a feature is "functionally complete" but fails its quality attribute threshold, it is **not done**.

**Quality Gates in the Definition of Done (DoD):**

- Unit tests pass (Functional)
- Integration tests pass (Functional)
- **Performance benchmark < X ms** (Architectural)
- **Security scan has 0 Criticals** (Architectural)
- **Documentation reflects changes** (Maintainability)

**The Rule:** If the gate is red, the release is blocked.

---

## Quality Gates in CI/CD

### *Automating the Guardrails*

You can't manually check every quality attribute on every PR. Automate the most critical ones (ASRs).

**Example Pipeline Stages:**

1. **Build & Lint:** Static analysis (Maintainability).
2. **Security Scan:** Snyk/Trivy (Security).
3. **Automated Load Test:** k6/JMeter (Scalability/Performance).
    - *Pass Condition:* "If p95 latency > 300ms, fail the build."
4. **Canary Deployment:** Compare metrics of new version vs. old.

**Tooling:** GitHub Actions, GitLab CI, Spinnaker (for automated rollbacks).

---

## Architectural Dashboards

### *Visualizing the Health of the Tree*

Don't bury quality metrics in a sea of 1,000 infra charts. Create a dedicated **Architectural Health Dashboard**.

**What to include:**

- Top-level "Traffic Lights" for each major Quality Attribute.
- Trends over time (Are we getting slower? Are we getting more unstable?).
- Comparison against the thresholds defined in your Quality Tree.

**Stakeholder View:** A dashboard that says "We are 99.9% Available" is more powerful than a 50-page PDF report.

---

## Integrating with Product Roadmaps

### *Making Quality a First-Class Citizen*

Quality Trees provide the **data** needed to negotiate with Product Owners.

- **Scenario:** Product wants "Feature X," but your Quality Tree shows that "Latency" is already at its limit.
- **The Conversation:** "Adding Feature X will push our p95 latency to 400ms, violating our agreed architectural goal of 300ms. We should spend the next sprint on 'Performance Optimization' to create the 'headroom' for Feature X."
- **Outcome:** Quality is no longer "Technical Debt" — it's "Capacity Management."

---

## Measuring Architectural Success

### *Closing the Feedback Loop*

The Quality Tree is a hypothesis: *"If we build it this way, we will achieve this result."*

**Quarterly Review:**

1. **Look at the Metrics:** Did we meet our thresholds?
2. **Analyze Deviations:** If we failed, was the architecture wrong, or was the requirement unrealistic?
3. **Update the Tree:** Refine scenarios based on what you've learned from production.

**Success is when your production metrics match your Quality Tree's leaves.**

---

## Module 5 Recap: The Living Tree

- **Metrics** turn wishes into reality.
- **Quality Gates** prevent architectural decay.
- **Dashboards** make architecture visible to everyone.
- **Roadmap Integration** ensures sustainable development.
- **Feedback Loops** allow the architecture to evolve with data.

Your Quality Tree is now a living part of your engineering culture.


