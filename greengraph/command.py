from argparse import ArgumentParser
import greengraph
import matplotlib.pyplot as plt

def process():
   parser = ArgumentParser(description = "Generate a graph that shows \
                    the amount of green pixels between two locations. ")
   parser.add_argument('--frm', '-f')
   parser.add_argument('--to', '-t')
   parser.add_argument('--steps', '-s')
   #parser.add_argument('--out', 'o')
   arguments = parser.parse_args()

   mygraph = greengraph.Greengraph(arguments.frm ,arguments.to)
   data = mygraph.green_between(arguments.steps)
   plt.plot(data)
   plt.show()

if __name__ == "__main__":
    process()
