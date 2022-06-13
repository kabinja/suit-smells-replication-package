import graphics
import time
import data

def pretty_label(metric):
    if metric == 'number_test_cases':
        return 'Number of Tests'
    if metric == 'number_keywords':
        return 'Number of Keywords'
    if metric == 'number_variables':
        return 'Number of Variables'
    if metric == 'number_lines':
        return 'Number of Lines of Code'
    
    raise RuntimeError('Invalid metric name: ' + metric)


def draw_number_commits(project_data):
    graphics.countplot(project_data, 'number-commits', y='project', x_label='Number of commits')


def draw_metric_distribution(project_data, metric):
    print("--------------------------------------------------")
    print("Metric Distribution: " + metric)
    print("--------------------------------------------------")
    print(project_data.groupby('project')[metric].describe())
    graphics.boxplot(project_data, data.pretty_name(metric, 'distribution'), metric, 'project', x_label=pretty_label(metric))


def draw_metric_evolution(project_data, metric):
    for project in project_data['project'].unique():
        evolution = project_data.loc[project_data['project'] == project]
        graphics.lineplot(evolution, data.pretty_name(metric, 'evolution') + '-' + project, 'date', metric, y_label=pretty_label(metric))


if __name__ == "__main__":
    t_start = time.perf_counter()

    project_data = data.load_projects()
    draw_metric_evolution(project_data, 'number_test_cases')
    draw_metric_evolution(project_data, 'number_keywords')
    draw_metric_evolution(project_data, 'number_variables')
    draw_metric_evolution(project_data, 'number_lines')
    
    draw_number_commits(project_data)
    draw_metric_distribution(project_data, 'number_test_cases')
    draw_metric_distribution(project_data, 'number_keywords')
    draw_metric_distribution(project_data, 'number_variables')
    draw_metric_distribution(project_data, 'number_lines') 

    t_stop = time.perf_counter()

    print("--------------------------------------------------")
    print("Elapsed time: %.1f [sec]" % ((t_stop-t_start)))
    print("--------------------------------------------------") 
