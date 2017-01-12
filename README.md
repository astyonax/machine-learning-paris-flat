
# Machine Learning Paris Flats

I just moved to Paris from Germany, and I find the flats-renting market quite different and more complicate.
That's not only because of the prices. Nonetheless, in this series of notebooks I want to get a quantitative view of the situation.

The idea is to scrap some data from websites to see the obvious correlations, like price _vs_ district (arrondissement, here), the non-trivial correlated features, e.g. a non-linear size _vs_ price/sqm relation, or even better, if there are some conditions, like the flat floor, or the availabily of laundry or parking, that do not correlate strongly with the price/size/district.

## Second version
[The second (and current)](v2/) version is much lighter than the 1<sup>st</sup> one thanks to the use of a better source of data.

The flats price and features are somewhat delucitated and a heatmap of *price per arrondissement* is done with the Leaflet ipython extension.

## First version
In [the first version](v1/) I took the data from a complicate website, thus we use some creative way to fill in the empty or wrong records.s
