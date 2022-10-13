Schema for the Database:
![img.png](img.png)

1. Query for top25 gainers on given day,
    
```sqlite
SELECT
    t1.TIMESTAMP,
    t2."NAME OF COMPANY",
    t2.SYMBOL,
    ((t1.CLOSE-t1.OPEN)/t1.OPEN) as "Gain",
    t2."SERIES"
from Bhavcopy as t1
    INNER JOIN "Equity Segment Securities" as t2
    ON t1.ISIN = t2."ISIN NUMBER"
ORDER BY Gain desc
limit 25;
```
Result for above query 
```
+-----------+-------------------------------------+----------+-------------------+------+
|TIMESTAMP  |NAME OF COMPANY                      |SYMBOL    |Gain               |SERIES|
+-----------+-------------------------------------+----------+-------------------+------+
|13-OCT-2022|Hindcon Chemicals Limited            |HINDCON   |0.15222375057313167|EQ    |
|13-OCT-2022|Indo Amines Limited                  |INDOAMIN  |0.13513513513513514|EQ    |
|13-OCT-2022|Suzlon Energy Ltd-RE                 |SUZLON-RE |0.1250000000000001 |BE    |
|13-OCT-2022|DSJ Keep Learning Limited            |KEEPLEARN |0.10416666666666667|BE    |
|13-OCT-2022|Liberty Shoes Limited                |LIBERTSHOE|0.1041639641976911 |EQ    |
|13-OCT-2022|Pennar Industries Limited            |PENIND    |0.10359869138495092|EQ    |
|13-OCT-2022|Aditya Birla Money Limited           |BIRLAMONEY|0.10042553191489371|EQ    |
|13-OCT-2022|Dredging Corporation of India Limited|DREDGECORP|0.09993763642033057|EQ    |
|13-OCT-2022|RITES Limited                        |RITES     |0.09959525874530224|EQ    |
|13-OCT-2022|Rajdarshan Industries Limited        |ARENTERP  |0.093603744149766  |EQ    |
|13-OCT-2022|Kritika Wires Limited                |KRITIKA   |0.08937198067632858|EQ    |
|13-OCT-2022|Next Mediaworks Limited              |NEXTMEDIA |0.0882352941176471 |EQ    |
|13-OCT-2022|Apollo Sindoori Hotels Limited       |APOLSINHOT|0.0876251666040122 |EQ    |
|13-OCT-2022|PVP Ventures Limited                 |PVP       |0.08641975308641989|EQ    |
|13-OCT-2022|Rama Steel Tubes Limited             |RAMASTEEL |0.08457943925233642|EQ    |
|13-OCT-2022|Vertoz Advertising Limited           |VERTOZ    |0.08041060735671507|EQ    |
|13-OCT-2022|Ortel Communications Limited         |ORTEL     |0.08000000000000007|BZ    |
|13-OCT-2022|Bedmutha Industries Limited          |BEDMUTHA  |0.07994186046511628|EQ    |
|13-OCT-2022|Hotel Rugby Limited                  |HOTELRUGBY|0.075268817204301  |BE    |
+-----------+-------------------------------------+----------+-------------------+------+
```
2. Query for top25 gainers for each day in last 30 working days
```sqlite
with top25 as (
    SELECT *, ROW_NUMBER() over (PARTITION BY TIMESTAMP order by Gain desc ) as rn
    from (
        SELECT *,
        ((t1.CLOSE- t1.OPEN)/t1.OPEN) as Gain
        from Bhavcopy as t1
    )
)
select top25.TIMESTAMP, t2."NAME OF COMPANY", t2.SYMBOL, top25.Gain, top25.rn, t2.SERIES
from top25 join "Equity Segment Securities" as t2 on t2."ISIN NUMBER" = top25.ISIN
where rn <=25;
```
Result for above CTE
```
+-----------+-------------------------------------------+----------+-------------------+------+
|TIMESTAMP  |NAME OF COMPANY                            |SYMBOL    |Gain               |SERIES|
+-----------+-------------------------------------------+----------+-------------------+------+
|01-SEP-2022|Pritika Auto Industries Limited            |PRITIKAUTO|0.14714714714714733|EQ    |
|01-SEP-2022|Tata Teleservices (Maharashtra) Limited    |TTML      |0.139347923179991  |BE    |
|01-SEP-2022|Paramount Communications Limited           |PARACABLES|0.13624678663239087|BE    |
|01-SEP-2022|Hindware Home Innovation Limited           |HINDWAREAP|0.12890625         |EQ    |
|01-SEP-2022|IFCI Limited                               |IFCI      |0.1284403669724771 |EQ    |
|01-SEP-2022|RKEC Projects Limited                      |RKEC      |0.1268403171007928 |EQ    |
|01-SEP-2022|Compucom Software Limited                  |COMPUSOFT |0.12582781456953648|EQ    |
|01-SEP-2022|Fineotex Chemical Limited                  |FCL       |0.12258530420653543|EQ    |
|01-SEP-2022|Bharat Gears Limited                       |BHARATGEAR|0.12122905027932955|EQ    |
|01-SEP-2022|Manaksia Coated Metals & Industries Limited|MANAKCOAT |0.11528150134048269|EQ    |
|01-SEP-2022|Ashima Limited                             |ASHIMASYN |0.11272727272727277|EQ    |
|01-SEP-2022|Best Agrolife Limited                      |BESTAGRO  |0.11229787234042557|EQ    |
|02-SEP-2022|Automotive Stampings and Assemblies Limited|ASAL      |0.1746478873239436 |EQ    |
|02-SEP-2022|Shiva Mills Limited                        |SHIVAMILLS|0.1725197541703249 |EQ    |
|02-SEP-2022|EIH Limited                                |EIHOTEL   |0.1717581047381545 |EQ    |
|02-SEP-2022|Surana Solar Limited                       |SURANASOL |0.1656050955414012 |EQ    |
|02-SEP-2022|AksharChem India Limited                   |AKSHARCHEM|0.16362492133417242|EQ    |
|02-SEP-2022|Royal Orchid Hotels Limited                |ROHLTD    |0.1536782361929709 |EQ    |
|02-SEP-2022|Country Club Hospitality & Holidays Limited|CCHHL     |0.13636363636363633|BE    |
|02-SEP-2022|MIRC Electronics Limited                   |MIRCELECTR|0.11141304347826092|EQ    |
|02-SEP-2022|TCNS Clothing Co. Limited                  |TCNSBRANDS|0.10589510547819561|EQ    |
|02-SEP-2022|Udaipur Cement Works Limited               |UDAICEMENT|0.10016155088852982|EQ    |
|02-SEP-2022|EIH Associated Hotels Limited              |EIHAHOTELS|0.09796481545360461|EQ    |
|02-SEP-2022|The Byke Hospitality Ltd                   |BYKE      |0.0950276243093922 |EQ    |
|02-SEP-2022|GMM Pfaudler Limited                       |GMMPFAUDLR|0.09460431654676256|EQ    |
|02-SEP-2022|Omax Autos Limited                         |OMAXAUTO  |0.09448082319925158|EQ    |
+-----------+-------------------------------------------+----------+-------------------+------+
```

