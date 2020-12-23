import pandas as pd
from fuzzywuzzy import process, fuzz

def username(df, first_name, last_name, email):

    df.dropna()

    #make names lowercase and remove spaces
    df[first_name] = df[first_name].str.lower()
    df[last_name] = df[last_name].str.lower()
    df[first_name] = df[first_name].str.replace(' ', '')
    df[last_name] = df[last_name].str.replace(' ', '')
    #get initials
    df['first_initial'] = df[first_name].astype(str).str[0]
    df['last_initial'] = df[last_name].astype(str).str[0]
    #seperate username and domain
    df['username'] = df[email].str.split("@").str[0]
    df['domain'] = df[email].str.split("@").str[1]

    df = df.astype(str)

    codes = []

    for index, row in df.iterrows():

        positions = []

        positions.append(row['username'].find(row[first_name])+1)
        positions.append(row['username'].find(row[last_name])+1)

        #if first name exists in username, make first initial 0
        if positions[0] == 0:
            positions.append(row['username'].find(row['first_initial'])+1)
        else:
            positions.append(0)

        if positions[1] == 0:
            positions.append(row['username'].find(row['last_initial'])+1)
        else:
            positions.append(0)

        positions.append(row['username'].find('.')+1)
        positions.append(row['username'].find('_')+1)

        #rank positions so that largest number is 3

        positions = pd.DataFrame({
            'position' : positions
        })

        positions['rank'] = (positions['position'].rank(method="dense")-1).astype(int)

        positions = positions['rank'].tolist()

        # if number chars in username is greater than # chars in what makes up username (e.g., first & last name), make code '000000' 
        #This means unknown chars exist

        count = 0

        if positions[0]>0:
            count +=len(row[first_name])
        if positions[1]>0:
            count +=len(row[last_name])
        if positions[2]>0:
            count +=1
        if positions[3]>0:
            count +=1
        if positions[4]>0:
            count +=1
        if positions[5]>0:
            count +=1

        if len(row['username']) > count:
            codes.append('000000')
        else:
            codes.append(''.join(map(str, positions)))

    df['syntax'] = codes
    
    return df

def domain(df, co_name, email, contacts=5, domain_pct=80, co_domain_match_pct=60):
    
    #Parse domain from email
    df['domain'] = df[email].str.split("@").str[1]
    
    #Create a new column that indicates the number of contacts (rows) per company
    df['contacts'] = df[co_name].map(df[co_name].value_counts())

    #Group rows by company name and count the number of rows with each domain
    df = df.groupby([co_name, 'domain', 'contacts']).size().reset_index(name='domain_count')
    df['domain_count'] = df['domain_count'].astype(float)
    
    #Take percentage of number of contacts with a domain to total number of contacts in each company
    df['domain_pct'] = round((df['domain_count']/df['contacts'])*100,0)
    
    #Keep the domain with the maximum percent for each company
    df = df.sort_values('domain_pct', ascending=False).drop_duplicates(co_name).sort_index()
    
    #Calcualte the percent match between company name and domain
    df['co_domain_match_pct'] = df.apply(lambda x: fuzz.ratio(x[co_name].lower().replace(" ", ""), x['domain'].rsplit('.')[0]), axis=1).astype(float)
    
    #Create a new column that indicates if the domain is unique to the company
    df['unique'] = df['domain'].map(df['domain'].value_counts())
    df.loc[df['unique']>1, 'unique'] = 0
    
    #Load dataframe with free email domains (e.g., gmail.com, aol.com)
    free_domains = pd.read_csv('../Recruitment Pipeline/free_domains.csv',encoding = "ISO-8859-1")
    
    #Create a new column that indiactes if a company domain matches a free email domain
    df['free_domain'] = 0
    df.loc[df['domain'].isin(free_domains['domain']), 'free_domain'] = 1
    
    #Create a column called 'doubt' to indicate if their is doubt about a company domain being correct.
    df['doubt'] = 1
    
    #doubt = 0 if:
    # - The company has X number of contacts and the percent of contacts with the domain is greater than X OR
    # - The company name and domain match by more than X% AND
    # - The domain is not a free email domain AND
    # - The domain is unique

    df.loc[(((df['contacts']>contacts)&(df['domain_pct']>domain_pct))|(df['co_domain_match_pct']>co_domain_match_pct))&(df['free_domain']==0)&(df['unique']==1), 'doubt'] = 0
    
    return df
