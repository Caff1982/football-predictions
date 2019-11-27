# Football Predictions

Using machine-learning to predict the outcome of football matches. 

## Requirements

- Python 3
- Jupyter notebook
- Pandas
- Numpy
- Keras
- Selenium (optional)

## Description

This is my project to predict football results using machine-learning. My goal is to get a model that is more accurate than the bookmakers predictions.

I used several approaches to creating input data and combined the features I found most useful. I used league-stats to capture difference in previous league position, difference in points etc. I also used Exponentially weighted Moving Averages(EMAs) to get form across several features. I also used B365 betting odds as input.

For the model itself I used Keras to create a Neural Network. Although the the dataset is fairly small (5000 matches and 36 features) I found this outperformed any other algorithm I tried.

## License
Licensed under the [MIT](https://choosealicense.com/licenses/mit/) license.


## Credits

For creating the league-stats dataset I took a lot of inspiration from the repository below. The functions for preparing the data were very useful. 

- (https://github.com/RudrakshTuwani/Football-Data-Analysis-and-Prediction)

I also took a lot of inspiration from the repository below for the exponential moving-averages dataset. Most of the function I used to create the EMA dataset have been taken and adapted from here.

- (https://github.com/betfair-datascientists/predictive-models/tree/master/epl)

## Contributions

Any Pull Requests are welcome
