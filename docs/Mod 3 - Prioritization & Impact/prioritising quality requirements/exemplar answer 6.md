### **Scenario 6: IoT Smart Home System - Exemplar Answer**

#### **Quality Tree**

```mermaid
graph TD
    A[Goal: Reliable & Secure Smart Home] --> B[Device Interactivity]
    A --> C[System Resilience]
    A --> D[Data & Control]
    A --> E[User Experience]

    B --> B1[Communication Speed]
    B1 --> Q1[1. Latency]

    C --> C1[Scalability]
    C1 --> Q2[2. Scalability]
    C1 --> Q8[8. Fault Tolerance]
    C1 --> Q9[9. Battery Life]

    D --> D1[Security & Privacy]
    D1 --> Q4[4. Security]
    D1 --> Q6[6. Privacy]
    D1 --> Q12[12. Firmware Updates]

    E --> E1[Usability]
    E1 --> Q7[7. Ease of Setup]
    E1 --> Q10[10. User Experience]
    E1 --> Q11[11. Voice Control]

    F[Core Automation] --> Q3[3. Reliability (Routines)]
    G[Device Compatibility] --> Q5[5. Interoperability]
```

#### **Prioritization Quadrant Diagram**

```mermaid
quadrantChart
  title "Prioritization of Quality Requirements - Scenario 6"
  x-axis "Low Architectural Impact" --> "High Architectural Impact"
  y-axis "Low Business Value" --> "High Business Value"
  quadrant-1 "ASRs (High Value, High Impact)"
  quadrant-2 "Quick Wins"
  quadrant-3 "Deprioritize"
  quadrant-4 "Avoid / Re-evaluate"
  1. Latency: [0.85, 0.9]
  2. Scalability: [0.8, 0.85]
  3. Reliability: [0.9, 0.92]
  4. Security: [0.93, 0.95]
  5. Interoperability: [0.75, 0.8]
  6. Privacy: [0.88, 0.9]
  7. Ease of Setup: [0.3, 0.6]
  8. Fault Tolerance: [0.7, 0.75]
  9. Battery Life: [0.5, 0.4]
  10. User Experience: [0.25, 0.65]
  11. Voice Control: [0.6, 0.55]
  12. Firmware Updates: [0.78, 0.7]
```
