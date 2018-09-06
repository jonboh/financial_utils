import numpy as np


def tick2ret(tick_table):
    ticks = tick_table.Tick
    returns = np.nan * np.ones((len(ticks) - 1, 1))
    for i in range(0, len(ticks) - 1):
        returns[i] = ticks[i + 1] / ticks[i] - 1
    return returns

def tick2ret_pivoted(tick_table):
	ticks = tick_table.Tick
	other_ticks = tick_table.drop(["Tick","Date"], axis=1)
	returns = np.nan * np.ones((len(ticks) - 1, 1))
	other_returns = np.nan * np.ones((len(ticks) - 1, other_ticks.shape[1]))
	for i in range(0, len(ticks)-1):
		returns[i] = ticks[i + 1] / ticks[i] - 1
		for j in range(0, other_ticks.shape[1]):
			other_returns[i,j] = other_ticks.iloc[i+1][j] / ticks[i] -1		
	return returns, other_returns


def tick2ret_ann(tick_table, base=365):
    returns = tick2ret(tick_table)
    datediff = tick_table.Date.diff().apply(lambda x: x.total_seconds() / 60 / 60 / 24).as_matrix()[1:]
    datediff = datediff.reshape(returns.shape)
    returns_ann = (returns + 1) ** (base * datediff) - 1
    return returns_ann

			
def maxdrawdown(tick_table):
    ticks = tick_table.Tick.as_matrix()
    unscaled = np.log(ticks)
    i = np.argmax(np.maximum.accumulate(unscaled) - unscaled)  # end of the period
    j = np.argmax(unscaled[:i])  # start of period
    maxdrawdown = ticks[i] / ticks[j] - 1
    return maxdrawdown


def annual_return(tick_table, base=365):
    dates = tick_table.Date
    returns = tick2ret(tick_table)
    totalreturns = np.prod(returns + 1)
    ann_ret = totalreturns ** (1 / (dates[len(dates) - 1] - dates[0]).total_seconds() * 60 * 60 * 24 * base) - 1
    return ann_ret


def calmarR(tick_table, r=0):
    ann_return = annual_return(tick_table)
    maxdrawd = maxdrawdown(tick_table)
    calmar = (ann_return - r) / np.abs(maxdrawd)
    return calmar


def sharpeR(tick_table, r=0, base=365):
    ret = tick2ret(tick_table)
    datediff = tick_table.Date.diff().apply(lambda x: x.total_seconds() / 60 / 60 / 24).as_matrix()[1:]
    datediff = datediff.reshape(ret.shape)
    r_adj = (r + 1) ** (1 / (base / datediff)) - 1
    sharpe = np.mean(ret - r_adj) / np.std(ret - r_adj) * np.sqrt(base)
    return sharpe
