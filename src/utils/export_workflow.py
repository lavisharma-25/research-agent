from src.graph.builder import build_workflow
from src.core.settings import settings

workflow = build_workflow()

flow = workflow.get_graph()
png = flow.draw_mermaid_png()

with open(settings.WORFLOW_IMAGE_PATH, "wb") as f:
    f.write(png)