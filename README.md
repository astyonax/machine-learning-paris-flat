
# Machine Learning Paris Flats

I just moved to Paris from Germany, and I find the flats-renting market quite different and more complicate.
That's not only because of the prices. Thus, in this series of notebooks I want to get a quantitative view of the situation.

The idea is to scrap some data from websites to measure  the obvious:  eg. price _vs_ district; and the less obvious: e.g. a non-linear size _vs_ price/sqm relation, or lack of relations with respect to cases in which one would expect a correlation.


**TL;DR:** [the *jupyter notebook* as web-page](http://htmlpreview.github.io/?https://github.com/astyonax/machine-learning-paris-flat/blob/master/v2/rendered/LBC-simple.html).


## Summary of analysis

The following data is for  fournished, 2 rooms flats, with minumu size of 30m<sup>2</sup>, within Paris only.

### Flats distribution per arrondissement and per size



![](/home/astyonax/Projects/machine-learning-paris-flat/v2/plots/flats_distribution.png) 
*Figure 1:  Histogram of 2 rooms flats per price and per arrondissement (left) and per binned size and per arrondissement (right). Size binning = 5m<sup>2</sup>. Minimum size capped at 30m<sup>2</sup>.*

### Price distributions
![ ](/home/astyonax/Projects/machine-learning-paris-flat/v2/plots/price_breakdown.png  "Price Breakdown #1/3")
*Figure 2:  Two visualizations of the price per square meter (€/m<sup>2</sup>) versus flat sizes, averaged over arrondissement. Blue: unfournished, Green: fournished. **Note**: The price per square meter obviously decreases with flat size, however the noise appears to be quite important, probably meaning that we are missing some important variables.*

![ ](/home/astyonax/Projects/machine-learning-paris-flat/v2/plots/price_breakdown_2.png  "Price Breakdown #2/3")
*Figure 3: Visualization of the price per square meter versus arrondissement, flat size. Red dots: unfournished. Filled dots: fournished.*

## [V 2 -- the newest](v2/)

**TL;DR:** [the *jupyter notebook* as web-page](http://htmlpreview.github.io/?https://github.com/astyonax/machine-learning-paris-flat/blob/master/v2/rendered/LBC-simple.html).

[The second (and current)](v2/) version is more straightforward than the 1<sup>st</sup> one thanks to the use of a better data source ([Le Bon Coin](leboncoin.fr)).

The flats price versus flats features are quite self-explaining by the plots. A heatmap of *price per arrondissement* is done with the [Leaflet ipython extension](https://github.com/ellisonbg/ipyleaflet).


## [V 1](v1/)
In [the first version](v1/) I took the data from a complicate website, thus we use some creative way to fill in the empty or wrong records.s


## Dependencies

* `Jupyter`
* `Beautifulsoup`
* `Pandas` 
* `Scikit-learn`
* fuzzy string matching
* `Seaborn`
