# Currency exchange (by Pryvate Bank)

This is a console application.

### 1. Default mode

By default you can use the command:

`python3 main.py N`

where `N` is a number of past days that have to be shown.
By default `N = 1` and it couldn't be more than `10`. As the result you will get JSON:

```
[
    {
        '24.07.2023': [
        {
            'baseCurrency': 'UAH', 
            'currency': 'AUD',
            'saleRateNB': 24.629,
            'purchaseRateNB': 24.629},
        {
            'baseCurrency': 'UAH',
            'currency': 'EUR',
            'saleRateNB': 40.6643,
            'purchaseRateNB': 40.6643,
            'saleRate': 41.6,
            'purchaseRate': 40.6},
        {
            'baseCurrency': 'UAH',
            'currency': 'USD',
            'saleRateNB': 36.5686,
            'purchaseRateNB': 36.5686,
            'saleRate': 37.15,
            'purchaseRate': 36.55}
            ]}
    }
]        
```

### 2. Table mode

If you use flag `-t` it transform the output into table:

```commandline
                             =====================================================================================
                             |              National Bank              |              Private Bank               |
==================================================================================================================
|    Date    |   Currency    |     Sale rate     |    Purchase rate    |     Sale rate     |    Purchase rate    |
==================================================================================================================
| 24.07.2023 |      AUD      |      24.629       |       24.629        |         -         |          -          |
| 24.07.2023 |      EUR      |      40.6643      |       40.6643       |       41.6        |        40.6         |
| 24.07.2023 |      USD      |      36.5686      |       36.5686       |       37.15       |        36.55        |
==================================================================================================================
| 25.07.2023 |      AUD      |      24.6619      |       24.6619       |         -         |          -          |
| 25.07.2023 |      EUR      |      40.5838      |       40.5838       |       41.7        |        40.7         |
| 25.07.2023 |      USD      |      36.5686      |       36.5686       |       37.3        |        36.7         |
==================================================================================================================

```

### 3. Expert mode

You can use the command:

`python3 main.py 2 -t -c USD, AUD`

where `-c` additional parameter that takes name of currency. By default `['USD', 'EUR']`. and it couldn't be more than `10`.
You max mixed it with table mode.
