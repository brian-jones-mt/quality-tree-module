flowchart LR
  subgraph "Quality"
    A1["Performance"]
    A2["Scalability"]
  end
  subgraph "Refinement"
    B1["Asset Loading Speed"]
    B2["Load Test - Ramp"]
    B3["Load Test - Steady State"]
  end
  subgraph "Scenario"
    C1["Largest contentful paint must occur within 2.5 seconds"]
    C2["First page load must occur in 3 seconds"]
    C3["Site must be able to respond to up to 5k requests /second ina ramp pattern with 99% of requests taking no more than 3 seconds per load"]
    C4["Site must be able to respond to 1k requests / second for 48 hours. 99% of page loads should occur within 3s"]
  end

  A1 --> B1
  B1 --> C1
  B1 --> C2
  A2 --> B2
  B2 --> C3
  A2 --> B3
  B3 --> C4