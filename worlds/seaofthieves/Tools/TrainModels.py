import os
import subprocess

class CommandFiles:

    def __init__(self, pos_file = "", neg_file = "", sample_out_file = "", training_out_file =""):
        self.pos_file = pos_file
        self.neg_file = neg_file
        self.sample_output_file = sample_out_file
        self.training_output_file = training_out_file
class TrainingCommand:

    def __init__(self):
        self.samples_command: str = ""
        self.train_command: str = ""
        self.commandfiles = None
        self.width: int = 24
        self.height = 24
        self.num = 1000


def main():

    commandFiles = [
        CommandFiles("samples\\banana_positive", "samples/banana_negatvies", "vectors/banana_pos.vec", "cascade/banana/"),
        CommandFiles("samples\\coconut_positive", "samples/coconut_negatvies", "vectors/coconut_pos.vec", "cascade/coconut/"),
        CommandFiles("samples\\mango_positive", "samples/mango_negatvies", "vectors/mango_pos.vec", "cascade/mango/"),
        CommandFiles("samples\\pineapple_positive", "samples/pineapple_negatvies", "vectors/pineapple_pos.vec", "cascade/pineapple/"),
        #CommandFiles("samples\\pomegran_positive", "samples/pomegran_negatvies", "vectors/pomegran_pos.vec", "cascade/pomegran/"),
    ]
    trainingCommand = TrainingCommand()
    trainingCommand.samples_command = "C:\\Users\\Ethan\\Desktop\\open_cv\\3.14.16\\opencv\\build\\x64\\vc15\\bin\\opencv_createsamples.exe"
    trainingCommand.train_command = "C:\\Users\\Ethan\\Desktop\\open_cv\\3.14.16\\opencv\\build\\x64\\vc15\\bin\\opencv_traincascade.exe"


    #create samples
    for commandFile in commandFiles:
        trainingCommand.commandfiles = commandFile

        w = 24
        h = 24
        stages = 6
        print(os.getcwd())


        print(os.path.isfile(commandFile.neg_file))
        #make samples
        subprocess.run([trainingCommand.samples_command, "-info", trainingCommand.commandfiles.pos_file, "-w", str(w), "-h", str(h), "-num", str(100), "-vec", trainingCommand.commandfiles.sample_output_file])

        #train model
        subprocess.run([trainingCommand.train_command, "-data", trainingCommand.commandfiles.training_output_file, "-vec", trainingCommand.commandfiles.sample_output_file, "-bg", trainingCommand.commandfiles.neg_file, "-w", str(w), "-h", str(h), "-numPos", str(28), "numNeg", str(60), "-numStages", str(stages)])


#C:\Users\Ethan\Desktop\open_cv\3.14.16\opencv\build\x64\vc15\bin\opencv_createsamples.exe -info coconut_positive -w 24 -h 24 -num 1000 -vec coconut_pos.vec


#C:\Users\Ethan\Desktop\open_cv\3.14.16\opencv\build\x64\vc15\bin\opencv_traincascade.exe -data cascade/coconut/ -vec coconut_pos.vec -bg coconut_negatvies -w 24 -h 24 -numPos 28 -numNeg 60 -numStages 3


main()