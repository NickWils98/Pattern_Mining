import pandas as pd
from apyori import apriori

def inspect(results):
    """
    make the data visual
    :param results: results of apriori
    :return: visual representation of data
    """
    lhs     =  [tuple(result [2] [0] [0]) [0] for result in results]
    rhs     =  [tuple(result [2] [0] [1]) [0] for result in results]
    supports = [result [1] for result in results]
    confidences = [result [2] [0] [2]   for result in results]
    lifts = [result [2] [0] [3]   for result in results]
    return list(zip(lhs,rhs,supports,confidences, lifts))

def reedDB(filename):
    """
    read the database
    :param filename: string
    :return: pandas framework
    """
    dataset = pd.read_csv(filename)
    return dataset

def getBasketsSes_id(dataset):
    """
    get baskets from dataset
    :param dataset: pandas dataset
    :return: list
    """
    return dataset.groupby("user_session").product_id.apply(set).tolist()

def getBasketsUser_id(dataset):
    """
    get baskets from dataset
    :param dataset: pandas dataset
    :return: list
    """
    return dataset.groupby("user_id").product_id.apply(set).tolist()

def preformApriori(transactions, min_support=0.1, min_confidence=0.2, min_lift=1.2, min_length=2):
    """
    preform apriori
    :param transactions:
    :param min_support: float
    :param min_confidence: float
    :param min_lift: float
    :param min_length: int
    :return: generator
    """
    rules = apriori(transactions, min_support=min_support, min_confidence=min_confidence, min_lift=min_lift, min_length=min_length)
    results = list(rules)
    return results

def printTop10(df):
    """
    print top 10
    :param df: pandas dataframe
    :return: None
    """
    print(df.head(10))

def reformDB(df):
    """
    get baskets from dataframe with all data
    :param df: dataframe pandas
    :return: list
    """


    boughtDf= df[df.event_type == 'purchase']
    boughtDf['product_id'] = 'purchase-' + boughtDf['product_id'].astype(str)
    boughtDf['product_id'] = boughtDf['product_id'].astype(str)
    boughtbasket =boughtDf.groupby("user_session").product_id.apply(set).tolist()
    total = boughtbasket

    viewDf= df[df.event_type == 'view']
    viewDf['product_id'] = 'view-' + viewDf['product_id'].astype(str)
    viewDf['product_id'] = viewDf['product_id'].astype(str)
    viewbasket =viewDf.groupby("user_session").product_id.apply(set).tolist()
    total += viewbasket

    brandsDf = df
    brandsDf = brandsDf[brandsDf.event_type == 'view']
    brandsDf['brand'] = "brand-" + brandsDf['brand']
    brandsDf['brand'] = brandsDf['brand'].astype(str)

    brandbasket =brandsDf.groupby("user_id").brand.apply(set).tolist()
    total += brandbasket

    catagoriesDf = df
    catagoriesDf = catagoriesDf[catagoriesDf.event_type == 'view']
    catagoriesDf['category_id'] = catagoriesDf['category_id'].astype(str)
    catagoriesDf['category_id'] = catagoriesDf['category_id'].astype(str)
    catagoriesbasket =catagoriesDf.groupby("user_id").category_id.apply(set).tolist()
    total += catagoriesbasket

    for i, e in reversed(list(enumerate(total))):
        if 'nan' in total[i]:
            total.pop(i)

    return total

if __name__ == '__main__':
    #################" RUN ####################"

    # Load the dataset as a pandas DataFrame
    dataset = reedDB("dataset.csv")
    # Convert the dataset to baskets (a list of sets)
    transactions = getBasketsUser_id(dataset)

    results = preformApriori(transactions, 0.0004, 0.2, 1.2, 2)

    # putting output into a pandas dataframe
    resultsinDataFrame = pd.DataFrame(inspect(results),
                                      columns=['Left Hand Side', 'Right Hand Side', 'Support', 'Confidence', 'Lift'])
    ordered = resultsinDataFrame.sort_values(by="Support", ascending=False)
    printTop10(ordered)

    #################" RUN ALTERNATIVE ####################"
    dataset = reedDB("dataset.csv")
    transactions = reformDB(dataset)
    results = preformApriori(transactions, 0.0004, 0.3, 1.2, 2)

    resultsinDataFrame = pd.DataFrame(inspect(results),
                                      columns=['Left Hand Side', 'Right Hand Side', 'Support', 'Confidence', 'Lift'])
    ordered = resultsinDataFrame.sort_values(by="Lift", ascending=False)
    printTop10(ordered)

