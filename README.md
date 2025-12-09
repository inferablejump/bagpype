# Bagpype: Better Academic Graphs for Processor Pipelines

A Python library for describing and visualizing processor pipeline diagrams with a clean, intuitive syntax.

## Installation

```bash
pip install bagpype
```

## Quick Start

```python
import bagpype as bp

# Create a pipeline
p = bp.Pipeline()

# Add instructions (operations)
p += (i := bp.Op("add x1, x2, x3"))

# Add edge and nodes 
p += bp.Edge(i.IF(0) >> i.DE(1) >> i.EX(2) >> i.WB(3), legend="simple_pipeline").set_node_color("violet")

# Visualize the pipeline
p.draw()
```

## Core Concepts

### Operations (Op)
An operation represents one instruction in your pipeline. Each operation is visualized as a row and can contain multiple pipeline stages.

```python
# A one-liner
p += (i0 := Op("add x1, x2, x3")) 
# for the faint of heart
i1 = Op("orr x4, x5, x6")         
p.add_op(i1)
```

### Nodes
Nodes represent pipeline stages (fetch, decode, execute, etc.). They're positioned by time (x-axis) and instruction (y-axis).

```python
# Create nodes with timing
i0.fetch(0)             # fetch at cycle 0
i0.decode(1, "red")     # decode at cycle 1, optional color 
i0.add_node(Node("execute", 2))    # for the faint of heart

# Access nodes later
print(i0.fetch)  # fetch@0
```

Multi-cycle operation are also supported, by specifying an optional "duration" argument. If note specified, they default to 1.

### Edges
Edges show dependencies between pipeline stages using the `>>` operator:

```python
# Simple dependency
edge1 = Edge(i0.execute >> i1.fetch)

# Chain multiple dependencies, optional color and legend
i0.fetch(0) # create a fetch node
# create decode and execute node in the edge declaration 
edge2 = Edge(i0.fetch >> i0.decode(1) >> i0.execute(2), "purple", "simple-pipeline")

# Avoid using weird syntax, by using other weird syntax
edge3 = Edge([i0.execute, i1.decode]).set_edge_color("blue").set_edge_legend("forwarding")

# Style Nodes along the edge
edge3 = Edge(i0.execute >> i1.decode).set_node_color("lightblue")
```

### Pipeline
The main container that holds operations and edges:

```python
p = Pipeline()
p += i0                    # add operation
p += i1                    # add another operation  
p += edge1                 # add dependency
p.draw()                   # visualize
# saving
p.draw(save=True, file="something.png")                   
```

## Styling Options

### Node Colors
```python
i0.fetch(0, color="lightblue")
i0.decode(1, color="lightgreen")
```

### Edge Colors and Legends
```python
p += Edge(i0.execute >> i1.fetch).set_edge_color("red").set_edge_legend("data hazard")
p += Edge(i0.writeback >> i2.fetch).set_edge_color("blue").set_edge_legend("control hazard")
```

## Example: 5-Stage Pipeline with Hazards

This example demonstrates why we might want to use a DSL to describe the pipeline. 

```python
def example_program():
    p = bp.Pipeline()

    stall_node_style = bp.NodeStyle(color="red", linestyle="--")

    # Three instructions
    insns = [bp.Op("add x1, x1, x3"),
             bp.Op("sub x4, x1, x5"),  # depends on x1 from i0
             bp.Op("mul x6, x4, x7")]  # depends on x4 from i1

    # Normal pipeline stages
    for i, op in enumerate(insns):
        op.IF(i + 1)
        op.DE(i + 2)
        # add stall nodes
        for j in range(i):
            op.add_node(bp.Node(f"stall{j}", i + 3 + j, stall_node_style))
        op.EX(2 * i + 3)
        op.WB(2 * i + 4)
        p += op

    for i in range(len(insns) - 1):
        p += bp.Edge(insns[i].WB >> insns[i + 1].EX, bp.EdgeStyle(color="red"), "data hazard").set_node_color("pink")

    p.draw(save=True, filename="assets/program.png")
```
This produces the follwing diagram:
![programmatically generated diagram](assets/program.png)

## Requirements

- Python ≥ 3.10
- matplotlib ≥ 3.7.0
- seaborn ≥ 0.12.0

## License

MIT 