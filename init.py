"""
Made by potat#1735 / potat7163
Usage: python [src_file] <input_workbook:required(.xlsx)> <input_sheet:optional>
"""

import sys # for argv, stderr
# import os
import pandas as pd # for pd.DataFrame methods
import numpy as np # for np.nan, np.unique()

class ErrCodes : 
    INPUT_READ_FAILURE = -1
    INPUT_READ_SUCCESS = 0
    # PERMS_ERROR = 1
err_codes = ErrCodes()

"""
* Parse the dataframe and print statistics to stdout.
*
* Parameters:
* @df (required): The dataframe to parse. Should have at least the following columns:
*     - Map, Zombie, Rank, Kills, Deaths, Tied
*
* Returns:
* ErrCodes.INPUT_READ_SUCCESS if the @df was parsed successfuly
* ErrCodes.INPUT_READ_FAILURE otherwise
"""
def print_stats(df: pd.DataFrame) -> int : 
    # I hope the number of prints here made you puke.
    try : 
        total_games: int = df["Date"].count()
        print(f"Read data from {total_games} games")

        print(f"--- Game Data ---")
        zombie_ct: int = df["Zombie"].sum()
        human_ct: int = total_games*3 - zombie_ct
        print(f"Human:      {human_ct}      (average {human_ct/total_games:.2f})")
        print(f"Zombie:     {zombie_ct}     (average {zombie_ct/total_games:.2f})")
        for i in range(4) :
            zombie_df = df.loc[df["Zombie"] == i]
            print(f"   {i}Z ({3-i}H):    {zombie_df['Zombie'].count()} ({zombie_df['Zombie'].count()/total_games:.3f}%) \
                K/D: {zombie_df['Kills'].mean():.2f}/{zombie_df['Deaths'].mean():.2f} = {zombie_df['Kills'].sum()/zombie_df['Deaths'].sum():.2f} \
                ")
        kills: pd.Series = df["Kills"]
        deaths: pd.Series = df["Deaths"]
        print(f"Kills:      {kills.sum()}   (average {kills.mean():.2f})")
        print(f"Deaths:     {deaths.sum()}  (average {deaths.mean():.2f})")
        print(f"K/D:        {kills.sum()/deaths.sum():.2f}")

        print(f"----------")
        kill_record = df.iloc[df['Kills'].idxmax()]
        death_record = df.iloc[df['Deaths'].idxmax()]
        print(f"Kill Record:    {kill_record['Map']} K/D: {kill_record['Kills']}/{kill_record['Deaths']} = {kill_record['Kills']/kill_record['Deaths']:.2f}")
        print(f"Death Record:   {death_record['Map']} K/D: {death_record['Kills']}/{death_record['Deaths']} = {death_record['Kills']/death_record['Deaths']:.2f}")
        print(f"----------")

        print("Rank Info")
        over3_ct: int = 0
        for i in range(3) : 
            rank_ct: int = df.loc[df["Rank"] == i+1]["Rank"].count()
            print(f"{i}:    {rank_ct} ({rank_ct/total_games*100:.2f}%)")
            over3_ct += rank_ct
        print(f"Sub 3: {total_games - over3_ct} ({(total_games - over3_ct)/total_games*100:.2f}%)")
        print(f"Avg. Rank:  {df['Rank'].mean():.2f}")
        tied_games: int = df.loc[df["Tied"]]["Tied"].count()
        print(f"Tied games: {tied_games} ({tied_games/total_games*100:.2f}%)")

        print("--- Map-wise Data ---")
        print("----------")
        for map in np.unique(df["Map"].values) :
            map_df: pd.Series = df.loc[df["Map"] == map]
            map_ct: int = map_df["Map"].count()
            zombie_ct = map_df["Zombie"].sum()
            human_ct: int = 3*map_ct - zombie_ct
            print(f"{map}:  {map_ct} ({map_ct/total_games*100:.2f}%)")
            print(f"Human:  {human_ct} (average {human_ct/map_ct:.2f})")
            print(f"Zombie: {map_df['Zombie'].sum()} (average {map_df['Zombie'].mean():.2f})")
            for i in range(4) :
                zombie_df = map_df.loc[df["Zombie"] == i]
                print(f"   {i}Z ({3-i}H):    {zombie_df['Zombie'].count()} ({zombie_df['Zombie'].count()/total_games:.3f}%) \
                    K/D: {zombie_df['Kills'].mean():.2f}/{zombie_df['Deaths'].mean():.2f} = {zombie_df['Kills'].sum()/zombie_df['Deaths'].sum():.2f} \
                    ")
            kills: pd.Series = map_df['Kills']
            deaths: pd.Series = map_df['Deaths']
            print(f"Kills:  {kills.sum()} (average {map_df['Kills'].mean():.2f})")
            print(f"Deaths: {deaths.sum()} (average {deaths.mean():.2f})")
            print(f"K/D:    {kills.sum()/deaths.sum():.2f}")
            print("----------")

        return err_codes.INPUT_READ_SUCCESS
    except : 
        return err_codes.INPUT_READ_FAILURE 

"""
* Read the Excel worksheet supplied by @ifile and @sname.
*
* Parameters:
* @ifile (required): Path to the Excel file to read
* @sname (optional): Name of the worksheet to read from @ifile
*   - If @sname is None, the first worksheet in @ifile is read
*
* Returns:
* pd.DataFrame containing the data stored in the worksheet
"""
def get_df(ifile:str, sname:str=None) -> pd.DataFrame :
    return pd.read_excel(ifile, sheet_name=sname) if sname else pd.read_excel(ifile)

def main(argv:list[str]) -> int :
    # Yeah this is dirty and bad boohoo cry me a river.
    # Print the stats, process any errors that occur.
    if (print_stats(get_df(argv[0])) if len(argv)<2 else print_stats(get_df(argv[0], argv[1]))) < err_codes.INPUT_READ_SUCCESS : 
        print("Error: Could not read input file (maybe you forgot the worksheet name?)", file=sys.stderr)

    # o_file = f"outputs/{os.path.splitext(arg)[0]}.txt"
    
    return 0

if __name__ == "__main__":
    main(sys.argv[1:])