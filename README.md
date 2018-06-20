<h1>Predicting flight delays using deep learning</h1>

This is an attempt to predict delays in both the arrival and the departure of domestic flights within the US. Specifically, the data was pulled from <a href="https://www.kaggle.com/usdot/flight-delays">this Kaggle dataset</a>, which contains information on over 5 million domestic flights in 2015, courtesty of the US Department of Transportation. The L_AIRPORT.csv_ and L_AIRPORT_ID.csv_ files came from the Bureau of Transportation Statistics. 
 
I did not upload the data to this repository because it's nearly 200 MB. However, in order to execute the scripts and notebooks in this repository, you will have to download and unzip the dataset from Kaggle. It's necessary for the three unzipped files (flights.csv, airlines.csv, and airports.csv) to be in whatever directory you clone this repository into.

Once you have downloaded and unzipped the data, you must either go through the preprocess.ipynb notebook or run preprocess.py.

You can then go through delay_prediction.ipynb to see how well my models perform. 

When I ran my models, I got a mean absolute error for both arrival delay AND departure delay of less than 4 minutes. My results are summarized in delay_prediction.ipynb.