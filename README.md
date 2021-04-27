# Problem Domain

_Create an application than takes in customer requests (in JSON format) containing customer home insurance
request data and returns quote premiums. Here is an example of a customer request:_

```shell
{
  "CustomerID": 233,
  "DwellingCoverage": 30200,
  "HomeAge": 108,
  "RoofType": "Tin",
  "NumberOfUnits": 4,
  "PartnerDiscount": "N"
}
```

- #### Factors for Dwelling Coverage calculated through linearly interpolated.

#### Output:
```shell
{
  "success": true,
  "final_premium": 1467
}
```

### Technology:
```shell
  - Python
  - Django Rest Framewoek
```

### Setup
- Tested under `Python 3+` versions
- run `pip install -r requirements.txt`
- run `./manage.py runserver`

As swagger is introduced to execute apis, simply go to 
```sh 
http://127.0.0.1:8000/api/doc/
```