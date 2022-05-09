

class PrecisionMeasurements:

    def GetPrecision(rr, ri):
        return rr / (rr + ri)

    def GetRecovered(rr, nr):
        return rr / (rr + nr)

    def GetMearureF(precision, recovered, beta=1):
        return (1 + beta ** 2) / ((1 / precision) + ((beta ** 2) / recovered))

    def GetMearureF1(precision, recovered):
        return 2 / ((1 / precision) + (1 / recovered))
