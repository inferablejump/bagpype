import bagpype as bp


def example_simple():

    # Create a pipeline
    p = bp.Pipeline()

    # Add instructions (operations)
    p += (i := bp.Op("add x1, x2, x3"))

    # Add edge and nodes
    p += bp.Edge(i.IF(0) >> i.DE(1) >> i.EX(2) >> i.WB(3), legend="simple_pipeline").\
        set_node_color("violet", True)

    # Visualize the pipeline
    p.draw()


def example_DEC():
    p = bp.Pipeline()
    start = 0
    p += (i0 := bp.Op("add x1, x2, x3"))
    p += (i1 := bp.Op("orr x4, x5, x6"))
    p += (i2 := bp.Op("b.eq"))
    i0.Issue(start + 0), i0.E(start + 1), i0.C(start + 2)
    i1.Issue(start + 1), i1.E(start + 2), i1.C(start + 3)
    i2.Issue(start + 2), i2.E(start + 3), i2.C(start + 4)
    p += bp.Edge(i0.Issue >> i1.Issue >> i2.Issue, "red").set_node_color("pink")
    p += bp.Edge(i0.E >> i1.E, "blue", "data dependency").set_node_color("lightblue")
    p.draw()


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
            op.add_node(bp.Node(f"stall{j}", i + 3 + j, style=stall_node_style))
        op.EX(2 * i + 3)
        op.WB(2 * i + 4)
        p += op

    for i in range(len(insns) - 1):
        p += bp.Edge(insns[i].WB >> insns[i + 1].EX, bp.EdgeStyle(color="red"), "data hazard").set_node_color("pink")

    p.draw(save=True, filename="assets/program.png")


def example_multicycle():
    """Example demonstrating multi-cycle nodes in a pipeline diagram."""
    p = bp.Pipeline()

    # Create operations
    load = bp.Op("ldr x1, [x2]")
    add = bp.Op("add x3, x1, x4")
    store = bp.Op("str x3, [x5]")

    # Load instruction: IF(1), DE(2), multi-cycle MEM(3-5), WB(6)
    load.IF(1)
    load.DE(2)
    load.EX(3)
    load.add_node(bp.Node("MEM", start_time=4, end_time=5, style=bp.NodeStyle(color="lightblue")))
    load.WB(6)

    # Add instruction: IF(2), DE(3), waits for load, EX(6), WB(7)
    add.IF(2)
    add.DE(3)
    add.add_node(bp.Node("stall", start_time=4, end_time=5, style=bp.NodeStyle(color="orange", linestyle="--")))
    add.EX(6)
    add.WB(7)

    # Store instruction: IF(3), DE(4), waits, EX(7), MEM(8-9)
    store.IF(3)
    store.DE(4)
    store.add_node(bp.Node("stall", start_time=5, end_time=6, style=bp.NodeStyle(color="orange", linestyle="--")))
    store.EX(7)
    store.MEM(8, 9)

    p += load
    p += add
    p += store

    # Data dependency: load WB -> add EX
    p += bp.Edge(load.MEM >> add.EX, bp.EdgeStyle(color="blue"), "RAW hazard")

    # Data dependency: add WB -> store EX
    p += bp.Edge(add.EX >> store.EX, bp.EdgeStyle(color="blue"), "RAW hazard")

    p.draw(save=True, filename="assets/multicycle.png")


if __name__ == "__main__":
    example_multicycle()
