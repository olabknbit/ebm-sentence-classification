BACKGROUND = 'background'
INTERVENTION = 'intervention'
POPULATION = 'population'
OUTCOME = 'outcome'
OTHER = 'other'
STUDY_DESIGN = '\"study design\"'
STUDY_DESIGN_FILENAME_KEY = 'study_design'

POS_MODE = 'pos'
CUI_MODE = 'cui'
UNIGRAMS_MODE = 'uni'
BIGRAMS_MODE = 'bi'
POSITION_MODE = 'position'
HEADING_MODE = 'headings'

valid_feature_types = [POS_MODE, CUI_MODE, UNIGRAMS_MODE, BIGRAMS_MODE, POSITION_MODE, HEADING_MODE]
valid_labels = [BACKGROUND,
                INTERVENTION,
                POPULATION,
                OUTCOME,
                OTHER,
                STUDY_DESIGN_FILENAME_KEY]


def filter_out_feature_types(potential_feature_types):
    feature_types = []
    for feature_type in potential_feature_types:
        if feature_type in valid_feature_types:
            feature_types.append(feature_type)
        else:
            print('No such feature type', feature_type)
    feature_types.sort()
    return feature_types


def map_label(label):
    if label == STUDY_DESIGN:
        return STUDY_DESIGN_FILENAME_KEY
    elif label == STUDY_DESIGN_FILENAME_KEY:
        return STUDY_DESIGN
    else:
        return label
