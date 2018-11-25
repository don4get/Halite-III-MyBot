from os import listdir
import subprocess


def extract_map(filename):
    # Open file and read the map
    file = open(filename)

    map = []
    width = 0
    for i, line in enumerate(file):
        if i == 4:
            size = [int(num) for num in line.split()]
            width = size[0]
        if i > 4 and i <= 4 + width:
            map.append([int(num) for num in line.split()])
    file.close()
    return map

ext = '.hlt'
files = [file for file in listdir('./replays') if ext in file]

output_files = []
for input_file in files:
    temp = input_file.replace('replay-', '')
    output_file = temp.replace(ext, '.txt')
    output_files.append(output_file)
    bash_command = "./analysis/replay_decoder.py" \
                   + " -i " + "replays/" + input_file \
                   + " -o " + "replays/" + output_file \
                   + " -p 1"
    output = subprocess.check_output(['bash', '-c', bash_command])

for filename in output_files:
    game_map = extract_map("replays/"+filename)
    filename = filename.replace('.txt', '.csv')
    file = open("maps/"+filename, "w")
    for row in game_map:
        string = ','.join(str(col) for col in row)
        file.write("%s\n" % string)
    file.close()
