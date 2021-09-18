import logging 
from utils.loader import Loader
from intent_classification.predict import NLPModel
logger = logging.getLogger(__name__)

DIR2GRAPH = './resource/graph.md'
DIR2TEMPLATE_ACTION = "config/template_action.json"
DIR2MODEL = './intent_classification/NLPModel.h5'

logger.debug("\t\tLoading Graph")
graphs = Loader.load_graph(DIR2GRAPH)

logger.debug("\t\tLoading Template Action")
actions = Loader.load_action(DIR2TEMPLATE_ACTION)

logger.debug("\t\tLoading NLP Model")
logger.debug("---------- LOADING MODEL ---------")
model = NLPModel(DIR2MODEL) 
logger.debug("---------- PREDICT -----------")
sample = "tên của mình chưa đúng nhé."
logger.debug(f"sentence: {sample}")
label, p = model.predict(sample)
logger.debug(f"Initialize - label: {label} - prob: {p}")