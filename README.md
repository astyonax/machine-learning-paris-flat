
# Machine Learning Paris Flats

I just moved to Paris from Germany, and I find the flats-renting market quite different and more complicate.
Thus, in this series of notebooks I want to get a quantitative visualization of the situation.

The idea is to scrap some data from websites to measure  the obvious:  eg. price _vs_ district; and the less obvious: e.g. a non-linear size _vs_ price/sqm relation, or lack of relations with respect to cases in which one would expect a correlation.

## Summary of analysis

The following data is for  furnished, 2 rooms flats, with minimum size of 25m<sup>2</sup>, within Paris only.

### Flats distribution per arrondissement and per size

![](v2/plots/flats_distribution.png) 

*Figure 1:  Histogram of 2 rooms flats per price and per arrondissement (left) and per binned size and per arrondissement (right).*

### Price distributions
![ ](v2/plots/price_breakdown.png  "Price Breakdown #1/3")

*Figure 2:  Two visualizations of the price per square meter (€/m<sup>2</sup>) versus flat sizes, averaged over arrondissement. Blue: unfournished, Green: fournished. 

![ ](v2/plots/price_breakdown_2.png  "Price Breakdown #2/3")

*Figure 3: Visualization of the price per square meter versus arrondissement and flat size. Red dots: unfurnished. Filled dots: furnished.*


![ ](v2/plots/price_breakdown_3.png  "Price Breakdown #3/3")

*Figure 4: Energy efficiency of Paris flats. Same color-coding as previous plot. There is no need to comment.*

![ ](v2/plots/PCA.png  "Relevant features from PCA")

*Figure 6: PCA to identify some important features. There is no attempt to do a more robust assessment with a kernel PCA (I don't need it now). Note, however, that the 3 modes shown represent about 97% of the data, so they are enough (in this case)*

So, Price correlates with size, which in turns weakly correlates with the arrondissement. One would expect also that the energy level correlates with the price as a proxy for the flat quality but it's not the case. 
I think that for the choosen features, the data is too noisy; but the current perspective is enough for the moment.

### Sustainability

How much does a couple has to earn to afford to live in Paris? 
Using the rule that a flat can't be more expensive than 1/3 of the net total income of the inhabitants, the average needed income per person per month is about 1900 €/monnth, assuming that the flat is inhabited by 2 persons with equal income.

![ ](v2/plots/sustainability.png  "Sustainability")

*Figure 7: (Left) Distribution of average income for a couple (green), and per person (assuming 2 persons in the flat, and equal income) (blue). -- (Right) Price distribution of all flats of 2 rooms (blue), and of flats with size  between 35m<sup>2</sup> and 50m<sup>2</sup> (green) -- White lines correspond to the average of the distribution. Binning: 100€.*



## Notebooks
### Analysis

[Analysis notebook on *nbviewer*](https://nbviewer.jupyter.org/github/astyonax/machine-learning-paris-flat/blob/master/v2/Visualize on-sight insights.ipynb)

### Web scraping + Analysis

[the notebook on *nbviewer*](https://nbviewer.jupyter.org/github/astyonax/machine-learning-paris-flat/blob/master/v2/LBC-simple.ipynb)

[the *jupyter notebook* as web-page](http://htmlpreview.github.io/?https://github.com/astyonax/machine-learning-paris-flat/blob/master/v2/rendered/LBC-simple.html).

## History

### [V 2 -- the newest](v2/)

**TL;DR:** [the *jupyter notebook* as web-page](http://htmlpreview.github.io/?https://github.com/astyonax/machine-learning-paris-flat/blob/master/v2/rendered/LBC-simple.html).

[The second (and current)](v2/) version is more straightforward than the 1<sup>st</sup> one thanks to the use of a better data source ([Le Bon Coin](leboncoin.fr)).

The flats price versus flats features are quite self-explaining by the plots. A heatmap of *price per arrondissement* is done with the [Leaflet ipython extension](https://github.com/ellisonbg/ipyleaflet).


### [V 1](v1/)
In [the first version](v1/) I took the data from a complicate website, thus we use some creative way to fill in the empty or wrong records.s


## Dependencies

* `Jupyter`
* `Beautifulsoup`
* `Pandas` 
* `Scikit-learn`
* fuzzy string matching
* `Seaborn`
