import pandas
import graphics
import time
import data
import textdistance

from kneed import KneeLocator


TO_IGNORE = ['Eager Test', 'Complex Scenario','Same Documentation', 'Missing Documentation']


def pretty_column_name(column):
    if column == 'number_lines':
        return 'Number of Lines'
    if column == 'number_test_cases':
        return 'Number of Test Cases'
    if column == 'number_keywords':
        return 'Number of Keywords'
    if column == 'smell_raw_value':
        return 'Raw Smell Value'
    if column == 'smell_normalized_value':
        return 'Normalized Smell Value'
    if column == 'fixes':
        return 'Number of Fixes'
    if column == 'test_case_size':
        return 'Test Case Size'
    if column == 'test_case_sequence':
        return 'Test Case Sequence Size'
    if column == 'test_case_level':
        return 'Test Case Level'
    

    raise RuntimeError('Invalid label name: ' + column)

def compute_number_fixes_per_test(smell_data):
    total = smell_data.loc[smell_data['smell_raw_value'] > 0].groupby(['origin', 'test_case_name', 'smell_name'])['fixes'].sum().reset_index()
    percent = total.groupby(['origin', 'smell_name'])['fixes'].apply(lambda c: (c > 0).sum() / len(c) * 100).reset_index()
    percent.rename(columns={'fixes': 'percent'}, inplace=True)
    
    return percent


def draw_number_fixes(smell_data):
    count = smell_data.groupby(['origin', 'smell_name'])['fixes'].sum().reset_index()
    percent = compute_number_fixes_per_test(smell_data)

    graphics.barplot(count, 'number-fixes', x='fixes', y='smell_name', hue='origin', x_label="Number of Refactoring Actions", fig_size=(6,8), hue_order=['open-source', 'industrial'])
    graphics.barplot(percent, 'percent-fixes', x='percent', y='smell_name', hue='origin', x_label="Percentage Symptomatic Tests Refactored", fig_size=(6,8), hue_order=['open-source', 'industrial'])

    data.save_table(count, 'count-fixes')
    data.save_table(percent, 'percent-fixes')


def draw_metric_evolution(smell_data, metric, **kwargs):
    for project in smell_data['project'].unique():
        evolution = smell_data.loc[smell_data['project'] == project]
        fig_name = data.pretty_name(metric, 'evolution-' + project)
        graphics.lineplot(evolution, fig_name, 'version', metric, hue='smell_name', y_label=pretty_column_name(metric), legend_pos='outside', fig_size=(8,4), **kwargs)

def draw_metric_distribution(smell_data, metric, fig_name=None, **kwargs):
    order = smell_data['smell_name'].unique()
    order.sort()
    metric_name = metric + "_" + str(kwargs.get("x_lim")[1]) if 'x_lim' in kwargs else metric
    fig_name = data.pretty_name(metric_name if fig_name == None else fig_name, 'distribution')

    print("--------------------------------------------------")
    print("Metric Distribution: " + metric)
    print("--------------------------------------------------")

    data.save_table(smell_data, fig_name, ['origin', 'smell_name'], metric)
    graphics.violinplot(smell_data, fig_name + '-violinplot', metric, 'smell_name', fig_size=(6,8), hue='origin', hue_order=['open-source', 'industrial'], inner='box', linewidth=0.5, **kwargs)
    graphics.boxplot(smell_data, fig_name + '-boxplot', metric, 'smell_name', fig_size=(6,8), hue='origin', hue_order=['open-source', 'industrial'], legend_pos='above', order=order, **kwargs)


def draw_metric_distribution_per_project(project_data, metric):
    print("--------------------------------------------------")
    print("Metric Distribution: " + metric)
    print("--------------------------------------------------")

    fig_name = data.pretty_name(metric, 'distribution')

    data.save_table(project_data, fig_name, ['project'], metric)
    graphics.boxplot(project_data, fig_name, metric, 'project', x_label=pretty_column_name(metric))


def draw_distribution_step_sequences(number_quantiles):
    steps = data.load_step_sequences()
    graphics.countplot(steps, 'step-sequences-distribution', x='Step Sizes')

    quantiles = data.get_quantile_values(steps, 'Step Sizes', number_quantiles)
    kn = KneeLocator(quantiles['Quantile'].to_numpy(), quantiles['Value'].to_numpy(), curve='convex', direction='increasing')

    print(kn.knee)
    print(kn.knee_y)
    graphics.lineplot(quantiles, 'step-sequences-quantiles', x_label='Quantile', y_label='Length of Step Sequence', x='Quantile', y='Value', v_lines=[kn.knee], h_lines=[kn.knee_y])


def draw_metric_evolution_one_shot(smell_data, metric, project, smell_name, **kwargs):
    evolution = smell_data.loc[(smell_data['project'] == project) & (smell_data['smell_name'] == smell_name)]
    df = evolution.groupby(['version'])[metric].sum().reset_index()
    fig_name = data.pretty_name(metric, 'evolution-' + project + '-' + smell_name)
    
    graphics.lineplot(df, fig_name, 'version', metric, **kwargs)


def draw_diffusion(smell_data):
        diffusion = smell_data.groupby(['origin', 'smell_name'])['smell_raw_value'].apply(lambda c: (c > 0).sum() / len(c) * 100).reset_index()
        order = diffusion['smell_name'].unique()
        order.sort()
        graphics.barplot(diffusion, 'diffusion', x='smell_raw_value', y='smell_name', hue='origin', x_label="Percentage Symptomatic Tests", fig_size=(6,8), hue_order=['open-source', 'industrial'], legend_pos='above', order=order)
        data.save_table(diffusion, 'diffusion')

