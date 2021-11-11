import getopt
import sys
import pandas as pd

def print_kd_report(game_data, num_games, ofile):
  ofile.write("---------- Performance Averages ----------\n")
  for i in range(0, 4):
    avg_kills = round((game_data[i][0] / game_data[i][-1]), 2)
    avg_deaths = round((game_data[i][1] / game_data[i][-1]), 2)
    avg_rank = round((game_data[i][2] / game_data[i][-1]), 2)
    percentage = round(((game_data[i][-1] / num_games) * 100), 2)
    ofile.write(f"{i}-time zombie averages ({game_data[i][-1]} games -> {percentage}%):\n\tKills: {avg_kills}\n\tDeaths: {avg_deaths}\n\tK/D: {round(avg_kills/avg_deaths, 2)}\n\tRank: {avg_rank}\n")

def generate_reports(ifile, ofile):
  ##### Averages #####
  df = pd.read_excel(ifile)
  df["Date"] = pd.to_datetime(df["Date"]).dt.date
  print(f"Reading data for {df.shape[0]} games from {df['Date'][0]} to {df['Date'][df['Date'].shape[0] - 1]}...")
  

  game_data = [[0, 0, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0]]
  map_count_dict = {}
  map_perf_dict = {}

  for i in range(0, df.shape[0]):
    try:
      game_data[int(df["Zombie"][i])][0] += df["Kills"][i]
      game_data[int(df["Zombie"][i])][1] += df["Deaths"][i]
      game_data[int(df["Zombie"][i])][2] += df["Rank"][i]
      game_data[int(df["Zombie"][i])][3] += 1
    except:
      pass

    try:
      map_count_dict[df["Map"][i]] += 1
    except:
      map_count_dict[df["Map"][i]] = 0
      map_count_dict[df["Map"][i]] += 1

    try:
      if df["Kills"][i] > map_perf_dict[df["Map"][i]][2]:
        map_perf_dict[df["Map"][i]] = [df["First Place"][i], df["Date"][i], df["Kills"][i], df["Deaths"][i]]
    except:
      map_perf_dict[df["Map"][i]] = [df["First Place"][i], df["Date"][i], df["Kills"][i], df["Deaths"][i]]

  print_kd_report(game_data, df.shape[0], ofile)

  ##### Map Statistics #####
  ofile.write("---------- Map Frequency Report ----------\n")
  for k, v in map_count_dict.items():
    ofile.write(f"{k}: {v} ({round((v / df.shape[0]) * 100, 2)}%)\n")

  ##### Best Performance #####
  ofile.write("---------- Map Frequency Report ----------\n")
  max_kill_row = df["Kills"].idxmax()
  ofile.write(f"Winner: {df['First Place'][max_kill_row]}\n")
  ofile.write(f"Date: {df['Date'][max_kill_row]}\n")
  ofile.write(f"Map: {df['Map'][max_kill_row]}\n")
  ofile.write(f"Kills: {df['Kills'][max_kill_row]}\n")
  ofile.write(f"Deaths: {df['Deaths'][max_kill_row]}\n")
  ofile.write(f"K/D: {round(df['Kills'][max_kill_row] / df['Deaths'][max_kill_row], 2)}\n")

  ##### Map-wise Best Performance #####
  ofile.write("---------- Map-wise Performance Report ----------\n")
  for k, v in map_perf_dict.items():
    ofile.write(f"Map: {k}\n")
    ofile.write(f"\tWinner: {v[0]}\n\tDate: {v[1]}\n\tKills: {v[2]}, Deaths: {v[3]}, K/D: {round(v[2] / v[3], 2)}\n")

  
def main(argv):
  inputfile = ''
  outputfile = ''
  try:
    opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
  except getopt.GetoptError:
    print("tracker.py -i <inputfile> -o <outputfile>")
    sys.exit(2)
  for opt, arg in opts:
    if opt == '-h':
      print("main.py -i <inputfile> -o <outputfile>")
      sys.exit()
    elif opt in ("-i", "--ifile"):
      inputfile = arg
    elif opt in ("-o", "--ofile"):
      outputfile = arg
      outputfile = open(outputfile, "w")
    elif opt in ("-t", "--target"):
      target = arg

  generate_reports(inputfile, outputfile)

  outputfile.close()
  print("Finished processing data and saved to output report file")

if __name__ == "__main__":
  main(sys.argv[1:])