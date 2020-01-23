import numpy as np

from dal.service import DalService


# this function will always return current price
# because Rfq qty will "never" be above MDV21
def answer_rfq(rfq):
    hist_prices = DalService.get_prices(rfq.get_sym()).iloc[-20:]
    mean_price = float(np.mean(hist_prices))

    hist_prices_30 = DalService.get_prices(rfq.get_sym()).iloc[-30:]
    mean_price_30 = float(np.mean(hist_prices_30))
    std_price_30 = float(np.std(hist_prices_30))

    hist_prices_10 = DalService.get_prices(rfq.get_sym()).iloc[-10:]
    mean_price_10 = float(np.mean(hist_prices_10))

    hist_volume = DalService.get_volumes(rfq.get_sym()).iloc[-20:]
    med_volume = float(np.median(hist_volume))

    param = 0.2
    skew_mova = skew_parameters(mean_price_10, mean_price_30, std_price_30)
    # skew_mom = float(momentum(rfq))

    price_stock_hist = DalService.get_prices(rfq.get_sym())
    pr_ret = price_stock_hist.pct_change()

    sign = np.sign(np.mean(pr_ret.iloc[-2:]).values[0])
    av_ret = np.mean(pr_ret.iloc[-10:]).values[0]
    av_ret3d = np.mean(pr_ret.iloc[-2:]).values[0]

    if sign > 0:
        if av_ret3d > av_ret:
            skew_mom = float(0.002)
        else:
            skew_mom = float(-0.001)
    else:
        if av_ret3d < av_ret:
            skew_mom = float(-0.002)
        else:
            skew_mom = float(0.001)

    if rfq.get_qty() < 0:
        if abs(rfq.get_qty()) > med_volume:
            return DalService.get_prices(rfq.get_sym()).iloc[-1].values[0] * (1 - (param + 0.6) * mean_price) * (
                    1 + skew_mova) * (1 + skew_mom)
        else:
            return DalService.get_prices(rfq.get_sym()).iloc[-1].values[0] * (1 + skew_mova) * (1 + skew_mom)

    else:
        if abs(rfq.get_qty()) > med_volume:
            return DalService.get_prices(rfq.get_sym()).iloc[-1].values[0] * (1 + param * mean_price) * (
                    1 + skew_mova) * (1 + skew_mom)
        else:
            return DalService.get_prices(rfq.get_sym()).iloc[-1].values[0] * (1 + skew_mova) * (1 + skew_mom)


def skew_parameters(st_mov, lt_mov, std_lt):
    skewed = 0.001
    if st_mov > lt_mov + (1.5 * std_lt):
        return float(-skewed)
    elif st_mov < lt_mov - (1.5 * std_lt):
        return float(skewed)
    else:
        return 0

# def momentum(rf):
#     pr_hist = DalService.get_prices(rf.get_sym())
#     pr_ret = pr_hist.pct_change()
#
#     sign = np.mean(pr_ret.iloc[-3:]))
#     av_ret = np.mean(pr_ret.iloc[-30:])
#     av_ret3d = np.mean(pr_ret.iloc[-3:])
#
#     if sign > 0:
#         if av_ret3d > av_ret:
#             return 0.0015
#         else:
#             return 0
#     else:
#         if av_ret3d < av_ret:
#             return 0.0015
#         else:
#             return 0

#
# def vsk(pr, rfq):
#     pr_hist = pr.get_prices(rfq.get_sym())
#     av_std = np.std(pr_hist.iloc[-30:])
#     ld_std = np.std(pr_hist.iloc[-1])
#
#     if rfq.get_qty() > 0:
#         if ld_std > av_std:
#             return -0.01
#         else:
#             return 0.001
#     else:
#         if ld_std > av_std:
#             return +0.01
#         else:
#             return -0.001
