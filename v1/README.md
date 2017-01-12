
# Machine Learning Paris Flats

I just moved to Paris from Germany, and I find the flats-renting market quite different and more complicate.
That's not only because of the prices. Nonetheless, in this series of notebooks I want to get a quantitative view of the situation.

The idea is to scrap some data from websites to see the obvious correlations, like price _vs_ district (arrondissement, here), the non-trivial correlated features, e.g. a non-linear size _vs_ price/sqm relation, or even better, if there are some conditions, like the flat floor, or the availabily of laundry or parking, that do not correlate strongly with the price/size/district.

This turns out to be also a good chance to learn some new libraries I wanted to play with since a while:
* `Beautifulsoup`
* `Pandas` (with mixed text/number data)
* `Scikit-learn`
* fuzzy string matching
* `Seaborn`'s statistical plotting capabilities

Indeed, I won't discuss at all the actual results, as that is interesting to me only, while the techniques may have a broader usage.

**Nota bene:** The data collected with webscraping can be highly imperfect, as many details usually lie embedded in the text. For example, a given price may or may not include some expenses (like electricity or water, or agency fees). I did not find, nor carefully look for, a website with all the informations already sorted out. I just googled for flats in paris and found craig list. That's the starting point.

## Machine Learning tutorials
As I am already used to python for work, for fun, and in every other occasion it proves useful, I went for tutorials that focus on scikit-learn, _not_ python, numpy, jupyter, ...
I tried to keep the same definitions of the 1st reference. Hence, e.g., _model_ refers to a Machine Learning model. `features` are the features of each flat, in this sense, our dataset's columns are the `features`.

1. [Advanced Machine Learning with scikit-learn](https://www.youtube.com/watch?v=iFkRt3BCctg),
2. [Scikit-learn User Guide](http://scikit-learn.org/stable/user_guide.html)
3. [An Introduction to scikit-learn (II)](https://conference.scipy.org/scipy2013/tutorial_detail.php?id=111)
4. [NLTK book, Ch. 6: Learning to Classify Text](http://www.nltk.org/book/ch06.html): not needed now, may be in the future

Links 1., and 3. are 2013 resources. You may be looking for something more up to date; I was for the bases.

## Chapters

The story develops in 6 chapters. Some of them are more interesting, and some are more commented out.
Ideally, the first 3 chapters deal with getting the data, and the second three with analyzing the data.

### Getting the data
1. [Web scraping](CL.ipynb)
> In this notebook we download a list of flats from the Paris section of crag list.  
> The notebook is not very commented, as the task is boring, and quite simple.
> Of note, we use a Poissonian waiting time between the download of subsequent pages to mimick a human behaviour
> The flats list is stored as pickle in `locations.pkl`
2. [Paris Metros](Paris Metro.ipynb)
> A map between the metro stations cited in the flats description and the corresponding district.
> The initial data comes from wikipedia, but in this notebook it is prepared to be robust against typos
3. [Refinement](normalize_CL.ipynb)
> The data, as downloaded, is quite rough, this is a step of massaging. Other 2 will come ;)
> We will remove some of the unicode problems, look for (typos-proof) metro stations in the description, map them to  the district, refine our RegEx to match the addresses, find the flat floor, and use fuzzy string matching everywhere possible.
> The initial list of random, clumsy fields will be cast on a nice, _pandas_, `dataframe`, and saved in `hdf5`


### Analyzing the data
4. [Simple Machine Learning and complicate plotting](ML 1 -- see in the data.ipynb)
> In which we use PCA, and some complicate plotting strategy.
> I am a physicist, so I won't let the machine tell me what's the model. Instead we let PCA suggest some correlations,
> we will see that PCA is here and there right, but can also fail.
> What I like of PCA is that it is an unsupervised ML model that can be understooooood!!!
5. [Machine Learning to fill the gaps](ML 2 -- Fill the gaps.ipynb)
> Missing data, what the hell. Here we fill some of the gaps. Not all, but better than nothign,
> We choose to train a `DecisionTree` on a set of features with high-variance [$\nearrow$](http://scikit-learn.org/stable/modules/feature_selection.html). Why? With an analogy to statistical mechanics, those features that scan most of the possible parameters allow knowing more of the configurational/parameters space.
> We use `DecisionTrees` because they are amazing, as they can refine even more our choice of features because they make their own ranking.
> We also train different other models, in order to choose the best one, and later verify the predictions against two of them.
> Optmization is done with `GridSearchCV`.
6. [V for Plotting 2](ML 3 -- see in the data.ipynb)
> Ok ok. Thus, we have less gaps: each flat has a `predicted floor`. Is that useful?
> No.
> But, we can still understand more than before by some clever plots, and close here.

So far I am happy with what I've done, learned, and found. It's time to change project.
In the, not too near future I'll come back to conclude with the following two chapters.

## Next
7. [Other sources](..)
> There are other sources of data that may offer a different perspective
> The problem is that we have to go back to the boring scraping..


8. [Natural Language](..)
> Is it possible to extract more from the description, sort it, and the analyze it?
>
