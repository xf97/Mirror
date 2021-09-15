# Mirror(镜像)
![logo](logo.jpg)

*Mirror* is the program used in our paper **An identification mechanism of stock price bubble: evidence from Chinese stock market**, which is mainly used to simulates stock automatic trading.



## How to use *Mirror*

To drive mirror, you need to provide the following groups of data:

1. Initial stock price (by modifying *data/datarequiredformirror.xlsx/initPrice.sheet*)
2. The probability of users purchasing each stock each year (by modifying *data/DataRequiredForMirror.xlsx/purchaseProb.sheet*, please refer to our paper for the calculation method of purchase probability)
3. Number of trading days per month per year (by modifying *data/DataRequiredForMirror.xlsx/trading day and trading year.sheet*)
4. The initial capital of each user and the total number of shares of each stock (by modifying *data/DataRequiredForMirror.xlsx/initFund.sheet*, our suggestion is to give each user the same initial capital, and the total capital is twice the total initial value of all stocks)



We have given the templates of the *DataRequiredForMirror.xlsx*, you can change the internal data according to your needs, but please do not change the file name, sheet name, column name.



In addition, you also need to give the following three values:

1. Number of users participating by modifying  *userNeeds.json-USERS_NUM*
2. The number of stocks participating in the simulation by modifying  *userNeeds.json-SHARES_NUM* (please keep the same with the number of stocks filled in the *DataRequiredForMirror.xlsx*)
3. The duration years of the simulation by modifying  *userNeeds.json-LAST_YEARS* (please keep it consistent with the length of the year filled in the *DataRequiredForMirror.xlsx*)



After given the above data, you can start Mirror by entering the following commands in the terminal, and the simulation results will be stored in the **result** folder:

```shell
cd Mirror\src
python main.py
```

And you're done! The execution process will be printed in the terminal.

## How to install

Make sure that git and python3 (and python3's pip) have been installed on your computer, and you can install *Mirror* (and its dependencies) by entering the following commands in the terminal:

```
git clone https://github.com/xf97/Mirror
cd Mirror
pip install -r usedPackage.txt
```

And you're done!

## Supported operating systems
At present, we have only tested *Mirror* on Windows 10.



## License
This program is issued, reproduced or used under the permission of **MIT**. Please indicate the source when using.



