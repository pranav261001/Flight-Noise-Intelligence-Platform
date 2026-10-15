# print(min(3,4))

# import pandas as pd

# df = pd.DataFrame({
#     'Name': ['Alice', 'Bob'],
#     'Age': [25, 30]
# })

# dicto = [ ]

# for index, row in df.iterrows():
#     demo = row["Name"]
#     dicto.append(demo)


# print(dicto)

keys = ['name', 'age', 'city']
values = ['John', 25, 'New York', 'John', 25, 'New York', ]

# Using the zip function to pair up keys 
#and values
my_dict = {key: value for key, 
           value in zip(keys, values)}

# Print the resulting dictionary
print(my_dict)

d1 = [{
    "icao": 'abc123', "icato": "hdiud" 
    ,"cate": 'def456'
}, {"icao": 'abc123'}]
import pandas as pd

data = pd.DataFrame(d1)
print(data.head())