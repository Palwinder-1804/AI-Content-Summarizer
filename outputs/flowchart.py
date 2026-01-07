from graphviz import Digraph
import re
import textwrap

def wrap_text(text, width=35):
    return "\n".join(textwrap.wrap(text, width))

def extract_steps(text, max_steps=8):
    """
    Extract meaningful steps from raw text
    """
    # Split by sentence endings
    sentences = re.split(r'(?<=[.!?])\s+', text)

    # Filter useful sentences
    steps = [
        s.strip()
        for s in sentences
        if len(s.split()) > 6
    ]

    return steps[:max_steps]

def generate_flowchart(raw_text):
    dot = Digraph(format="png")

    # Natural sizing (NO zoom)
    dot.attr(rankdir="TB", bgcolor="white")

    dot.attr(
        "node",
        shape="box",
        style="rounded,filled",
        fontname="Helvetica",
        fontsize="11",
        color="#1565C0"
    )

    dot.attr("edge", arrowsize="0.6", color="#424242")

    steps = extract_steps(raw_text)

    prev = None
    for i, step in enumerate(steps):
        node_id = f"N{i}"
        wrapped = wrap_text(step, width=38)

        fill = "#E3F2FD" if i % 2 == 0 else "#FFF9C4"
        dot.node(node_id, wrapped, fillcolor=fill)

        if prev is not None:
            dot.edge(prev, node_id)

        prev = node_id

    return dot
