import pandas as pd
import mysql.connector
from datetime import datetime, timedelta
import numpy as np
import statsmodels.api as sm
from statsmodels.formula.api import ols
from numpy.polynomial.polynomial import polyfit
import scipy.stats as stats
from scipy.stats import pearsonr
from scipy.stats import spearmanr
from scipy.stats import chi2_contingency
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from IPython.display import display, HTML


# DEFINE "GLOBAL" VARIABLES
conn = mysql.connector.connect(user='root',
                               host='127.0.0.1',
                               database='mydb2',
                               autocommit=True)
cur = conn.cursor()

credentials = "mysql://root@localhost:3306/mydb2"
num_participants = 40

cur.execute(
    """
    SELECT 
        participant_id
    FROM participants
    WHERE 
    xp_level='Expert'
    """
)
experts = cur.fetchall()  # should get 20 experts
experts = [tup[0] for tup in experts]

cur.execute(
    """
    SELECT 
        participant_id
    FROM participants
    WHERE 
    xp_level='Python Novice'
    """
)
middle = cur.fetchall()  # should get 9 python-only novices
middle = [tup[0] for tup in middle]

cur.execute(
    """
    SELECT 
        participant_id
    FROM participants
    WHERE 
    xp_level='True Novice'
    """
)
novices = cur.fetchall()  # should get 11 true novices
novices = [tup[0] for tup in novices]

expert_patch = mpatches.Patch(color='blue', label='expert')
middle_patch = mpatches.Patch(color='purple', label='python-only novices')
novice_patch = mpatches.Patch(color='orange', label='novice')


# COLOR class (for formatting)
class color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

    @classmethod
    def bold(self, s):
        return self.BOLD + s + self.END


# START FUNCTION DEFINITIONS

def label_group(row):
    '''Labels xp_level as just Expert or Novice.'''
    if row['participant_id'] in experts:
        return 'Expert'
    if row['participant_id'] not in experts:
        return 'Novice'
    return 'No Group'


def avg_session_times():
    """Return list of average session times per participant."""
    conn = mysql.connector.connect(user='root',
                                   host='127.0.0.1',
                                   database='mydb2',
                                   autocommit=True)  # TODO: change to 'mydb' when not testing
    cur = conn.cursor()

    my_query = """
        SELECT 
            participants.participant_id,
            AVG(sessions.total_time) 'Average Session Duration'
        FROM sessions
        INNER JOIN participants
        ON sessions.participant_id=participants.participant_id
        GROUP BY participant_id;
    """
    cur.execute(my_query)
    results = cur.fetchall()

    participant_ids = [i for i in range(1, num_participants + 1)]
    avg_time = [0 for k in range(num_participants)]  # average session duration

    for r in results:
        # r: (participant_id, programming_xp, python_xp, avg_time)
        i = r[0]-1  # participant_id - 1
        avg_time[i] = float(r[1])

    return avg_time


def experiences():
    """Return list of (participant_id, programming_xp, python_xp, professional_xp) tuples"""
    conn = mysql.connector.connect(user='root',
                                   host='127.0.0.1',
                                   database='mydb2',
                                   autocommit=True)  # TODO: change to 'mydb' when not testing
    cur = conn.cursor()

    my_query = """
        SELECT 
            participant_id,
            programming_xp,
            python_xp,
            professional_xp
        FROM participants
    """
    cur.execute(my_query)
    results = cur.fetchall()

    return results


def error_time_stats(cur):
    """Break down average session times and standard
    deviation for each stimuli and error type."""
    query = """
    SELECT
        stimuli.stimuli_id,
        stimuli.error_type,
        AVG(sessions.total_time) AS 'Average Session Duration',
        STD(sessions.total_time) AS 'Standard Deviation of Session Duration',
        MIN(sessions.total_time) AS 'Min Session Duration',
        MAX(sessions.total_time) AS 'Max Session Duration'
    FROM stimuli
    INNER JOIN sessions
    ON stimuli.stimuli_id=sessions.stimuli_id
    GROUP BY stimuli.stimuli_id;
    """
    cur.execute(query)
    results = cur.fetchall()
    print(results)


