import bagpype as bp


def draw_tpu_example():
    p = bp.Pipeline()
    p.renderer.config.x_axis_label_stride = 1
    p.renderer.config.x_axis_tick_stride = 1
    p.renderer.config.edge_routing = "orthogonal"

    # Create operations
    WLSU = bp.Op("WLSU")
    MLSU = bp.Op("MLSU")
    # VLSU = bp.Op("VLSU")
    MXU = bp.Op("MXU")
    VPU = bp.Op("VPU")

    VLEN = 4

    WLSU.load_weight1(0, VLEN)
    MLSU.load_activation(1, VLEN)
    MLSU.load_activation2(VLEN+1+1, VLEN)
    MXU.add_node(bp.Node("matmul_redosum", 0+VLEN+1, VLEN))
    VPU.softmax(0+VLEN+1+VLEN, VLEN)

    p += WLSU
    p += MLSU
    # p += VLSU
    p += MXU
    p += VPU

    p += bp.Edge(WLSU.load_weight1 >> MXU.matmul_redosum, bp.EdgeStyle(color="red"), "data dependency")
    p += bp.Edge(MLSU.load_activation >> MXU.matmul_redosum, bp.EdgeStyle(color="red"))
    p += bp.Edge(MXU.matmul_redosum >> VPU.softmax, bp.EdgeStyle(color="red"))

    p.draw()
    # p.draw(save=True, filename="assets/tpu.png")


if __name__ == "__main__":
    draw_tpu_example()
