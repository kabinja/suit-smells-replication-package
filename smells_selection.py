import pandas
import graphics

def load_xls():
    return pandas.read_excel(open('data/smells_catalog.xlsx', 'rb'), sheet_name='catalog')


def compute_issues_df(smells):
    data = []
    for level in smells['Level'].unique():
        total_readability = smells.loc[(smells['Level'] == level) & (smells['Readability issue'].notnull())].shape[0]
        total_maintenance = smells.loc[(smells['Level'] == level) & (smells['Maintenance issue'].notnull())].shape[0]
        total_execution = smells.loc[(smells['Level'] == level) & (smells['Execution issue'].notnull())].shape[0]

        selected_readability = smells.loc[(smells['Level'] == level) & (smells['Can compute metric from test code'] == 'YES') & (smells['Readability issue'].notnull())].shape[0]
        selected_maintenance = smells.loc[(smells['Level'] == level) & (smells['Can compute metric from test code'] == 'YES') & (smells['Maintenance issue'].notnull())].shape[0]
        selected_execution = smells.loc[(smells['Level'] == level) & (smells['Can compute metric from test code'] == 'YES') & (smells['Execution issue'].notnull())].shape[0]

        data.append([level, 'Readability', total_readability, selected_readability])
        data.append([level, 'Maintenance', total_maintenance, selected_maintenance])
        data.append([level, 'Execution', total_execution, selected_execution])

    return pandas.DataFrame(data, columns=['Level', 'Issue Type', 'Total', 'Selected'])


def compute_sources_df(smells):
    data = []
    for level in smells['Level'].unique():
        total_grey_literature = smells.loc[(smells['Level'] == level) & (smells['Source'] == 'Grey Literature')].shape[0]
        total_academia = smells.loc[(smells['Level'] == level) & (smells['Source'] == 'Academia')].shape[0]

        selected_grey_literature = smells.loc[(smells['Level'] == level) & (smells['Can compute metric from test code'] == 'YES') & (smells['Source'] == 'Grey Literature')].shape[0]
        selected_academia = smells.loc[(smells['Level'] == level) & (smells['Can compute metric from test code'] == 'YES') & (smells['Source'] == 'Academia')].shape[0]

        data.append([level, 'Grey Literature', total_grey_literature, selected_grey_literature])
        data.append([level, 'Academia', total_academia, selected_academia])

    return pandas.DataFrame(data, columns=['Level', 'Source', 'Total', 'Selected'])


def plot_source_distribution(smells):
    df = compute_sources_df(smells)
    for level in smells['Level'].unique():
         graphics.barplot(df.loc[df['Level'] == level], 'source-distribution-{}'.format(level.lower()), 'Total', 'Source', x_label='number of smells', fig_size=(8,4), overlay_x='Selected')      


def plot_issues_distribution(smells):
    df = compute_issues_df(smells)
    for level in smells['Level'].unique():
        graphics.barplot(df.loc[df['Level'] == level], 'issue-distribution-{}'.format(level.lower()), 'Total', 'Issue Type', x_label='number of smells', fig_size=(8,4), overlay_x='Selected')


if __name__ == "__main__":
    smells = load_xls()
    plot_source_distribution(smells)
    plot_issues_distribution(smells)