def compute_ranking_statistics(smell_data):
    similarity_results = []

    normalized = smell_data.groupby(['origin', 'smell_name'])['smell_normalized_value'].mean().reset_index()
    normalized_industrial = normalized.loc[normalized['origin'] == 'industrial'].sort_values(by=['smell_normalized_value', 'smell_name'])['smell_name'].tolist()
    normalized_open_source = normalized.loc[normalized['origin'] == 'open-source'].sort_values(by=['smell_normalized_value', 'smell_name'])['smell_name'].tolist()
    levenshtein_normalized = textdistance.levenshtein.similarity(normalized_open_source, normalized_industrial) / max(len(normalized_industrial), len(normalized_open_source))
    similarity_results.append({'metric': 'Symptoms Percent', 'value': levenshtein_normalized})

    raw = smell_data.loc[smell_data['fixes'] > 0].groupby(['origin', 'smell_name'])['smell_raw_value'].mean().reset_index()
    raw_industrial = raw.loc[raw['origin'] == 'industrial'].sort_values(by=['smell_raw_value', 'smell_name'])['smell_name'].tolist()
    raw_open_source = raw.loc[raw['origin'] == 'open-source'].sort_values(by=['smell_raw_value', 'smell_name'])['smell_name'].tolist()
    levenshtein_raw = textdistance.levenshtein.similarity(raw_open_source, raw_industrial) / max(len(raw_industrial), len(raw_open_source))
    similarity_results.append({'metric': 'Symtoms Count', 'value': levenshtein_raw})

    fixes_percent = compute_number_fixes_per_test(smell_data)
    fixes_percent_industrial = fixes_percent.loc[fixes_percent['origin'] == 'industrial'].sort_values(by=['percent', 'smell_name'])['smell_name'].tolist()
    fixes_percent_open_source = fixes_percent.loc[fixes_percent['origin'] == 'open-source'].sort_values(by=['percent', 'smell_name'])['smell_name'].tolist()
    levenshtein_percent_fixes = textdistance.levenshtein.similarity(fixes_percent_industrial, fixes_percent_open_source) / max(len(fixes_percent_open_source), len(fixes_percent_industrial))
    similarity_results.append({'metric': 'Fixes Percent', 'value': levenshtein_percent_fixes})

    fixes_count = smell_data.groupby(['origin', 'smell_name'])['fixes'].sum().reset_index()
    fixes_industrial = fixes_count.loc[fixes_count['origin'] == 'industrial'].sort_values(by=['fixes', 'smell_name'])['smell_name'].tolist()
    fixes_open_source = fixes_count.loc[fixes_count['origin'] == 'open-source'].sort_values(by=['fixes', 'smell_name'])['smell_name'].tolist()
    levenshtein_fixes = textdistance.levenshtein.similarity(fixes_open_source, fixes_industrial) / max(len(fixes_industrial), len(fixes_open_source))
    similarity_results.append({'metric': 'Fixes Count', 'value': levenshtein_fixes})

    data.save_table(pandas.DataFrame(similarity_results), 'similarity-analysis')

def compute_statistics(smell_data):
    data.compare_distribution(smell_data.loc[smell_data['fixes'] > 0], 'statistics-compare-distribution', 'smell_name', 'origin', 'smell_raw_value')
    compute_ranking_statistics(smell_data)

if __name__ == "__main__":
    t_start = time.perf_counter()

    smell_data = data.load_smells()
    smell_data = smell_data.loc[~smell_data['smell_name'].isin(TO_IGNORE)]

    compute_statistics(smell_data)
    draw_diffusion(smell_data)

    draw_number_fixes(smell_data)
    draw_metric_evolution(smell_data, 'smell_normalized_value')
    draw_metric_evolution(smell_data, 'fixes')
    draw_metric_evolution(smell_data, 'smell_raw_value')

    draw_metric_distribution(smell_data, 'smell_normalized_value', x_label='Percentage of Symptoms per Test')
    draw_metric_distribution(smell_data.loc[smell_data['fixes'] > 0], 'smell_raw_value', x_label='Number of Symptoms per Test')
    draw_metric_distribution(smell_data.loc[smell_data['fixes'] > 0], 'smell_raw_value', x_label='Number of Symptoms per Test', x_lim=(0,200))
    draw_metric_distribution(smell_data, 'fixes', x_label='Number of Refactoring Actions per test')
    draw_metric_distribution(smell_data.loc[smell_data['fixes'] != 0], 'fixes', fig_name='fixes_no_null', x_label='Number of Refactoring Actions per test')

    draw_metric_distribution_per_project(smell_data, 'test_case_size')
    draw_metric_distribution_per_project(smell_data, 'test_case_sequence')
    draw_metric_distribution_per_project(smell_data, 'test_case_level')

    draw_metric_evolution_one_shot(smell_data, 'smell_raw_value', 'bgl', 'Narcissistic', y_label='Number of symptoms')

    number_quantiles = 1000
    draw_distribution_step_sequences(number_quantiles)

    t_stop = time.perf_counter()

    print("--------------------------------------------------")
    print("Elapsed time: %.1f [sec]" % ((t_stop-t_start)))
    print("--------------------------------------------------") 
