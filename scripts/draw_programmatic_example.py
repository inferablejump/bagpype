import bagpype as bp


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


if __name__ == "__main__":
    example_program()
