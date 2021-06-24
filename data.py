import pandas
import pathlib
import numpy

from os import listdir, stat, makedirs
from os.path import isfile, isdir, join, basename, exists
from itertools import chain

from scipy.stats import mannwhitneyu
from scipy.stats import shapiro


MINIMUM_COMMIT_NUMBER = 100

DATA_DIR = 'data'
CACHE_DIR = '__cache__'

HDF5_CACHE = CACHE_DIR + '/{}.h5'
TABLE_FOLDER = 'tables/'


def pretty_smell_name(name):
    if name == 'CALCULATE_EXPECTED_RESULTS_ON_THE_FLY':
        return "On the Fly"
    if name == 'COMPLICATED_SETUP_SCENARIOS':
        return "Complex Scenario"
    if name == 'CONDITIONAL_ASSERTION':
        return 'Conditional Assertion'
    if name == 'EAGER_TEST':
        return 'Eager Test'
    if name == 'HARDCODED_ENVIRONMENT_CONFIGURATIONS':
        return 'Hardcoded Environment'
    if name == 'HIDING_TEST_DATA_IN_FIXTURE_CODE':
        return 'Hidden Test Data'
    if name == 'LACK_OF_ENCAPSULATION':
        return 'Lack of Encapsulation'
    if name == 'LOGGING_IN_FIXTURE_CODE':
        return 'Noisy Logging'
    if name == 'LONG_TEST_STEPS':
        return 'Long Test Steps'
    if name == 'MIDDLE_MAN':
        return 'Middle Man'
    if name == 'MISSING_ASSERTION':
        return 'Missing Assertion'
    if name == 'HARD_CODED_VALUES':
        return 'Hardcoded Values'
    if name == 'OVER_CHECKING':
        return 'Over Checking'
    if name == 'COMPLEX_LOCATORS':
        return 'Sensitive Locator'
    if name == 'SNEAKY_CHECKING':
        return 'Sneaky Checking'
    if name == 'STINKY_SYNCHRONIZATION_SYNDROME':
        return 'Stinky Synchronization'
    if name == 'TEST_CLONES':
        return 'Army of Clones'
    if name == 'USING_PERSONAL_PRONOUN':
        return 'Narcissistic'

    raise RuntimeError('Invalid metric name: ' + name)


def pretty_name(metric, text):
    name = remove_suffix(remove_prefix(metric, 'number_'), '_value') + '-' + text
    return name.replace('_', '-').replace(' ', '-').lower()


def remove_suffix(string, suffix):
    if string.endswith(suffix):
        offset = len(suffix)
        string = string[:-offset]

    return string


def remove_prefix(string, prefix):
    if string.startswith(prefix):
        offset = len(prefix)
        string = string[offset:]

    return string


def get_files_list(parent, suffix):
    if not isdir(parent):
        return []

    return [join(parent, f) for f in listdir(parent) if isfile(join(parent, f)) and f.endswith(suffix)]

def get_project_list():
    projects = []

    for project_file in get_files_list(DATA_DIR, '-projects.csv'):
        if stat(project_file).st_size == 0:
            continue

        if len(open(project_file).readlines()) < MINIMUM_COMMIT_NUMBER + 1:
            continue

        projects.append(remove_suffix(basename(project_file), '-projects.csv'))

    return projects


def load_projects():
    cache_file = HDF5_CACHE.format('projects')

    if not isfile(cache_file):
        print('generating cache for ' + cache_file)
        _generate_cache_folder() 

        df = pandas.DataFrame()
        
        for project in get_project_list():
            current = pandas.read_csv(join('data', project + '-projects.csv'))
            current['project'] = project
            current['origin'] = 'industrial' if project == 'bgl' else 'open-source'
            current['date'] = current['date'].astype('datetime64[ns]')
            df = df.append(current)

            _store_file_in_cache(df, cache_file)
    
    return _load_cache(cache_file)


def load_smells():
    cache_file = HDF5_CACHE.format('smells')

    if not isfile(cache_file):
        print('generating cache for ' + cache_file)
        _generate_cache_folder() 

        df = pandas.DataFrame()
        
        for project in get_project_list():
            current = pandas.read_csv(join('data', project + '-smells.csv'))
            current['project'] = project
            current['origin'] = 'industrial' if project == 'bgl' else 'open-source'
            current['version'] = current['version'].astype('datetime64[ns]')
            current['smell_name'] = current['smell_name'].apply(lambda x: pretty_smell_name(x))
        
            df = df.append(current)

            _store_file_in_cache(df, cache_file)
    
    return _load_cache(cache_file)
        

def get_quantile_values(df, column, number_quantiles=1000):
    indexes = list(range(1, number_quantiles + 1, 1))

    quantiles_df = pandas.DataFrame(numpy.nan, index=indexes, columns=['Quantile', 'Value'])
    for i in indexes:
        quantile = i / number_quantiles
        value = df[column].quantile(q=quantile)

        quantiles_df.at[i, 'Quantile'] = quantile
        quantiles_df.at[i, 'Value'] = value

    return quantiles_df


def load_step_sequences():
    df = pandas.read_csv(join('data', 'total-test-statistics.csv'))
    step_sequences = df['step_sequences_sizes'].apply(lambda x: _string_to_array(x))
    
    values = list(filter(lambda x: x > 0, chain.from_iterable(step_sequences.values)))

    return pandas.DataFrame(values, columns=['Step Sizes'])


def save_table(data, name, groups=None, value=None, labels=None):
    _generate_folder(pathlib.Path(TABLE_FOLDER).resolve())

    if groups and value:
        table = data.groupby(groups)[value].describe().to_latex()
    elif labels:
        labels.append(value)
        table = data[labels].to_latex()
    else:
        table = data.to_latex()

    with open(TABLE_FOLDER + name + ".tex", "w") as text_file:
        text_file.write(table)


def _store_file_in_cache(df, cache_file):
    df.to_hdf(cache_file, key='data', mode='w')


def _load_cache(filename):
    return pandas.read_hdf(filename, 'data')


def _generate_cache_folder():
    _generate_folder(pathlib.Path(HDF5_CACHE.format('', '')).parent.resolve())


def _generate_folder(folder):
    if not exists(folder):
        makedirs(folder)

def _string_to_array(string):
    return [int(e) for e in string.replace('[', '').replace(']', '').split(',')]


def normal_distribution(series, name, alpha=0.05):
    stat, p = shapiro(series)


def compare_distribution(data, name, group, series, criteria, alpha=0.05):
    total = data.groupby([group]).apply(compute_mannwhitneyu, series, criteria, alpha).reset_index()
    save_table(total, name)    

def compute_mannwhitneyu(x, series, criteria, alpha):
    category = x[series].unique()

    try:
        stat, p = mannwhitneyu(x.loc[x[series] == category[0]][criteria], x.loc[x[series] == category[1]][criteria])
        results = {}
        results['statistics'] = stat
        results['p-value'] = p
        results['reject'] = p < alpha
    except:
        results = {}
        results['statistics'] = numpy.nan
        results['p-value'] = numpy.nan
        results['reject'] = False

    return pandas.Series(results, index=['statistics', 'p-value', 'reject'])
