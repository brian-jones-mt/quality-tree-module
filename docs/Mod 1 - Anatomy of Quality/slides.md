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
      <span class="full-text">vailability - Can users access this when they want it?</span>
    </li>    
    <li onclick="this.classList.toggle('revealed')">
      <span class="initial">P</span>
      <span class="full-text">erformance - Has your app done the thing fast enopugh to satisfy the user</span>
    </li>
    <li onclick="this.classList.toggle('revealed')">
      <span class="initial">Sc</span>
      <span class="full-text">alability - Can 10x the number of users you expected, access your application without degradation of performance?</span>
    </li>
    <li onclick="this.classList.toggle('revealed')">
      <span class="initial">Se</span>
      <span class="full-text">curity - Is the data in your app only viewable by those that should.</span>
    </li>
    <li onclick="this.classList.toggle('revealed')">
      <span class="initial">U</span>
      <span class="full-text">sability - Can all users do the thing they need to do with your app.</span>
    </li>
    <li onclick="this.classList.toggle('revealed')">
      <span class="initial">T</span>
      <span class="full-text">estability - Can your developers test the app before it is released.</span>
    </li>
    <li onclick="this.classList.toggle('revealed')">
      <span class="initial">M</span>
      <span class="full-text">aintainability - Can your developers add features to your application easily.</span>
    </li>
    <li onclick="this.classList.toggle('revealed')">
      <span class="initial">C</span>
      <span class="full-text">ost - How much is it going to cost to run the systems infrastructure.</span>
    </li>
  </ul>
</div>

--- 

## Tradeoffs

Almost all architectural decisions involve tradeoffs between characteristics.

As an example:

Splitting a C# MVC webside into a front end angular app, and a back end ASP.Net API

- Improves 
    - Maintainability
        - Front end developers can add features quicker
    - Performance
        - Server does less work generating full HTML page
        - less data to transfer between front end and back end      
        - Front end application can be cached as part of a content delivery network, inproving first load speed
    - Scalability
        - Since front end app is essentially a static site which passes smaller requests, back end can deal with more requests.
        - Back end scaling should be less required.
- Degrades
    - Cost
        - Need to pay for content delivery network, or static site as well as original server for API.
    - Maintainability
        - Needs two sets of developers (front end and back end) to communicate to deliver  a feature. Alternatively full stack engineers need to widen knowlege scope. 
    - Security
        - Need to implement greater controls to not trust user inputs from front end application 
    
--- 

## Tradeoff Discussion

*Group discussion - 6 mins = one question each*

What characteristics being traded off in the following scenarios:

- Moving from an on-premise to a cloud deployment of a MVC web app
- Breaking a single microservice out of a monolith
- Adding full end to end integration testing to a system
- Adding a developer to the team

---

## 🔍 Quality Refinement: Moving Down the Tree
To make these characteristics usable, we must refine them. A development team doesn't build "Performance"; they build "Low Latency" or "High Throughput."

The Refinement Process:

- Quality Attribute: Performance

- Refinement: Asset Loading Speed

- Scenario (The Leaf): "When a user on a 3G connection (Source/Stimulus) loads the homepage, the Largest Contentful Paint must occur within 2.5 seconds (Response)."

![Q=ualities, lead to scenarios](quality-refinement-scenario.png)