def get_avg_session_time_correlation(y, y_name):
    avg_time = avg_session_times()

    x = np.asarray(avg_time)

    corr, spearman_p = spearmanr(x, y)

    print("SPEARMAN'S R FOR AVERAGE SESSION TIME VS. " + y_name + ":", corr)
    print("P-VALUE (TWO-TAILED):", spearman_p)

    # plot
    plt.figure(1)
    b, m = polyfit(x, y, 1)
    plt.plot(x[:20], y[:20], '.', color='blue')
    plt.plot(x[20:], y[20:], '.', color='orange')
    plt.plot(x, b + m * x, '-')

    plt.xlabel('Average Session Time (seconds)')
    plt.ylabel(y_name)
    plt.title(y_name + ' vs. Average Session Time (seconds)')

    plt.legend(handles=[expert_patch, novice_patch])

    plt.show()


def get_xp_correlation(y, y_name):
    conn = mysql.connector.connect(user='root',
                                   host='127.0.0.1',
                                   database='mydb2',
                                   autocommit=True)  # TODO: change to 'mydb' when not testing
    cur = conn.cursor()

    my_query = """
    SELECT participants.participant_id,
           participants.programming_xp,
           participants.python_xp,
           participants.professional_xp
    FROM participants
    """
    cur.execute(my_query)
    results = cur.fetchall()

    participant_ids = [i for i in range(1, num_participants + 1)]
    programming_xp = [0 for k in range(num_participants)]
    python_xp = [0 for k in range(num_participants)]
    # only want to include professional developers in this analysis
    professional_xp = [0 for k in range(20)]

    for r in results:
        # r is a tuple where
        # r[0] = participant_id
        # r[1] = programming_xp
        # r[2] = python_xp
        # r[3] = professional_xp
        programming_xp[r[0]-1] = r[1]
        python_xp[r[0]-1] = r[2]
        if r[0] <= 20:
            professional_xp[r[0]-1] = r[3]

    x_programming = np.asarray(programming_xp)
    x_python = np.asarray(python_xp)
    x_professional = np.asarray(professional_xp)[:20]

    corr_programming, spearman_p_programming = spearmanr(x_programming, y)
    corr_python, spearman_p_python = spearmanr(x_python, y)
    corr_professional, spearman_p_professional = spearmanr(
        x_professional, y[:20])

    print("SPEARMAN'S R FOR PROGRAMMING XP VS. " +
          y_name + ":", corr_programming)
    print("P-VALUE (TWO-TAILED):", spearman_p_programming)
    print("-*" * 40)
    print("SPEARMAN'S R FOR PYTHON XP VS. " + y_name + ":", corr_python)
    print("P-VALUE (TWO-TAILED):", spearman_p_python)
    print("-*" * 40)
    print("SPEARMAN'S R FOR PROFESSIONAL XP VS. " +
          y_name + ":", corr_professional)
    print("P-VALUE (TWO-TAILED):", spearman_p_professional)

    # programming plot
    plt.figure(1)
    b, m = polyfit(x_programming, y, 1)

    novice_programming = []
    novice_python = []
    novice_y = []
    for p_id in novices:
        novice_programming.append(x_programming[p_id-1])
        novice_python.append(x_python[p_id-1])
        novice_y.append(y[p_id-1])

    middle_programming = []
    middle_python = []
    middle_y = []
    for p_id in middle:
        middle_programming.append(x_programming[p_id-1])
        middle_python.append(x_python[p_id-1])
        middle_y.append(y[p_id-1])

    expert_programming = []
    expert_python = []
    expert_y = []
    for p_id in experts:
        expert_programming.append(x_programming[p_id-1])
        expert_python.append(x_python[p_id-1])
        expert_y.append(y[p_id-1])

    # plt.plot(x_programming[:20], y[:20], '.', color='blue')
    # plt.plot(x_programming[20:], y[20:], '.', color='orange')
    plt.plot(novice_programming[:20], novice_y[:20], '.', color='orange')
    plt.plot(middle_programming[:20], middle_y[:20], '.', color='purple')
    plt.plot(expert_programming[:20], expert_y[:20], '.', color='blue')
    plt.plot(x_programming, b + m * x_programming, '-')

    plt.xlabel('Programming Experience (years)')
    plt.ylabel(y_name)
    plt.title(y_name + ' vs. Programming Experience')
    plt.legend(handles=[expert_patch, middle_patch, novice_patch])

    # python plot
    plt.figure(2)
    b, m = polyfit(x_python, y, 1)
    # plt.plot(x_python[:20], y[:20], '.', color='blue')
    # plt.plot(x_python[20:], y[20:], '.', color='orange')
    plt.plot(novice_python[:20], novice_y[:20], '.', color='orange')
    plt.plot(middle_python[:20], middle_y[:20], '.', color='purple')
    plt.plot(expert_python[:20], expert_y[:20], '.', color='blue')
    plt.plot(x_python, b + m * x_python, '-')

    plt.xlabel('Python Experience (years)')
    plt.ylabel(y_name)
    plt.title(y_name + ' vs. Python Experience')
    plt.legend(handles=[expert_patch, middle_patch, novice_patch])

    # professional plot
    plt.figure(3)
    b, m = polyfit(x_professional, y[:20], 1)
    plt.plot(x_professional, y[:20], '.', color='blue')
    # plt.plot(x_professional[20:], y[20:], '.', color='orange')
    plt.plot(x_professional, b + m * x_professional, '-')

    plt.xlabel('Professional Experience (years)')
    plt.ylabel(y_name)
    plt.title(y_name + ' vs. Professional Experience')
    plt.legend(handles=[expert_patch, novice_patch])

    plt.show()


