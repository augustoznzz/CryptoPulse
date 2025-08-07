import pandas as pd
import numpy as np
from technical_indicators import TechnicalIndicators


def create_trending_df(length=50, start=1, step=1, volume=1000):
    close = pd.Series(np.arange(start, start + length * step, step), dtype=float)
    high = close + 0.5
    low = close - 0.5
    volume_series = pd.Series(volume, index=close.index, dtype=float)
    return pd.DataFrame({
        'high': high,
        'low': low,
        'close': close,
        'volume': volume_series
    })


def test_stochastic_oscillator_bounds():
    df = create_trending_df(30)
    ti = TechnicalIndicators()
    stoch = ti.stochastic_oscillator(df['high'], df['low'], df['close'])
    valid = stoch['stoch_k'].dropna()
    assert valid.between(0, 100).all()
    assert valid.iloc[-1] > 80


def test_ichimoku_cloud_positive():
    df = create_trending_df(100)
    ti = TechnicalIndicators()
    cloud = ti.ichimoku_cloud(df['high'], df['low'], df['close'])
    assert cloud['ichimoku_span_a'].iloc[-1] > cloud['ichimoku_span_b'].iloc[-1]


def test_vwap_basic():
    df = pd.DataFrame({
        'high': [10, 11, 12],
        'low': [9, 10, 11],
        'close': [9.5, 10.5, 11.5],
        'volume': [100, 150, 200]
    })
    ti = TechnicalIndicators()
    vwap_val = ti.vwap(df).iloc[-1]
    expected = (((10 + 9 + 9.5) / 3 * 100) + ((11 + 10 + 10.5) / 3 * 150) + ((12 + 11 + 11.5) / 3 * 200)) / (100 + 150 + 200)
    assert abs(vwap_val - expected) < 1e-6


def test_obv_trend():
    df = pd.DataFrame({
        'close': [1, 2, 3, 2, 3],
        'volume': [100, 100, 100, 100, 100],
        'high': [1.5, 2.5, 3.5, 2.5, 3.5],
        'low': [0.5, 1.5, 2.5, 1.5, 2.5]
    })
    ti = TechnicalIndicators()
    obv = ti.on_balance_volume(df['close'], df['volume'])
    assert obv.iloc[-1] > 0


def test_parabolic_sar_trend():
    df = create_trending_df(10)
    ti = TechnicalIndicators()
    psar = ti.parabolic_sar(df['high'], df['low'])
    assert psar.iloc[-1] < df['low'].iloc[-1]


def test_adx_threshold():
    df = create_trending_df(40)
    ti = TechnicalIndicators()
    adx_data = ti.adx(df['high'], df['low'], df['close'])
    assert adx_data['adx'].iloc[-1] > 25


def test_chaikin_oscillator_volume_spike():
    close = pd.Series(np.linspace(1, 20, 20))
    high = close + 1
    low = close - 2
    volume = pd.Series(100, index=close.index)
    volume.iloc[15:] = 5000
    df = pd.DataFrame({'high': high, 'low': low, 'close': close, 'volume': volume})
    ti = TechnicalIndicators()
    chaikin = ti.chaikin_oscillator(df['high'], df['low'], df['close'], df['volume'])
    assert chaikin.iloc[-1] > 0


def test_williams_r_bounds():
    ti = TechnicalIndicators()
    df_up = create_trending_df(30)
    wr_high = ti.williams_r(df_up['high'], df_up['low'], df_up['high'])
    assert wr_high.iloc[-1] > -20
    df_down = create_trending_df(30).iloc[::-1].reset_index(drop=True)
    wr_low = ti.williams_r(df_down['high'], df_down['low'], df_down['close'])
    assert wr_low.iloc[-1] < -80
