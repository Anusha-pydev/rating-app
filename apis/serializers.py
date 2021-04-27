from rest_framework import serializers
from apis import utils


class QuoteSerializer(serializers.Serializer):
    """
    Quote Request Parameters defined here.
    """
    BASE_PREMIUM = 350
    ROOF_TYPE = {"Asphalt Shingles": 1.0, "Tin": 1.70, "Wood": 2.0}
    NUM_UNITS = {1: 1.0, 2: 0.8, 3: 0.8, 4: 0.8}
    DWELLING_COVERAGE = (
        [100000, 150000, 200000, 250000, 300000, 350000],
        [0.971, 1.104, 1.314, 1.471, 1.579, 1.761],
    )
    HOME_AGE = {"0-10": 1, "11-35": 1.5, "36-100": 1.80, "100+": 1.95}
    DISCOUNT = 0.05

    CustomerID = serializers.IntegerField(min_value=1)
    DwellingCoverage = serializers.IntegerField(min_value=100000)
    HomeAge = serializers.IntegerField(min_value=0)
    RoofType = serializers.ChoiceField(
        (("Asphalt Shingles", "Asphalt Shingles"), ("Tin", "Tin"), ("Wood", "Wood"))
    )
    NumberOfUnits = serializers.ChoiceField(choices=range(1, 5))
    PartnerDiscount = serializers.ChoiceField(choices=(("Y", "Yes"), ("N", "No")))

    def calculate_premium(self, data):
        """
        calculate Premium based on quote parameters
        :param data:
        :return:
        """
        interpolate = utils.Interpolate(*self.DWELLING_COVERAGE)
        interpolate_covergae = interpolate(data["DwellingCoverage"])
        roof_factor = self.ROOF_TYPE[data["RoofType"]]
        unit_factor = self.NUM_UNITS[data["NumberOfUnits"]]

        if 0 <= data["HomeAge"] < 11:
            home_age_key = "0-10"
        elif 11 <= data["HomeAge"] < 36:
            home_age_key = "11-35"
        elif 36 <= data["HomeAge"] < 100:
            home_age_key = "36-100"
        elif data["HomeAge"] > 100:
            home_age_key = "100+"
        else:
            raise ValueError("Invalid HomeAge Value")

        monthly_premium = (
            self.BASE_PREMIUM
            * interpolate_covergae
            * roof_factor
            * unit_factor
            * self.HOME_AGE[home_age_key]
        )
        if data["PartnerDiscount"] == "Y":
            discount = monthly_premium * self.DISCOUNT
            monthly_premium = monthly_premium - discount

        return monthly_premium
