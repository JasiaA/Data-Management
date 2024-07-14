import pandas as pd
from groq import Groq
import sys

def scrape():
    """This scrape function sorts a small sales database into 3 categories 
    from a file called databigmart.csv located in the same directory"""

    # Imports dataset
    colnames = ['Item', 'sales'] 
    df = pd.read_csv("databigmart.csv", names=colnames, header=None)

    # Create three empty DataFrames for sorting
    high_sales = pd.DataFrame(columns=colnames)
    low_sales = pd.DataFrame(columns=colnames)
    mid_sales = pd.DataFrame(columns=colnames)

    # Iterate over each row in the dataset
    for index, row in df.iterrows():
        if row['sales'] > 8744.33: #change this number
            high_sales.loc[len(high_sales)] = row
        elif row['sales'] < 4355.63: #change this number
            low_sales.loc[len(low_sales)] = row
        else:
            mid_sales.loc[len(mid_sales)] = row

    # Redirect stdout to a file
    original_stdout = sys.stdout
    with open('sales.txt', 'w') as f:
        sys.stdout = f
        # Print each category
        print("High sales")
        print(high_sales)
        print("Mid sales")
        print(mid_sales)
        print("Low sales")
        print(low_sales)
        # Restore stdout
        sys.stdout = original_stdout

    return None
#print the results
print(scrape.__doc__)
scrape()

# Opens 'api.txt' file that contains the api key
with open('api.txt') as f:
    api_key = f.read()
client = Groq(api_key=api_key)
#use of groq API below
with open('sales.txt') as g:
    file_contents= g.read()
    completion = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[
            {
                "role": "user",
                "content": f"Take in the list of items given in sales.txt, tell me the number of sales each item has, give me a description for each of the items, and give me a possible reason as to why it may have that number of sales and do that for the set of items with high sales, low sales, and mid sales: {file_contents}" 
            }
        ],
        temperature=1,
        max_tokens=2048,
        top_p=1,
        stream=True,
        stop=None,
    )

# Iterate over the completion chunks and print the generated descriptions

for chunk in completion:
    print(chunk.choices[0].delta.content or "", end="")