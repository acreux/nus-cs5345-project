from collections import defaultdict
import numpy as np
import matplotlib.pyplot as plt
import cPickle as pickle


class Chart(object):

    def __init__(self):
        self.book_counter = defaultdict(int)
        self.user_counter = defaultdict(int)
        self.user_r = defaultdict(int)
        self.book_r = defaultdict(int)
        # with open("user_book_sample_50.csv") as f:
        with open("user_book_raw.csv") as f:
            for line in f:
                u, b, r = line.split(";")
                self.book_counter[b] += 1
                self.book_r[b] += int(r)
                self.user_counter[u] += 1
                self.user_r[u] += int(r)

        self.book_rating = {k: 1. * v/self.book_counter[k] for k, v in self.book_r.iteritems()}
        self.user_rating = {k: 1. * v/self.user_counter[k] for k, v in self.user_r.iteritems()}
        
    @staticmethod
    def load(filename="chart"):
        """Load a graph picke file"""
        with open(filename, "rb") as f:
            return pickle.load(f)

    def save(self, filename="chart"):
        """Save a graph using pickle"""
        file_name = filename
        with open(file_name, "wb") as f:
            pickle.dump(self, f)

    def user_average_book(self):
        return np.mean(self.user_counter.values())

    def book_average_user(self):
        return np.mean(self.book_counter.values())

    def user_average_rating(self):
        return np.mean(self.user_rating.values())

    def book_average_rating(self):
        return np.mean(self.book_rating.values())

    def user_median_book(self):
        return np.median(self.user_counter.values())

    def book_median_user(self):
        return np.median(self.book_counter.values())

    def user_median_rating(self):
        return np.median(self.user_rating.values())

    def book_median_rating(self):
        return np.median(self.book_rating.values())

    def user_scatter(self, lim=10**6, filename=None):

        fig, ax = self.get_fig()

        # ax.set_xlabel("Number of books read")
        ax.set_ylabel("Average reader rating")
        ax.set_title("Distribution of reader rating")
        
        y = [self.user_counter[k] for k in self.user_counter if self.user_counter[k]<lim]
        x = [self.user_rating[k] for k in self.user_counter if self.user_counter[k]<lim]
        
        plt.scatter(x, y, c="#3F5D7D");
        plt.xlim(1, max(x))
        plt.ylim(min(y), max(y))
        filename_scatter = filename or "user_scatter_" + str(lim)
        plt.savefig(filename_scatter + ".png", bbox_inches="tight", dpi=100);

    def get_fig(self):
        # Create new Figure with black background
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

    def book_scatter(self, lim=10**6, filename=None):

        fig, ax = self.get_fig()
        ax.get_yaxis().set_visible(True)  

        # ax.set_xlabel("Number of readings")
        ax.set_ylabel("Average book rating")
        ax.set_title("Distribution of average book rating")

        y = [self.book_counter[k] for k in self.book_counter if self.book_counter[k]<lim]
        x = [self.book_rating[k] for k in self.book_counter if self.book_counter[k]<lim]
        
        plt.scatter(x, y, c="#3F5D7D");
        plt.xlim(0, max(x))
        plt.ylim(min(y), max(y))

        filename_scatter = filename or "book_scatter_" + str(lim)
        plt.savefig(filename_scatter + ".png", bbox_inches="tight", dpi=100);

    def user_fig(self):
        self.dist_fig(df=self.user_counter,
                 limit_high=500,
                 start=0,
                 step=50,
                 xlabels="Number of books read",
                 ylabels="Readers(%)",
                 title='Distribution of readers by number of books read',
                 filename="users", 
                 plus=True)

    def book_fig(self):
        self.dist_fig(df=self.book_counter,
                 limit_high=10,
                 start=1,
                 step=1,
                 xlabels="Numbers of readers",
                 ylabels="Books(%)",
                 title='Distribution of books by number of readers',
                 filename="books",
                 plus=True)

    def book_rating_fig(self):
        self.dist_fig(df=self.book_rating,
                     limit_high=5,
                     start=1,
                     step=0.2,
                     xlabels="Ratings",
                     ylabels="Books(%)",
                     title='Distribution of books',
                     filename="books_ratings")

    def user_rating_fig(self):
        self.dist_fig(df=self.user_rating,
                     limit_high=5,
                     start=1,
                     step=0.2,
                     xlabels="Ratings",
                     ylabels="Readers(%)",
                     title='Distribution of readers',
                     filename="user_ratings")


    def dist_fig(self, df, limit_high, step, xlabels, ylabels, title, filename, start=0, plus=False):
        values = np.clip(df.values(), 1, limit_high)

        range_bins = np.arange(start=start, stop=limit_high+2*step, step=step)

        hist_normed, _ = np.histogram(values, bins=range_bins, density=True)
        hist, bins = np.histogram(values, bins=range_bins)

        hist_normed = step*hist_normed
        print hist, sum(hist)
        print hist_normed, sum(hist_normed)
        width = 1 * (bins[1] - bins[0])
        center = (bins[:-1] + bins[1:]) / 2

        # fig, ax = plt.subplots(figsize=(20, 14))

        fig, ax = self.get_fig()

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
        x = []
        for i, j in zip(bins, bins[1:]):
            if j-i == 1:
                x.append(i)
            else:
                x.append("{0}-{1}".format(i, j))
            
        # Display 100-200-300-400-500+ for books-users
        # Display 1-2-3-4-5 for ratings
        if plus:
            x[-1] = str(limit_high) + " +"

        # add some text for labels, title and axes ticks
        # ax.set_ylabel('Users(%)')
        ax.set_xlabel(xlabels)
        ax.set_ylabel(ylabels)
        ax.set_title(title)
        ax.set_xticks(center)
        ax.set_xticklabels(x, fontsize=14, rotation=+45)
        bars = plt.bar(center, hist_normed, align='center', width=width, color="#3F5D7D")

        max_height = max(b.get_height() for b in bars)
        # Lastly, write in the ranking inside each bar to aid in interpretation
        for bar, val, val_normed in zip(bars, hist, hist_normed):
            # Rectangle widths are already integer-valued but are floating
            # type, so it helps to remove the trailing decimal point and 0 by
            # converting width to int type
            height = bar.get_height()

            if (height < 0.05):        # The bars aren't wide enough to print the ranking inside
                # yloc_normed = 1.0008 * height
                yloc = height + max_height*0.02   # Shift the text to the right side of the right edge
                
                clr = 'black'      # Black against white background
            else:
                yloc = height-max_height*0.03
                # yloc_normed = height*0.8
                # Shift the text to the left side of the right edge
                clr = 'white'      # White on magenta

            xloc = bar.get_x()+bar.get_width()/2.0
        #     ax.text(xloc, yloc_normed, str(val), horizontalalignment='center', color=clr)
            ax.text(xloc, yloc, '{:.1%}'.format(val_normed), horizontalalignment='center', color=clr)


        # Finally, save the figure as a PNG.  
        # You can also save it as a PDF, JPEG, etc.  
        # Just change the file extension in this call.  
        # bbox_inches="tight" removes all the extra whitespace on the edges of your plot.  
        plt.savefig(filename + ".png", bbox_inches="tight", dpi=100); 


if __name__ == "__main__":
    pass
    c = Chart()
    print c.user_average_book()
    print c.book_average_user()
    print c.user_average_rating()
    print c.book_average_rating()
    c.book_fig()
    c.user_fig()
    c.book_rating_fig()
    c.user_rating_fig()

    c.user_scatter(lim=10**6, filename="user_scatter")
    c.user_scatter(lim=1500, filename="user_scatter_1500")
    c.book_scatter(lim=10**6, filename="book_scatter")
    c.book_scatter(lim=1500, filename="book_scatter_1500")
