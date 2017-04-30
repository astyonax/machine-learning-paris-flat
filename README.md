
# Machine Learning Paris Flats

I just moved to Paris from Germany, and I find the flats-renting market quite different and more complicate.
That's not only because of the prices. Thus, in this series of notebooks I want to get a quantitative view of the situation.

The idea is to scrap some data from websites to measure  the obvious:  eg. price _vs_ district; and the less obvious: e.g. a non-linear size _vs_ price/sqm relation, or lack of relations wrt cases in which one would expect a correlation.

## V 2 -- the newest
[The second (and current)](v2/) version is much straightforward than the 1<sup>st</sup> one thanks to the use of a better source of data ([Le Bon Coin](leboncoin.fr)).

The flats price and features are somewhat delucitated and a heatmap of *price per arrondissement* is done with the [Leaflet ipython extension](https://github.com/ellisonbg/ipyleaflet).

The rendered notebook is at [this link](v2/rendered/LBC-simple.html).

## V 1
In [the first version](v1/) I took the data from a complicate website, thus we use some creative way to fill in the empty or wrong records.s
