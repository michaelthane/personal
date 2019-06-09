# Automation of Intelligent Investing

The Intelligent Investor, by Benjamin Graham, teaches investors a method of financial analysis focused on low risks and
high returns. This sounds like an obvious method that most investors already employ; however, the process of acquiring
financial data can be time consuming and cumbersome for the average person. The purpose of this project is to automate
this process so that even an average person can be an intelligent investor.

## The Seven

According to Benjamin Graham, the following are seven statistical requirements a company must meet for inclusion in a 
defensive investor's portfolio:

1. Adequate size
    - $2B or higher (mid-cap)
    - Small stocks can be owned through mutual funds specializing in small stocks

2. A sufficiently strong financial condition
    - Current assets : Current Liabilities -> 2 : 1;
    - Long term debt should not exceed working capital;
    - Best value today are stocks that were once hot and have since gone cold

3. Continued dividend for at least the past 20 years

4. No earning deficit in the past 10 years

5. Ten-year growth of at least 1/3 in per-share earnings (can also be 50% or 100% for spiciness)
    - Example: If looking at companies from 1993 to 2002, average EPS from 1991-1993 and compare to average EPS from 
    2000-2002

6. Price of stock no more than 1.5 times net asset value (NAV) (P/B Ratio)
    - Value of company can also come from franchises, brand name, patents, trademarks
    - 2.5 is a good max limit

7. Price no more than 15x average EPS of the past 3 years
    - (P/E) * (P/B) < 22.5 -> a good initial screen

The above requirements exclude companies that are:
- too small
- in relatively weak financial condition
- with a deficit stigma in their ten-year record
- without a long history of dividends

## Caveats

[XBRL Parser by tooksoi](https://github.com/tooksoi/ScraXBRL). His or her project is for XBRL documents.

This project focuses on getting financial data from .htm and .html documents. On SEC's EDGAR database, XBRL douments 
are typically only available for a company's latest 10 years.

Package highlights include Beautifulsoup, re, pandas, and selenium.

Future steps would also get financial data from .txt documents, which is the only available form in 1994 and some years 
after.

## Order of Operations

1. Navigate to listings page using Selenium.
2. Parse 10 annual reports to create combinations of Financial Statements.
    - Income, Balance, Cash Flow, Stockholder's' Equity
3. Write to google sheets. 
4. DataVis for to see if and when The Seven are met. 
    - This CAN be done in Tableau via google sheets.
5. If met, further research is warranted. Otherwise, disregard and DO NOT waste time.

## Installation

add chromedriver to PC path.

pip freeze > requirements.txt