import pandas as pd

def city_data_compile():
    '''
    
    '''
    data = pd.read_csv('Numbeo_API_Data/cities.csv')
    data_US = data[data.country == 'United States']
    cities_US_list = data_US.city.tolist()
    city_df_dict={}
    final_cities_list=[]
    
    for index,city in enumerate(cities_US_list):
        try:
            current_df = pd.read_csv(f"Numbeo_API_Data/city_prices_final/{index}_prices.csv")
        except:
            continue
        
        if len(current_df) is 0:
            continue
        elif len(current_df) is not 55:
            continue
        else:
#            Separate columns for city, state and country
            if len(current_df['name'][0].split(', ')) is 3:
                current_df['city'], current_df['state'], current_df['country'] = current_df['name'].str.split(', ').str
            elif len(current_df['name'][0].split(', ')) is 2:
                current_df['city'], current_df['country'] = current_df['name'].str.split(', ').str
            current_df.drop(columns = ['Unnamed: 0','name'], inplace=True)
            
    #            Rearrange columns in the dataframe
            cols = list(current_df.columns)
            cols = cols[-3:] + cols[:-3]
            current_df = current_df[cols]
        
#            city_df_dict[f"{index}"] = current_df
    
#    df_cols = list(list(city_df_dict.values())[0].columns)
#    list_df = list(city_df_dict.values())
#    total_df = len(city_df_dict)
#    final_df= pd.DataFrame(columns=df_cols)  
    
#    final_df = pd.concat(city_df_dict, axis=0, ignore_index=True, sort=False)
##    for i in range(total_df):
##        final_df = final_df.append(list_df[i], ignore_index=True)
#    final_cities_list = list(city_df_dict.keys())
            city_state_all = current_df['city'].str.cat(current_df['state'], sep=', ')
            city_state = city_state_all.unique()
            final_cities_list.append(city_state[0])
    
#    final_df.to_csv('Numbeo_API_Data/compiled_city_data_final.csv')
    with open('Numbeo_API_Data/final_city_state.txt','w') as f:
        f.write("\n".join(final_cities_list))
    return
    