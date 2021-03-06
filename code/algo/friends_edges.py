import numpy as np
from matplotlib import pyplot as plt
import cPickle as pickle


def get_fig():
    # Create new Figure with black background
    plt.close()
    fig = plt.figure()
    fig.set_size_inches(15,15)

    # Add a subplot with no frame
    ax = plt.subplot(111, frameon=False)

    # Remove the plot frame lines. They are unnecessary chartjunk.  
    ax.spines["top"].set_visible(False)  
    ax.spines["right"].set_visible(False)  

    # Ensure that the axis ticks only show up on the bottom and left of the plot.  
    # Ticks on the right and top of the plot are generally unnecessary chartjunk.
    ax.get_xaxis().tick_bottom()

    return fig, ax

def dist_fig(df, friends, start=0, limit_high=400, filename="dd", bin_size=150):
    values = np.clip(df, start, limit_high)
    step = (limit_high-start)/float(bin_size)
    range_bins = np.arange(start=start, stop=limit_high+2*step, step=step)
    # hist_normed, bins = np.histogram(values, bins=1000, density=True)
    hist, bins = np.histogram(values, bins=range_bins, density=True)


    # hist_normed = step*hist_normed
    # print hist, sum(hist)
    # print hist_normed, sum(hist_normed)
    width = 1 * (bins[1] - bins[0])
    center = (bins[:-1] + bins[1:]) / 2

    # fig, ax = plt.subplots(figsize=(20, 14))

    fig, ax = get_fig()

    



    # ax.get_yaxis().set_visible(False)  

    # Along the same vein, make sure your axis labels are large  
    # enough to be easily read as well. Make them slightly larger  
    # than your axis tick labels so they stand out.  
    # xlabel("Elo Rating", fontsize=16)  
    # ylabel("Count", fontsize=16) 

    # Make sure your axis ticks are large enough to be easily read.  
    # You don't want your viewers squinting to read your plot.  
    # axyticks(fontsize=14)  
    # xticks(fontsize=14) 

    # Remove the tick marks; they are unnecessary with the tick lines we just plotted.  
    plt.tick_params(axis="both", which="both", bottom="off", top="off",  
                    labelbottom="on", left="off", right="off", labelleft="on")  

    # xticks(fontsize=14)  
    # x = [str(bins[i]) + '-' + str(bins[i+1]) for i in range(len(bins)-1)]
    # x = []
    # for i, j in zip(bins, bins[1:]):
    #     if j-i == 1:
    #         x.append(i)
    #     else:
    #         x.append("{0}-{1}".format(i, j))
        
    # # Display 100-200-300-400-500+ for books-users
    # # Display 1-2-3-4-5 for ratings
    # if plus:
    #     x[-1] = str(limit_high) + " +"

    # # add some text for labels, title and axes ticks
    # ax.set_xlabel(xlabels)
    # ax.set_ylabel(ylabels)
    # ax.set_title(title)
    # ax.set_xticks(center)
    # ax.set_xticklabels(x, fontsize=14, rotation=+45)
    # bars = plt.bar(center, hist, align='center', width=width, color="#3F5D7D")
    bars = plt.bar(center, hist, align='center', width=width, color="b")
    import random

    friends_max = [i for i in friends if i<limit_high]
    friends_random = random.sample(friends_max, 20)
    friends_height = [max(hist)] * len(friends_random)

    bars = plt.bar(friends_random, friends_height, align='center', width=width/3., color="r")


    # max_height = max(b.get_height() for b in bars)
    # # Lastly, write in the ranking inside each bar to aid in interpretation
    # for bar, val, val_normed in zip(bars, hist, hist_normed):
    #     # Rectangle widths are already integer-valued but are floating
    #     # type, so it helps to remove the trailing decimal point and 0 by
    #     # converting width to int type
    #     height = bar.get_height()

    #     # if (height < 0.05):        # The bars aren't wide enough to print the ranking inside
    #     if (height < 100):        # The bars aren't wide enough to print the ranking inside
    #         # yloc_normed = 1.0008 * height
    #         yloc = height + max_height*0.02   # Shift the text to the right side of the right edge
            
    #         clr = 'black'      # Black against white background
    #     else:
    #         yloc = height-max_height*0.03
    #         # yloc_normed = height*0.8
    #         # Shift the text to the left side of the right edge
    #         clr = 'white'      # White on magenta

    #     xloc = bar.get_x()+bar.get_width()/2.0
    # #     ax.text(xloc, yloc_normed, str(val), horizontalalignment='center', color=clr)
    #     ax.text(xloc, yloc, '{:.1%}'.format(val_normed), horizontalalignment='center', color=clr, fontsize=12)


    # Finally, save the figure as a PNG.  
    # You can also save it as a PDF, JPEG, etc.  
    # Just change the file extension in this call.  
    # bbox_inches="tight" removes all the extra whitespace on the edges of your plot.  
    plt.savefig(filename + ".png", bbox_inches="tight", dpi=100); 

def analyze(friends_file, edges_file):
    # edges = {}
    # with open(edges_file) as f:
    #     for line in f:
    #         try:
    #             u, v, score = line.rstrip().split(";")
    #             edges[(u,v)] = score, 0
    #         except Exception:
    #             print line

    # print "edges finished"

    # with open(friends_file) as g:
    #     for line in g:
    #         w, x = line.rstrip().split(";")
    #         try:
    #             a, _ = edges[(w,x)]
    #         except KeyError:
    #             pass
    #         else:
    #             edges[(w,x)] = a, 1
    #         try:
    #             a, _ = edges[(x,w)]
    #         except KeyError:
    #             pass
    #         else:
    #             edges[(x,w)] = a, 1

    # with open("yyy", "wb") as f:
    #     pickle.dump(edges, f)
    # print "saved"

    with open("yyy", "rb") as g:
        edges = pickle.load(g)

    friends_u = [int(float(c)) for c,f in edges.values() if f==1]
    scores_u = [int(float(c)) for c, _ in edges.values()]
    dist_fig(scores_u, friends_u, 0, 200, "active_edges_common_600_20_friends.png")

if __name__ == "__main__":
    analyze("friends.csv", "edges/random_edges_common_5000_30.csv")

