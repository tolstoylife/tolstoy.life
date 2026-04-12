# Mermaid Diagrams Reference for Obsidian

Obsidian supports Mermaid diagrams using fenced code blocks.

## Basic Syntax

````markdown
```mermaid
<diagram-type>
  <diagram-content>
```
````

## Flowcharts

### Basic Flowchart
````markdown
```mermaid
graph TD
    A[Start] --> B{Decision}
    B -->|Yes| C[Option 1]
    B -->|No| D[Option 2]
    C --> E[End]
    D --> E
```
````

### Direction Options
- `graph TD` - Top to bottom
- `graph LR` - Left to right
- `graph RL` - Right to left
- `graph BT` - Bottom to top

### Node Shapes
```mermaid
graph LR
    A[Rectangle]
    B(Rounded)
    C([Stadium])
    D[[Subroutine]]
    E[(Database)]
    F((Circle))
    G>Asymmetric]
    H{Diamond}
    I{{Hexagon}}
    J[/Parallelogram/]
    K[\Parallelogram\]
    L[/Trapezoid\]
    M[\Trapezoid/]
```

## Sequence Diagrams

````markdown
```mermaid
sequenceDiagram
    participant A as Alice
    participant J as John

    A->>+J: Hello John, how are you?
    A->>+J: John, can you hear me?
    J-->>-A: Hi Alice, I can hear you!
    J-->>-A: I feel great!
```
````

### Arrow Types
- `->` - Solid line without arrow
- `-->` - Dotted line without arrow
- `->>` - Solid line with arrow
- `-->>` - Dotted line with arrow
- `-x` - Solid line with cross
- `--x` - Dotted line with cross

## Class Diagrams

````markdown
```mermaid
classDiagram
    Animal <|-- Duck
    Animal <|-- Fish
    Animal : +int age
    Animal : +String gender
    Animal : +isMammal()
    class Duck{
        +String beakColor
        +swim()
        +quack()
    }
    class Fish{
        -int sizeInFeet
        -canEat()
    }
```
````

## State Diagrams

````markdown
```mermaid
stateDiagram-v2
    [*] --> Still
    Still --> [*]
    Still --> Moving
    Moving --> Still
    Moving --> Crash
    Crash --> [*]
```
````

## Entity Relationship Diagrams

````markdown
```mermaid
erDiagram
    CUSTOMER ||--o{ ORDER : places
    ORDER ||--|{ LINE-ITEM : contains
    CUSTOMER }|..|{ DELIVERY-ADDRESS : uses
```
````

### Relationship Types
- `||--||` - One to one
- `||--o{` - One to many
- `}o--o{` - Many to many
- `||--|{` - One to one or many
- `}|--|{` - Many to many (strict)

## Gantt Charts

````markdown
```mermaid
gantt
    title Project Timeline
    dateFormat YYYY-MM-DD
    section Planning
    Research           :a1, 2025-01-01, 30d
    Requirements       :after a1, 20d
    section Development
    Backend            :2025-02-01, 45d
    Frontend           :2025-02-15, 40d
    Testing            :2025-03-15, 20d
```
````

## Pie Charts

````markdown
```mermaid
pie title Project Time Distribution
    "Planning" : 20
    "Development" : 50
    "Testing" : 20
    "Documentation" : 10
```
````

## Git Graphs

````markdown
```mermaid
gitGraph
    commit
    commit
    branch develop
    checkout develop
    commit
    commit
    checkout main
    merge develop
    commit
    commit
```
````

## Timeline

````markdown
```mermaid
timeline
    title History of Social Media
    2002 : LinkedIn
    2004 : Facebook
         : Google
    2005 : Youtube
    2006 : Twitter
```
````

## Mindmaps

````markdown
```mermaid
mindmap
  root((Mindmap))
    Origins
      Long history
      Popularisation
        British popular psychology author Tony Buzan
    Research
      On effectiveness<br/>and features
      On Automatic creation
        Uses
            Creative techniques
            Strategic planning
            Argument mapping
```
````

## Linking to Obsidian Notes

Add `internal-link` class to nodes to create clickable links:

````markdown
```mermaid
graph TD
    Biology --> Chemistry
    Chemistry --> Physics

    class Biology,Chemistry,Physics internal-link;
```
````

### With Special Characters in Note Names

````markdown
```mermaid
graph TD
    A["⨳ Special Character Note"]
    B[Regular Note]
    A --> B

    class A,B internal-link;
```
````

## Styling

### Node Styling
````markdown
```mermaid
graph LR
    A[Default]
    B[Styled]

    style B fill:#f9f,stroke:#333,stroke-width:4px
```
````

### Custom CSS Classes
````markdown
```mermaid
graph LR
    A:::customClass --> B

    classDef customClass fill:#f96,stroke:#333,stroke-width:2px
```
````

## Common Patterns

### Process Flow
````markdown
```mermaid
graph LR
    Start([Start]) --> Input[/Input Data/]
    Input --> Process[Process]
    Process --> Decision{Valid?}
    Decision -->|Yes| Output[/Output/]
    Decision -->|No| Error[Error Handler]
    Error --> Input
    Output --> End([End])
```
````

### System Architecture
````markdown
```mermaid
graph TB
    subgraph Frontend
        UI[User Interface]
        State[State Management]
    end
    subgraph Backend
        API[API Layer]
        Logic[Business Logic]
        DB[(Database)]
    end
    UI --> API
    State --> API
    API --> Logic
    Logic --> DB
```
````

### User Journey
````markdown
```mermaid
journey
    title User Registration Journey
    section Account Creation
      Navigate to signup: 5: User
      Fill form: 3: User
      Submit: 4: User
    section Verification
      Receive email: 5: System
      Click link: 5: User
      Account activated: 5: System
```
````

## Tips

1. Use Live Editor for complex diagrams: https://mermaid-js.github.io/mermaid-live-editor
2. Mermaid version in Obsidian: 11.4.1 (as of latest)
3. Internal links don't appear in Graph view
4. Use subgraphs for logical grouping
5. Add comments with `%%` in mermaid code
6. Use meaningful IDs for nodes when creating internal links

## References

- Mermaid docs: https://mermaid.js.org/intro/
- Flowchart syntax: https://mermaid.js.org/syntax/flowchart.html
- Sequence diagrams: https://mermaid.js.org/syntax/sequenceDiagram.html
- Live editor: https://mermaid-js.github.io/mermaid-live-editor
