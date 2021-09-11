import logging 
from utils.loader import Loader

logger = logging.getLogger(__name__)

DIR2GRAPH = './resource/graph.md'
DIR2TEMPLATE_ACTION = "config/template_action.json"

logger.debug("\t\tLoading Graph")
graphs = Loader.load_graph(DIR2GRAPH)

logger.debug("\t\tLoading Template Action")
actions = Loader.load_action(DIR2TEMPLATE_ACTION)