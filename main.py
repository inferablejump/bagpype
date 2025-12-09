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


if __name__ == "__main__":
    example_simple()
