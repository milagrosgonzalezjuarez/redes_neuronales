import matplotlib.pyplot as plt
import networkx as nx


# ==========================================
# FUNCIÓN PARA DIBUJAR LA RED NEURONAL
# ==========================================

def dibujar_red_neuronal(capas):

    # Crear un grafo dirigido
    G = nx.DiGraph()

    # Posiciones de los nodos
    pos = {}

    # Colores de los nodos
    colores = []

    # Nombres de cada capa
    nombres_capas = [
        "Entrada\n(4 Features)",
        "Capa Oculta\n(10 Neuronas)",
        "Salida\n(3 Clases)"
    ]

    # Colores para cada capa
    colores_capa = [
        "#4A90E2",
        "#50E3C2",
        "#F5A623"
    ]

    node_id = 0


    # ==========================================
    # CREAR LOS NODOS DE CADA CAPA
    # ==========================================

    for i, num_nodos in enumerate(capas):

        # Centrar verticalmente los nodos
        y_offset = (max(capas) - num_nodos) / 2.0

        for j in range(num_nodos):

            pos[node_id] = (
                i,
                j + y_offset
            )

            G.add_node(
                node_id,
                capa=i
            )

            colores.append(
                colores_capa[i]
            )

            node_id += 1


    # ==========================================
    # CREAR LAS CONEXIONES ENTRE LAS CAPAS
    # ==========================================

    offset_capa = 0

    for i in range(len(capas) - 1):

        nodos_capa_actual = range(
            offset_capa,
            offset_capa + capas[i]
        )

        nodos_siguiente_capa = range(
            offset_capa + capas[i],
            offset_capa + capas[i] + capas[i + 1]
        )

        # Conectar cada neurona con todas
        # las neuronas de la siguiente capa
        for n1 in nodos_capa_actual:

            for n2 in nodos_siguiente_capa:

                G.add_edge(
                    n1,
                    n2
                )

        offset_capa += capas[i]


    # ==========================================
    # DIBUJAR LA RED NEURONAL
    # ==========================================

    plt.figure(
        figsize=(10, 6)
    )


    # Dibujar neuronas
    nx.draw_networkx_nodes(
        G,
        pos,
        node_color=colores,
        node_size=700,
        alpha=0.9
    )


    # Dibujar conexiones
    nx.draw_networkx_edges(
        G,
        pos,
        alpha=0.15,
        edge_color="gray"
    )


    # ==========================================
    # NOMBRES DE LAS CAPAS
    # ==========================================

    for i, nombre in enumerate(nombres_capas):

        plt.text(
            i,
            max(capas) + 0.3,
            nombre,
            horizontalalignment="center",
            fontsize=11,
            fontweight="bold"
        )


    # ==========================================
    # TÍTULO
    # ==========================================

    plt.title(
        "Arquitectura Perceptrón Multicapa (MLP) - Dataset Iris",
        fontsize=14
    )

    plt.axis("off")

    plt.tight_layout()

    plt.show()


# ==========================================
# ARQUITECTURA DE LA RED
# ==========================================

# 4 neuronas de entrada
# 10 neuronas en la capa oculta
# 3 neuronas de salida

dibujar_red_neuronal([4, 10, 3])