import bagpype as bp


def draw_tpu_example():
    p = bp.Pipeline()
    p.renderer.config.x_axis_label_stride = 8
    p.renderer.config.x_axis_tick_stride = 8

    # Create operations
    WLSU = bp.Op("WLSU")
    MLSU = bp.Op("MLSU")
    VLSU = bp.Op("VLSU")
    MXU  = bp.Op("MXU")
    VPU  = bp.Op("VPU")

    WLSU.load_weight1(0, 32)
    WLSU.load_weight2(33, 32)
    MLSU.load_activation(1, 32)
    MLSU.load_activation2(33+1, 32)
    MXU.add_node(bp.Node("matmul_redosum", 0+33+1, 32))
    VPU.softmax(0+33+32+1, 32)

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
