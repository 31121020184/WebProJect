import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules

# pd.set_option('max_columns', None)
pd.set_option('display.max_columns', None)

# sữ dụng list để lưu danh sách các mục


data = pd.read_csv("D:/orders_orderitem.csv")
print(data.head())

df = data.iloc[:,3:]
print(df.head())

dataset = df.groupby('order_id')['product_id'].apply(list)
print(dataset)

te = TransactionEncoder()
te_ary = te.fit(dataset).transform(dataset)
df = pd.DataFrame(te_ary, columns=te.columns_)
print("Transactions:")
print(df)

print("Check null:")
print(df.isnull().any())

# dat ngương dua tren so transaction

frequent_itemsets = apriori(df, min_support=0.07, use_colnames = True)
print("Support:")
print(frequent_itemsets)

confidences = association_rules(frequent_itemsets, metric="confidence", min_threshold=0.5)
print("Confidence:")
print(confidences)

#rules
rules = association_rules(frequent_itemsets, metric="lift", min_threshold=1)
print("Lift:")
print(rules)
print(type(rules))
# rules.to_csv(r'E:\rules.csv', index=False)
rules.to_csv('rules.csv')

# Khi chon 2 thì nó kết hợp với item nào?
print("select '25' => which items go with it")
for index, row in rules.iterrows(): 
    # if 25 in row[1][0]:  
    if 27 in row.iloc[1]:
        print(list(row.iloc[1]))
        # print(list(row[1][1]))
