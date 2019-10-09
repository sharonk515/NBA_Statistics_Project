import seaborn as sns
import matplotlib.pyplot as plt


def desc_stats(df):
    """
    Creates a table of descriptive statistics for numerical variables of DataFrame.
    
    Parameters
    ----------
    df: DataFrame name
        Specify columns with df[[columns]].
    
    Returns
    -------
    Outputs a table of summary statistics
    
    """    
   # If you want specific columns, specify with df[[columns]]
    return df.describe()


def make_box_plot(data1, data2, image_name):
    """
    Creates two boxplots in one figure space and save as a png file
    
    Parameters
    ----------
    data1: DataFrame for the first boxplot
        Specify columns by data1[[column names]]
    data2: DataFrame for the second boxplot
        Specify columns by data2[[column names]]
    image_name: Desired filename for the saved image
    
    Returns
    -------
    Outputs a saved png file and returns a box plot

    """
    # Create a figure space and define subplots
    fig, axes = plt.subplots(2, 1, figsize=(7.5, 8))
    # Set first subplot
    box1 = sns.boxplot(data=data1,
                       orient='h',
                       ax=axes[0])
    box1.set(xlabel="number of points",
             title=f"{image_name.capitalize().replace('_', ' ')}")
    
    # Define second subplot
    box2 = sns.boxplot(data=data2,
                       orient="h",
                       ax=axes[1],
                       color='g')
    box2.set_xlabel("number of points");
    
    # exporting the image to the img folder
    plt.savefig(f'img/{image_name}.png',
                figure=fig,
               bbox_inches="tight")


def make_density_plot(df, col, image_name):
    """
    Create density plot and save as a png file
    
    Parameters
    ----------
    df: DataFrame name
    col: Column name
    image_name: Desired filename for the saved image
    
    Returns
    -------
    Outputs a saved png file and returns a density plot for testing

    """
    x = sns.distplot(df[col])
    x.set_title(image_name.capitalize().replace("_"," "))
    plt.savefig(f"img/{image_name}.png", bbox_inches="tight")


def make_ordered_boxplot(df, groupby_col, agg_col, image_name):
    """
    Create a boxplot that is sorted by group averages in descending order
    and save as a png file
    
    Parameters
    ----------
    df: DataFrame name
    groupby_col: Column by which DataFrame is grouped
    agg_col: Column to calculate mean
    image_name: Desired filename for the saved image
    
    Returns
    -------
    Outputs a saved png file and returns a box plot for testing

    """
    my_order = df.groupby(groupby_col)[agg_col].mean().sort_values(ascending=False).index
    # Create boxplot and add ordering
    ax = sns.boxplot(x=agg_col, y=groupby_col, data=df, order=my_order)
    # Make labels and title
    ax.set_title(image_name.capitalize().replace("_"," "))
    plt.savefig(f"img/{image_name}.png", bbox_inches="tight")
