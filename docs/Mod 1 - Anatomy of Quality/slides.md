# Module 1: The Anatomy of Quality

---

## The Anatomy of Quality

### *Understanding Quality as Quantifiable Trade-offs*

**Duration:** 1.75 hours

**Format:** Theory + Discussion

---

## Learning Objectives

By the end of this module, you will be able to:

- **Define** quality attributes and understand they are not binary states
- **Identify** vague requirements and reframe them into measurable criteria
- **Explain** the three-layer structure of quality attributes:
  - Quality Attribute (e.g., Performance)
  - Attribute Refinement (e.g., Latency vs. Throughput)
  - Quality Attribute Scenario (concrete, measurable event)
- **Recognize** architectural debt hidden in vague language
- **Distinguish** between wishes and achievable architectural goals

---

## Why You Need to Know This

Vague requirements like *"The system must be fast and secure"* are **architectural debt in disguise**.

As a lead developer, you will face:

- **Scope creep** from stakeholders who assume "quality" is free
- **Failed projects** because success criteria were never defined
- **Wasted engineering effort** building the wrong solution optimally
- **Post-launch surprises** when production performance doesn't match expectations

**This module teaches you to translate business speak into architectural decisions.**

By understanding quality as trade-offs, you gain the power to push back on impossible requirements with data, and to make intentional architectural choices instead of reactive firefighting.

---

## What does Quality mean to you?

Discussion: When we deliver a quality product - What did we do?

---

## Architectural Characteristics



<div class="reveal-list">
  <ul>
    <li onclick="this.classList.toggle('revealed')">
      <span class="initial">A</span>
      <span class="full-text">vailability</span>
    </li>
    <li onclick="this.classList.toggle('revealed')">
      <span class="initial">S</span>
      <span class="full-text">calability</span>
    </li>
    <li onclick="this.classList.toggle('revealed')">
      <span class="initial">P</span>
      <span class="full-text">erformance</span>
    </li>
    <li onclick="this.classList.toggle('revealed')">
      <span class="initial">S</span>
      <span class="full-text">ecurity</span>
    </li>
    <li onclick="this.classList.toggle('revealed')">
      <span class="initial">U</span>
      <span class="full-text">sability</span>
    </li>
    <li onclick="this.classList.toggle('revealed')">
      <span class="initial">T</span>
      <span class="full-text">estability</span>
    </li>
    <li onclick="this.classList.toggle('revealed')">
      <span class="initial">M</span>
      <span class="full-text">aintainability</span>
    </li>
  </ul>
</div>