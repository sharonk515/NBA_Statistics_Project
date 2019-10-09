import statsmodels.api as sm
import scipy.stats as stats
import itertools

def conduct_pairedttest(df, column1, column2):
    """
    Paired T-test on two samples of scores: column1 and column2 of DataFrame (df).
    Analyzes the significance of differences in scores of East and West conference teams.

    This is a two-sided test for the null hypothesis that 2 related or
    repeated samples have identical average (expected) values.

    alpha = 0.05
    
    Parameters
    ----------
    df: DataFrame name
    column1: column name for first sample
    column2: column name for second sample
    
    Returns
    -------
    Difference in means, t-value, p-value
    Whether null hypothesis is accepted or rejected

    """
    # Perform paired t-test
    ttest = stats.ttest_rel(df[column1], df[column2])

    # Print results using the test statistic and p-value
    print("Given our null hypothesis (the difference in means is 0),")
    print(f"the probability that our actual diference in means of {round(df[column1].mean() - df[column2].mean(), 2)}")
    print(f"is {round(ttest.statistic, 2)} standard deviations away is {round(ttest.pvalue, 2)}.")
    print(f"Therefore we can {'NOT'*(ttest.pvalue > .05)} reject the null hypothesis.")


def conduct_anova(df, team_names, team_scores):
    """
    Conducts the ANOVA test and Independent T-tests to analyze
    the significance of differences in scores of teams
    when playing games at their home courts.

    alpha = 0.05
    
    Parameters
    ----------
    df: DataFrame name
    team_names: column name with team names
    team_scores: column name with score differences
    
    Returns
    -------
    Difference in means, t-value, p-value
    Whether null hypothesis is accepted or rejected

    """
    ftest = stats.f_oneway(*(df[df[team_names] == team][team_scores]
                             for team in df[team_names].unique()))
    print("F: ", round(ftest.statistic, 2))
    print("p-value: ", round(ftest.pvalue, 6))
    if ftest.pvalue < 0.05:
        print("At least 1 team's home court advantage is statistically significant \n")
       # Create an empty dictionary that will store results
        ttest_dict = {}
       # Creating all possible combinations of teams and iterating through
        for pair in list(itertools.combinations(df[team_names].unique(), 2)):
           # Designating 1st list of values for ttest
            first_team_vals = df[df[team_names] == pair[0]][team_scores]
           # Designating 2nd list of values for ttest
            second_team_vals = df[df[team_names] == pair[1]][team_scores]
           # Perform ttest
            ttest = stats.ttest_ind(first_team_vals, second_team_vals)
           #Create key-values for initial dictionary
           # Only include 'significant' results
            if ttest.pvalue < 0.05:
                ttest_dict[pair] = [round(ttest.statistic, 2), round(ttest.pvalue, 6)]
                print(f"{pair[0]}'s home court advantage is statistically significantly")
                print(f"{' better'*(ttest.statistic>0)}{' worse'*(ttest.statistic<0)} than")
                print(f"{pair[1]}'s (t-stat: {round(ttest.statistic, 2)}, p-value: {round(ttest.pvalue, 4)})")
    else:
        print("No team's home court advantage is statistically significant")
