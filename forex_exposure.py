import matplotlib.pyplot as plt
import numpy as np

import volatilityProbability as vp


def forex_exposure(usdcash: float, eurusd_price: float, eurusd_vol: float, limits=(-2, 2), period=365):
    usdcash = float(usdcash)
    eurusd_price_next = np.arange(
        vp.sd2price(np.array([limits[0]]), np.array([eurusd_price]), np.array([eurusd_vol]), np.array([period])),
        vp.sd2price(np.array([limits[1]]), np.array([eurusd_price]), np.array([eurusd_vol]), np.array([period])), 0.001)

    eur_value0 = usdcash / eurusd_price
    eur_value1 = usdcash / eurusd_price_next

    eur_value_chg = eur_value1 - eur_value0
    delta = usdcash / (1.01 * eurusd_price) - eur_value0
    figObj = plt.figure()  # figsize=(16,9))
    plt.plot(eurusd_price_next, eur_value_chg)
    axes_eurusd = figObj.axes[0]
    ylim0 = np.min(eur_value_chg)
    ylim1 = np.max(eur_value_chg)
    xlim0 = np.min(eurusd_price_next)
    xlim1 = np.max(eurusd_price_next)
    axes_eurusd.set_ylim(ylim0, ylim1)
    axes_eurusd.set_xlim(xlim0, xlim1)
    axes_eurusd.set_xlabel('EUR/USD (+- 2 SD)')
    axes_eurusd.set_ylabel('EUR Value Change')
    # plt.hold(True)
    plt.plot([eurusd_price, eurusd_price], [ylim0, ylim1], '-.', color='0.5')
    plt.plot([xlim0, xlim1], [0, 0], color='0.75')
    # plt.hold(False)
    axes_eurusd.legend(['Value Change (EUR)', 'CurrentRate'])
    axes_eurusd.set_title('FOREX Exposure')
    string0 = "USD Amount: {:8.8g} $\nCurrent Rate: {:8.5} $/€\nDelta: {:20.2f} €".format(usdcash, eurusd_price,
                                                                                                 delta)
    plt.annotate(string0, xy=(0.7, 0.93), xycoords='axes fraction')

    # window_manager = plt.get_current_fig_manager()
    # window_manager.window.wm_geometry("1820x950-1920+50")
    plt.show()
    return figObj


if __name__ == '__main__':
    usdcash = 20300
    eurusd = 1.251
    eurusd_vol = 0.0826

    forex_exposure(usdcash,eurusd,eurusd_vol)