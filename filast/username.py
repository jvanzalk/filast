def syntax(df, first_name, last_name, email):

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