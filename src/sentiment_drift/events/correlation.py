from __future__ import annotations

from datetime import timedelta

import pandas as pd


def correlate_changepoints_to_events(
    changepoints: pd.DataFrame,
    events: pd.DataFrame,
    max_window: timedelta = timedelta(hours=12),
) -> pd.DataFrame:
    if changepoints.empty:
        return changepoints.copy()

    cp = changepoints.copy()
    cp["changepoint_timestamp"] = pd.to_datetime(cp["changepoint_timestamp"], utc=True)

    if events.empty:
        cp["nearest_event"] = None
        cp["time_difference"] = None
        cp["event_type"] = None
        return cp

    ev = events.copy()
    ev["timestamp"] = pd.to_datetime(ev["timestamp"], utc=True)

    nearest_event = []
    time_diff = []
    event_type = []

    for ts in cp["changepoint_timestamp"]:
        deltas = (ev["timestamp"] - ts).abs()
        idx = deltas.idxmin()
        if deltas.loc[idx] <= pd.Timedelta(max_window):
            nearest_event.append(ev.loc[idx, "event_name"])
            time_diff.append(ev.loc[idx, "timestamp"] - ts)
            event_type.append(ev.loc[idx, "event_type"])
        else:
            nearest_event.append(None)
            time_diff.append(None)
            event_type.append(None)

    cp["nearest_event"] = nearest_event
    cp["time_difference"] = time_diff
    cp["event_type"] = event_type
    return cp