def chi_test(df, ind: str, cols: list):
    '''Perform chi-square contingency test with cols and XP group.'''
    display(pd.crosstab(index=df[ind], columns=cols))

    chi2, p, dof, exp = chi2_contingency(
        pd.crosstab(index=df[ind], columns=cols))

    # initialize list of lists
    data = [['chi-square statistic', chi2],
            ['p-value', p],
            ['degrees of freedom', dof]]

    # Create and display the pandas DataFrame
    chi_results = pd.DataFrame(data, columns=['name', 'value'])
    chi_results.set_index('name')
    display(chi_results)

    # calculate residuals
    print("Pearson residuals")
    sm_table = sm.stats.Table(pd.crosstab(index=df[ind], columns=cols))
    display(sm_table.resid_pearson)

    # calculate residuals
    print("Standardized residuals")
    sm_table = sm.stats.Table(pd.crosstab(index=df[ind], columns=cols))
    display(sm_table.standardized_resids)

    print("Chi2 Contributions")
    display(sm_table.chi2_contribs)


def anova_xp_level(df, col: str):
    fvalue, pvalue = stats.f_oneway(df[col][df['xp_level'] == 'Expert'],
                                    df[col][df['xp_level'] == 'Python Novice'],
                                    df[col][df['xp_level'] == 'True Novice'])
    print("ANOVA f-value:", fvalue)
    print("ANOVA p-value:", pvalue)


def check_normality(df, outcome_variable: str, independent_variable: str):
    """Check assumption of normality for ANOVA"""
    model = ols('{} ~ C({})'.format(outcome_variable, independent_variable),
                data=df).fit()

    wteststat, pvalue = stats.shapiro(model.resid)
    print(color.bold("W-test statistic:"), wteststat)
    print(color.bold("p-value for normality:"), pvalue)

    if pvalue < 0.05:
        print(color.RED + 'WARNING: ' + outcome_variable +
              ' fails normality assumption' + color.END)


def check_homogeneity_xp(df, outcome_variable: str):
    # Independent variable is XP level for this check
    print(stats.levene(df[outcome_variable][df['xp_level'] == 'Expert'],
                       df[outcome_variable][df['xp_level'] == 'Python Novice'],
                       df[outcome_variable][df['xp_level'] == 'True Novice']))

    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111)

    ax.set_title("Box Plot of " + outcome_variable +
                 " by Experience", fontsize=20)
    ax.set

    data = [df[outcome_variable][df['xp_level'] == 'Expert'],
            df[outcome_variable][df['xp_level'] == 'Python Novice'],
            df[outcome_variable][df['xp_level'] == 'True Novice']]

    ax.boxplot(data,
               labels=['Expert', 'Python Novice', 'True Novice'],
               showmeans=True)

    plt.xlabel("Experience Level")
    plt.ylabel(outcome_variable)

    plt.show()
