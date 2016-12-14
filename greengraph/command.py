from argparse import ArgumentParser
import greengraph
import matplotlib.pyplot as plt

def process():
   parser = ArgumentParser(description = "Generate a graph that shows \
                    the amount of green pixels between two locations. ")
   parser.add_argument('--frm', '-f', required=True)
   parser.add_argument('--to', '-t', required=True)
   parser.add_argument('--steps', '-s', required=True)
   parser.add_argument('--out', '-o', required=True)
   arguments = parser.parse_args()

   mygraph = greengraph.Greengraph(arguments.frm ,arguments.to)
   data = mygraph.green_between(arguments.steps)
   plt.plot(data)
   plt.savefig(arguments.out)

if __name__ == "__main__":
    process()
