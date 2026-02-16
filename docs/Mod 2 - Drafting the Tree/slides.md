# Module 2: Drafting the Tree

---

## Drafting the Tree (Practical)

### *The Stimulus-Response Methodology*

**Duration:** 2.25 hours

**Format:** Theory + Hands-On Facilitation Lab

---

## Learning Objectives

By the end of this module, you will be able to:

- **Extract** concrete requirements from stakeholders using facilitated workshops
- **Apply** the Stimulus-Response formula to every requirement:
  - Source (Who/What triggers it?)
  - Stimulus (What happens?)
  - Response (The measurable outcome)
- **Translate** vague customer needs into actionable "leaves" on your quality tree
- **Facilitate** a requirements workshop without getting lost in abstract discussions
- **Distinguish** between a good requirement and a wish list

---

## Why You Need to Know This

Most projects fail not because the code is bad, but because **no one agreed on what success looks like**.

As a lead developer leading architecture discussions, you will encounter:

- **Stakeholders speaking in metaphors** ("The system should feel snappy")
- **Conflicting priorities** with no framework to resolve them
- **Post-launch disputes** because each team built for different success criteria
- **Inability to measure** whether your architecture actually solved the problem

**This module gives you the facilitation tools to lock down requirements BEFORE architecture is set in stone.**

The Stimulus-Response format forces concrete thinking and eliminates the 80% of heated debates that are really just miscommunication.

---

### The Stimulus-Response Format

To make a tree usable, every "Leaf" must follow this formula:

> **Source:** (Who/What triggers it?) + **Stimulus:** (What happens?) + **Response:** (The measurable outcome).

**Example Scenario:**

* **Bad:** "The checkout should be fast."
* **Good:** "Under a 500% spike in concurrent users (Stimulus), the checkout service must process transactions in  seconds (Response) with  data loss."

---

## Google's Four Golden Signals

### *The Pillars of Effective Monitoring*

**Goal:** Understand the fundamental metrics for system health and performance.

These four signals are a critical starting point for any monitoring strategy, helping to quantify what matters most about user-facing services.

---

## Deep Dive: The Golden Signals

-   **Latency:** The time it takes to serve a request. (e.g., *How long does it take to complete an action?*)
    -   *Good Latency:* Fast response times for users.
    -   *Bad Latency:* Slow loading, delays, frustrated users.

-   **Throughput (or Traffic):** How much demand is being placed on your system. (e.g., *How many requests per second are we handling?*)
    -   *Good Throughput:* System processing expected load efficiently.
    -   *Bad Throughput:* Requests queuing up, leading to backlogs.

-   **Errors:** The rate of requests that fail. (e.g., *How often does something go wrong?*)
    -   *Good Errors:* Low error rates, indicating reliability.
    -   *Bad Errors:* High rates of 5xx responses, impacting user experience.

-   **Saturation:** How "full" your service is. (e.g., *How much capacity are we using? Are we nearly overloaded?*)
    -   *Good Saturation:* Healthy resource utilization.
    -   *Bad Saturation:* Resources (CPU, memory, network) at or near capacity, predicting future issues.
    -   *Bad Saturation:* Resources are paid for, but nver used. 

---

## Discussion

*6 minute discussion, breakout rooms 1 question per group*

- Your application has a function with high latency. Its not preventing login, or first page load. 
  - Other than speeding up the processing, what else might work?
- Your application has an endpoint with a large number of 4xx responses.
  - In terms of your application, are these good or bad errors?
  - What should you do about these?
- How can your application tell the difference between *good* and *bad* throughput.
  - What can your application do about this?
- As an application development team, how do you normally use these signals.
- Saturation is how full your service is. You are designing a dashboard to report on saturation of a resource (CPU, memory). 
  - Describe how the element should look to generate the information a (senior manager / CTO / Client) needs. 



---

## Building a Quality Tree: The Process

### *A Structured Approach to Defining Architectural Quality*

**Goal:** Understand the systematic steps to construct a comprehensive quality tree.

Building a quality tree is not a one-time event, but an iterative process of discovery, refinement, and prioritization involving various stakeholders. It translates ambiguous quality requirements into concrete, measurable scenarios.

Here are the key phases:

1.  **Identify Primary Stakeholders:** Determine who cares most about the system's quality (users, operations, business, security).
2.  **Brainstorm Quality Attributes:** Start with high-level "-ilities" (e.g., Performance, Security, Usability, Maintainability).
3.  **Refine Attributes into Sub-Attributes:** Break down broad attributes into more specific aspects (e.g., Performance -> Latency, Throughput).
4.  **Draft Quality Attribute Scenarios (QAS):** Define concrete, measurable scenarios for each sub-attribute using the Stimulus-Response pattern.
5.  **Prioritize Scenarios:** Assess Business Value and Architectural Impact (covered in Module 3).
6.  **Review and Iterate:** Continuously validate the tree with stakeholders.

---

## Step-by-Step: Constructing a Quality Scenario

### *From Vague Intent to Measurable Detail*

**Goal:** Master the art of writing precise and actionable quality attribute scenarios.

Each leaf of your quality tree is a Quality Attribute Scenario (QAS) that answers:
*"When X happens, under Y conditions, Z must occur, and we measure it by W."*

Let's break down the Stimulus-Response pattern for a QAS:

1.  **Source:** (Who or what triggers the event?) e.g., *"An authenticated user"*, *"A malicious actor"*, *"The system's daily backup process"*
2.  **Stimulus:** (What is the event or condition?) e.g., *"logs in"*, *"attempts SQL injection"*, *"runs at peak load"*
3.  **Artifact:** (Which part of the system is affected?) e.g., *"the authentication service"*, *"the database"*, *"the entire application"*
4.  **Environment:** (Under what conditions does this happen?) e.g., *"during normal operation"*, *"during a denial-of-service attack"*, *"with 10,000 concurrent users"*
5.  **Response:** (What is the system's observable reaction?) e.g., *"responds within 2 seconds"*, *"blocks the attempt"*, *"maintains 99.9% availability"*
6.  **Response Measure:** (How is the response measured?) e.g., *"end-to-end latency (P99)"*, *"error rate"*, *"number of successful transactions"*

**Example:** *"An authenticated user (Source) logs in (Stimulus) to the authentication service (Artifact) during normal operation (Environment). The service responds within 2 seconds (Response) measured by end-to-end latency (P99) (Response Measure)."*

---

## Exercise: Drafting Your First Quality Scenario

### *Breakout Rooms (12 minutes)*

**Goal:** Apply the Stimulus-Response pattern to a real-world problem.

**Instructions:**

In your breakout rooms, choose ONE of the following scenarios (or propose your own) and draft **three complete Quality Attribute Scenarios (QAS)** using the **Stimulus-Response pattern** (Source, Stimulus, Artifact, Environment, Response, Response Measure).


1.  **E-commerce Checkout:** A user completing a purchase.
2.  **Video Streaming Service:** A user watching a live stream.
3.  **IoT Device Update:** A smart home device receiving a firmware update.
4.  **Healthcare Patient Record Access:** A doctor accessing a patient's medical history.

**Be prepared to share one of your best (and one of your most challenging) QAS with the main group.**

---

## Exemplar Response: E-commerce Checkout

### *Quality Scenario for User Purchase Latency*

```mermaid
flowchart TD
    A[Source: Authenticated User] --> B{Stimulus: Clicks 'Place Order'};
    B --> C[Artifact: Checkout Service];
    C --> D{Environment: Peak Load (1000 concurrent users)};
    D --> E[Response: Order processed];
    E --> F[Measure: End-to-end latency < 1.5 seconds (P99)];
```

**Explanation:** This scenario focuses on the performance aspect (latency) of the e-commerce checkout under stressful conditions, defining a clear, measurable target.

---

## Exemplar Response: Video Streaming Service

### *Quality Scenario for Live Stream Availability*

```mermaid
flowchart TD
    A[Source: Any User] --> B{Stimulus: Attempts to watch live stream}; 
    B --> C[Artifact: Streaming Playback Service];
    C --> D{Environment: During major sporting event (high demand)};
    D --> E[Response: Stream starts and plays without buffering];
    E --> F[Measure: 99.99% availability for stream start; <0.1% re-buffering rate];
```

**Explanation:** This scenario addresses the critical availability and seamless playback experience for a live streaming service, especially during peak events.

---

## Exemplar Response: IoT Device Update

### *Quality Scenario for Firmware Update Reliability*

```mermaid
flowchart TD
    A[Source: Central Management System] --> B{Stimulus: Initiates firmware update for batch of devices}; 
    B --> C[Artifact: Group of 100 IoT devices (mixed models)];
    C --> D{Environment: Devices online, varying network conditions (Wi-Fi, Cellular)};
    D --> E[Response: All devices successfully update firmware];
    E --> F[Measure: 99.5% update success rate within 15 minutes; <0.01% device bricking];
```

**Explanation:** This scenario prioritizes the reliability and success rate of critical firmware updates for IoT devices across diverse conditions, with safeguards against failure.

---

## Exemplar Response: Healthcare Patient Record Access

### *Quality Scenario for Patient Data Security*

```mermaid
flowchart TD
    A[Source: Unauthorized External User] --> B{Stimulus: Attempts to access patient records}; 
    B --> C[Artifact: Electronic Health Record (EHR) System];
    C --> D{Environment: Public network, using common attack vectors (e.g., SQLi, XSS)};
    D --> E[Response: Access denied, attempt logged, no data breach];
    E --> F[Measure: 0 unauthorized access successes; detection and alert within 5 seconds];
```

**Explanation:** This scenario highlights a critical security aspect for a healthcare system, focusing on preventing unauthorized access and ensuring data integrity and compliance.

---

## Module 2 Summary: Key Takeaways

### *Translating Ambiguity into Actionable Requirements*

**Recap:**

-   **The Stimulus-Response Pattern:** The core formula for defining measurable quality attribute scenarios.
-   **Google's Golden Signals:** Foundational metrics (Latency, Throughput, Errors, Saturation) for system monitoring.
-   **Building the Tree:** A structured, iterative process from stakeholder identification to scenario prioritization.
-   **Constructing QAS:** Step-by-step guidance on crafting precise, measurable quality scenarios.
-   **Practical Application:** Hands-on exercise to apply QAS drafting to real-world problems.

**Next Steps:** With these tools, you are equipped to move from vague "-ilities" to concrete, defensible architectural requirements. Module 3 will focus on *prioritizing* these scenarios to identify what truly matters most.

