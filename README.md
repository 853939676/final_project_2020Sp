# Corona Beer and COVID-19
This is Rui Liu(ruiliu8)'s final project for IS590PR Spring2020.

Project Type: (Type II Projects) Specifics for an Original Data Analysis

## Proposal: 

**Description:**

The spread of COVID-19 is causing huge panic around the world. Due to the name of coronavirus, 
some people connect it with Corona Beer and refuse to buy any Corona Beer under this circumstances. This project aims to study how the spread of COVID-19 influence the stock price of Constellation Brand(owner of Corona Beer). 

**Hypothesis:**

* The spread of COVID-19 will negatively influence the stock price of Constellation.
* The influence of coronavirus on Corona Beer stock price will gradually disappear as coronavirus continues.

**Datasets:**

* COVID-19 Data: https://github.com/nytimes/covid-19-data
* Stock price data: csv files downloaded from https://finance.yahoo.com/

## Methodology and Result
The program can retrieve up-to-date stock prices and [COVID-19 data](https://github.com/nytimes/covid-19-data) online and merge them together 
to visualize stock prices and the spread of COVID-19.

Users can run the code directly to get following comparisons:
* Stock prices of [Corona(STZ)](https://finance.yahoo.com/quote/STZ?p=STZ&.tsrc=fin-srch)
vs. [Bud Light(BUD)](https://finance.yahoo.com/quote/BUD?p=BUD&.tsrc=fin-srch) before and after COVID-19
![BUD](https://github.com/853939676/final_project_2020Sp/blob/master/img/BUD_ba.png)

* Stock prices of [Corona(STZ)](https://finance.yahoo.com/quote/STZ?p=STZ&.tsrc=fin-srch) 
vs. [Coors Light(TAP)](https://finance.yahoo.com/quote/TAP?p=TAP&.tsrc=fin-srch) before and after COVID-19
![TAP](https://github.com/853939676/final_project_2020Sp/blob/master/img/TAP_ba.png)

* Stock price differences and new confirmed cases in the US
![BUD and TAP](https://github.com/853939676/final_project_2020Sp/blob/master/img/BUD_TAP_COVID.png)

Additional analysis can also be done using this program by changing function parameters, 
some examples are given in the code:
* Compare stock price difference of [Corona(STZ)](https://finance.yahoo.com/quote/STZ?p=STZ&.tsrc=fin-srch) 
and [S&P 500(^GSPC)](https://finance.yahoo.com/quote/%5EGSPC?p=^GSPC) number.
![GSPC](https://github.com/853939676/final_project_2020Sp/blob/master/img/GSPC_ba.png)

* Compare stock price difference with daily confirmed COVID-19 cases in Illinois state.
![BUD and TAP](https://github.com/853939676/final_project_2020Sp/blob/master/img/BUD_TAP_IL.png)

A slide containing detailed code structure and result graphs can be downloaded [here.](https://github.com/853939676/final_project_2020Sp/blob/master/Slide.pdf)

## Conclusion:

* The spread of COVID-19 did negatively impacted the stock price of Corona Beer compared with other beer companies, 
especially from 3/06 to 3/18.
* The effect of COVID-19 is decreasing after 3/18.

* There might be a positive relationship between COVID-19 and the stock price of Corona Beer compared with S&P 500 number.

