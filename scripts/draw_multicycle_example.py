import bagpype as bp


def draw_multicycle_example():
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
    draw_multicycle_example()
