import getopt, sys
import pdb
from create_similar_token_sets import create_similar_token
from create_learning_state_embeddings import create_learning_embedding 
from validate_learning_similarity import validate_learning_similarity
from run_gensim_model import run_gensim_model

fullCmdArguments = sys.argv
argumentList = fullCmdArguments[1:]
unixOptions = 'r:m:c:s:'
gnuOptions = ['readfileaffix=','method=','comparison=','sample=']

try:
    arguments, values = getopt.getopt(argumentList, unixOptions, gnuOptions)
except:
    sys.exit(2)


# allow pass in argument for individual runs
def pass_in_arguments():
     for currentArgument, currentValue in arguments:
         if currentArgument in ['-r','--readfileaffix']:
             read_file_affix = currentValue
             print( ("read file affix with: %s") % (read_file_affix))
         if currentArgument in '--method':
             method = currentValue
             print( ("read file affix with: %s") % (method))
         if currentArgument in '--comparison':
             find_nearest_comparison = currentValue
             print( ("with comparison: %s") % (find_nearest_comparison))
         if currentArgument in '--sample':
             remediation_sample_number = int(currentValue)
             print( ("with sample: %s") % (remediation_sample_number))

         create_similar_token(
                     read_file_affix = read_file_affix,
                     method = method,
                     find_nearest_comparison = find_nearest_comparison,
                     remediation_sample_number = remediation_sample_number )

         validate_learning_similarity(
                     read_file_affix = read_file_affix,
                     method = method,
                     find_nearest_comparison = find_nearest_comparison,
                     remediation_sample_number = remediation_sample_number)

hyperparameters = { 
     "hyperparameter1":{"window":5, "embedding":30, "read_file_affix":'full'},
     #"hyperparameter2":{"window":10, "embedding":30, "read_file_affix":'full'},
     "hyperparameter3":{"window":15, "embedding":30, "read_file_affix":'full'},
     "hyperparameter4":{"window":20, "embedding":30, "read_file_affix":'full'},
     "hyperparameter5":{"window":10, "embedding":15, "read_file_affix":'full'},
     "hyperparameter6":{"window":10, "embedding":20, "read_file_affix":'full'},
     "hyperparameter7":{"window":10, "embedding":30, "read_file_affix":'full'},
     "hyperparameter8":{"window":10, "embedding":40, "read_file_affix":'full'}
}
     



match_parameters = {
    "responseCosine1":{ "method": 'cosine', 
        "find_nearest_comparison": 'response', "remediation_sample_number": 1},
    "responseCosine5":{ "method": 'cosine', 
         "find_nearest_comparison": 'response', "remediation_sample_number": 5},
    "responseCosine10": { "method": 'cosine', 
        "find_nearest_comparison": 'response', "remediation_sample_number": 10},
    "responseCosine20": { "method": 'cosine', 
        "find_nearest_comparison": 'response', "remediation_sample_number": 20},
    "learnCosine1": { "method": 'cosine', 
        "find_nearest_comparison": 'learn', "remediation_sample_number": 1},
    "learnCosine5": { "method": 'cosine', 
        "find_nearest_comparison": 'learn', "remediation_sample_number": 5},
    "learnCosine10": { "method": 'cosine', 
        "find_nearest_comparison": 'learn', "remediation_sample_number": 10},
    "learnCosine20": { "method": 'cosine', 
        "find_nearest_comparison": 'learn', "remediation_sample_number": 20}
   # "responseEuclidean1": { "method": 'euclidean', 
   #     "find_nearest_comparison": 'response', "remediation_sample_number": 1},
   # "responseEuclidean5": { "method": 'euclidean', 
   #     "find_nearest_comparison": 'response', "remediation_sample_number": 5},
   # "responseEuclidean10": { "method": 'euclidean', 
   #     "find_nearest_comparison": 'response', "remediation_sample_number": 10}
}

for hyper in hyperparameters:
    '''
      for each hyperparameter run the gensim model
      this takes about a few hours for each iteration
    '''
    window_size = hyperparameters[hyper]["window"]
    embed_size = hyperparameters[hyper]["embedding"]
    iter_num = 30
    append_to_affix = "w" + str(window_size) + "e" + str(embed_size)
    read_file_affix = hyperparameters[hyper]["read_file_affix"] + append_to_affix
    print('iterate on:')
    print(read_file_affix) 
    run_gensim_model(window_size, embed_size, iter_num) 
    create_learning_embedding(read_file_affix)
    for iter in match_parameters:
        method =  match_parameters[iter]["method"]
        find_nearest_comparison =  match_parameters[iter]["find_nearest_comparison"]
        remediation_sample_number =  match_parameters[iter]["remediation_sample_number"]
        # write similarity token to the following path:
        # cahl_analysis/<method>_<nearest_comparison>_<readfileaffix>_w<window_size>e<embed_size>r<remediation_sample>/remediation_match_tokens.tsv
        create_similar_token(
                read_file_affix = read_file_affix,
                method = method,
                find_nearest_comparison = find_nearest_comparison,
                remediation_sample_number = remediation_sample_number )
        #write the precision / recall rate and the remediation match with match logic
        # to the following path
        # cahl_analysis/<method>_<nearest_comparison>_<readfileaffix>_w<window_size>e<embed_size>r<remediation_sample>
        # with the following files:
        # remediation_match_tf: matched prerequisites for each learning token, true/false whether any match included in prerequisite
        # _accuracy_: summary precision and recall rate 
        # _sample_: sample tokens that either match (true) or did not match (false)
        validate_learning_similarity(
                read_file_affix = read_file_affix,
                method = method,
                find_nearest_comparison = find_nearest_comparison,
                remediation_sample_number = remediation_sample_number)
