import numpy as np
import pandas as pd
from src.log import log


class MeowFeatureGenerator(object):
    @classmethod
    def featureNames(cls):
        return [
            "ob_imb0",
            "ob_imb0_4",
            "ob_imb5_9",
            "ob_imb10_19",
            "ob_tr_imb0_4",
            "ob_tr_imb5_9",
            "ob_tr_imb10_19",
            "ob_depth_buy",
            "spread_bps0",
            "spread_bps4",
            "spread_bps9",
            "spread_bps19",
            "spread_slope",
            "micro_price",
            "mp_dev",
            "midpx_ret1",
            "trade_imb",
            "trade_count_imb",
            "trade_tvr_imb",
            "trade_vwap_sprd",
            "trade_avg_buy",
            "trade_avg_sell",
            "trade_size_ratio",
            "trade_intensity",
            "trade_hi_lo_buy",
            "trade_hi_lo_sell",
            "add_imb",
            "add_count_imb",
            "cxl_imb",
            "cxl_count_imb",
            "net_flow_buy",
            "net_flow_sell",
            "net_flow_imb",
            "add_cxl_r_buy",
            "add_cxl_r_sell",
            "add_tvr_imb",
            "trade_imb_ma5",
            "trade_imb_ma12",
            "trade_imb_std12",
            "ob_imb0_ma5",
            "ob_imb0_std12",
            "midpx_ret1_ma5",
            "midpx_ret1_ma12",
            "midpx_ret1_std12",
            "midpx_ret1_std24",
            "spread_bps0_ma12",
            "trade_intensity_ma5",
            "trade_intensity_ma12",
            "vol_ratio5",
            "vol_ratio12",
            "spread_chg5",
            "imb_chg5",
            "ret_ma_accel",
            "cx_ret1",
            "cx_relret1",
            "cx_trade_imb",
            "cx_ob_imb0",
            "lagret12",
            "imb_x_spread",
            "obi_x_ret",
            "act_x_spread",
            "obi_x_vol",
        ]

    def __init__(self, cacheDir):
        self.cacheDir = cacheDir
        self.ycol = "fret12"
        self.mcols = ["symbol", "date", "interval"]

    def _rolling_mean(self, df, col, window):
        return (
            df.set_index(["symbol", "date"])[col]
            .groupby(level=[0, 1])
            .rolling(window=window, min_periods=1)
            .mean()
            .reset_index(level=[0, 1], drop=True)
            .values
        )

    def _rolling_std(self, df, col, window):
        return (
            df.set_index(["symbol", "date"])[col]
            .groupby(level=[0, 1])
            .rolling(window=window, min_periods=1)
            .std()
            .reset_index(level=[0, 1], drop=True)
            .values
        )

    def genFeatures(self, df):
        log.inf("Generating {} features from raw data...".format(len(self.featureNames())))
        df = df.sort_values(["symbol", "date", "interval"]).reset_index(drop=True)
        eps = 1e-8

        df["ob_imb0"] = (df["asize0"] - df["bsize0"]) / (df["asize0"] + df["bsize0"] + eps)
        df["ob_imb0_4"] = (df["asize0_4"] - df["bsize0_4"]) / (df["asize0_4"] + df["bsize0_4"] + eps)
        df["ob_imb5_9"] = (df["asize5_9"] - df["bsize5_9"]) / (df["asize5_9"] + df["bsize5_9"] + eps)
        df["ob_imb10_19"] = (df["asize10_19"] - df["bsize10_19"]) / (df["asize10_19"] + df["bsize10_19"] + eps)
        df["ob_tr_imb0_4"] = (df["atr0_4"] - df["btr0_4"]) / (df["atr0_4"] + df["btr0_4"] + eps)
        df["ob_tr_imb5_9"] = (df["atr5_9"] - df["btr5_9"]) / (df["atr5_9"] + df["btr5_9"] + eps)
        df["ob_tr_imb10_19"] = (df["atr10_19"] - df["btr10_19"]) / (df["atr10_19"] + df["btr10_19"] + eps)
        df["ob_depth_buy"] = df["bsize0_4"] / (df["bsize0_4"] + df["bsize5_9"] + df["bsize10_19"] + eps)

        df["spread_bps0"] = (df["ask0"] - df["bid0"]) / (df["midpx"] + eps) * 10000
        df["spread_bps4"] = (df["ask4"] - df["bid4"]) / (df["midpx"] + eps) * 10000
        df["spread_bps9"] = (df["ask9"] - df["bid9"]) / (df["midpx"] + eps) * 10000
        df["spread_bps19"] = (df["ask19"] - df["bid19"]) / (df["midpx"] + eps) * 10000
        df["spread_slope"] = (df["spread_bps19"] - df["spread_bps0"]) / 19.0
        df["micro_price"] = (df["bid0"] * df["asize0"] + df["ask0"] * df["bsize0"]) / (df["bsize0"] + df["asize0"] + eps)
        df["mp_dev"] = (df["midpx"] - df["micro_price"]) / (df["midpx"] + eps)
        mpx_s1 = df.groupby(["symbol", "date"])["midpx"].shift(1)
        df["midpx_ret1"] = (df["midpx"] - mpx_s1) / (mpx_s1 + eps)

        df["trade_imb"] = (df["tradeBuyQty"] - df["tradeSellQty"]) / (df["tradeBuyQty"] + df["tradeSellQty"] + eps)
        df["trade_count_imb"] = (df["nTradeBuy"] - df["nTradeSell"]) / (df["nTradeBuy"] + df["nTradeSell"] + eps)
        df["trade_tvr_imb"] = (df["tradeBuyTurnover"] - df["tradeSellTurnover"]) / (df["tradeBuyTurnover"] + df["tradeSellTurnover"] + eps)
        df["trade_vwap_sprd"] = (df["buyVwad"] - df["sellVwad"]) / (df["midpx"] + eps)
        df["trade_avg_buy"] = df["tradeBuyQty"] / (df["nTradeBuy"] + eps)
        df["trade_avg_sell"] = df["tradeSellQty"] / (df["nTradeSell"] + eps)
        df["trade_size_ratio"] = df["trade_avg_buy"] / (df["trade_avg_sell"] + eps)
        df["trade_intensity"] = df["nTradeBuy"] + df["nTradeSell"]
        df["trade_hi_lo_buy"] = (df["tradeBuyHigh"] - df["tradeBuyLow"]) / (df["midpx"] + eps)
        df["trade_hi_lo_sell"] = (df["tradeSellHigh"] - df["tradeSellLow"]) / (df["midpx"] + eps)

        df["add_imb"] = (df["addBuyQty"] - df["addSellQty"]) / (df["addBuyQty"] + df["addSellQty"] + eps)
        df["add_count_imb"] = (df["nAddBuy"] - df["nAddSell"]) / (df["nAddBuy"] + df["nAddSell"] + eps)
        df["cxl_imb"] = (df["cxlBuyQty"] - df["cxlSellQty"]) / (df["cxlBuyQty"] + df["cxlSellQty"] + eps)
        df["cxl_count_imb"] = (df["nCxlBuy"] - df["nCxlSell"]) / (df["nCxlBuy"] + df["nCxlSell"] + eps)
        df["net_flow_buy"] = df["addBuyQty"] - df["cxlBuyQty"]
        df["net_flow_sell"] = df["addSellQty"] - df["cxlSellQty"]
        df["net_flow_imb"] = (df["net_flow_buy"] - df["net_flow_sell"]) / (df["net_flow_buy"].abs() + df["net_flow_sell"].abs() + eps)
        df["add_cxl_r_buy"] = df["addBuyQty"] / (df["addBuyQty"] + df["cxlBuyQty"] + eps)
        df["add_cxl_r_sell"] = df["addSellQty"] / (df["addSellQty"] + df["cxlSellQty"] + eps)
        df["add_tvr_imb"] = (df["addBuyTurnover"] - df["addSellTurnover"]) / (df["addBuyTurnover"] + df["addSellTurnover"] + eps)

        df["trade_imb_ma5"] = self._rolling_mean(df, "trade_imb", 5)
        df["trade_imb_ma12"] = self._rolling_mean(df, "trade_imb", 12)
        df["trade_imb_std12"] = self._rolling_std(df, "trade_imb", 12)
        df["ob_imb0_ma5"] = self._rolling_mean(df, "ob_imb0", 5)
        df["ob_imb0_std12"] = self._rolling_std(df, "ob_imb0", 12)
        df["midpx_ret1_ma5"] = self._rolling_mean(df, "midpx_ret1", 5)
        df["midpx_ret1_ma12"] = self._rolling_mean(df, "midpx_ret1", 12)
        df["midpx_ret1_std12"] = self._rolling_std(df, "midpx_ret1", 12)
        df["midpx_ret1_std24"] = self._rolling_std(df, "midpx_ret1", 24)
        df["spread_bps0_ma12"] = self._rolling_mean(df, "spread_bps0", 12)
        df["trade_intensity_ma5"] = self._rolling_mean(df, "trade_intensity", 5)
        df["trade_intensity_ma12"] = self._rolling_mean(df, "trade_intensity", 12)

        df["vol_ratio5"] = df["trade_intensity"] / (df["trade_intensity_ma5"] + eps)
        df["vol_ratio12"] = df["trade_intensity"] / (df["trade_intensity_ma12"] + eps)
        df["spread_chg5"] = df["spread_bps0"] - df.groupby(["symbol", "date"])["spread_bps0"].shift(5)
        df["imb_chg5"] = df["trade_imb"] - df.groupby(["symbol", "date"])["trade_imb"].shift(5)
        df["ret_ma_accel"] = df["midpx_ret1_ma5"] - df["midpx_ret1_ma12"]

        df["cx_ret1"] = df.groupby("interval")["midpx_ret1"].transform("mean")
        df["cx_relret1"] = df["midpx_ret1"] - df["cx_ret1"]
        df["cx_trade_imb"] = df["trade_imb"] - df.groupby("interval")["trade_imb"].transform("mean")
        df["cx_ob_imb0"] = df["ob_imb0"] - df.groupby("interval")["ob_imb0"].transform("mean")

        bret12_s = df.groupby(["symbol", "date"])["midpx"].shift(12)
        df["bret12"] = (df["midpx"] - bret12_s) / (bret12_s + eps)
        cxbret = df.groupby("interval")[["bret12"]].mean().reset_index().rename(columns={"bret12": "cx_bret12"})
        df = df.merge(cxbret, on="interval", how="left")
        df["lagret12"] = df["bret12"] - df["cx_bret12"]

        df["imb_x_spread"] = df["trade_imb"] * df["spread_bps0"]
        df["obi_x_ret"] = df["ob_imb0"] * df["midpx_ret1"]
        df["act_x_spread"] = df["trade_intensity"] * df["spread_bps0"]
        df["obi_x_vol"] = df["ob_imb0"] * df["midpx_ret1_std12"]

        xdf = df[self.mcols + self.featureNames()].set_index(self.mcols)
        ydf = df[self.mcols + [self.ycol]].set_index(self.mcols)
        return xdf.fillna(0), ydf.fillna(0)
