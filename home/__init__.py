from utils.loader import Loader
from intent_classification.predict import NLPModel
import logging 
import environ

env = environ.Env()
environ.Env.read_env()

logger = logging.getLogger(__name__)

DIR2GRAPH = env('DIR2GRAPH')
DIR2TEMPLATE_ACTION = env('DIR2TEMPLATE_ACTION')
DIR2MODEL = env('DIR2MODEL')

logger.debug("\t\tLoading Graph")
graphs = Loader.load_graph(DIR2GRAPH)

logger.debug("\t\tLoading Template Action")
actions = Loader.load_action(DIR2TEMPLATE_ACTION)

logger.debug("\t\tLoading NLP Model")
logger.debug("---------- LOADING MODEL ---------")
model = NLPModel(DIR2MODEL) 
logger.debug("Successfully pre-load resource!")
