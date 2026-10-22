"""Render filtered Google Sheet data as an auto-sized PNG. Settings come from config.yaml."""
import json
import os
import sys

import gspread
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import yaml


def get_client():
    # In GitHub Actions the key comes from the GOOGLE_CREDENTIALS secret.
    raw = os.environ.get("GOOGLE_CREDENTIALS")
    if raw:
        return gspread.service_account_from_dict(json.loads(raw))
    return gspread.service_account(filename="credentials.json")  # local runs


def load_data(cfg) -> pd.DataFrame:
    sh = get_client().open_by_key(cfg["sheet_id"])
    ws = sh.worksheet(cfg["worksheet"]) if cfg.get("worksheet") else sh.sheet1
    return pd.DataFrame(ws.get_all_records())


def apply_config(df, cfg):
    for col, val in (cfg.get("filters") or {}).items():
        df = df[df[col].astype(str).str.strip() == str(val).strip()]
    if cfg.get("columns"):
        df = df[cfg["columns"]]
    return df


def render(df, out, title):
    df = df.astype(str)
    char_w, row_h = 0.11, 0.38
    widths = [max(df[c].map(len).max(), len(c)) * char_w + 0.4 for c in df.columns]
    fig_w = max(sum(widths), 3)
    fig_h = row_h * (len(df) + 1) + (0.6 if title else 0.2)

    fig, ax = plt.subplots(figsize=(fig_w, fig_h))
    ax.axis("off")
    tbl = ax.table(cellText=df.values, colLabels=df.columns,
                   colWidths=[w / fig_w for w in widths],
                   cellLoc="left", loc="upper center")
    tbl.auto_set_font_size(False)
    tbl.set_fontsize(10)
    tbl.scale(1, 1.4)
    for (r, _), cell in tbl.get_celld().items():
        cell.set_edgecolor("#cccccc")
        if r == 0:
            cell.set_facecolor("#1f4e79")
            cell.set_text_props(color="white", weight="bold")
        elif r % 2 == 0:
            cell.set_facecolor("#f3f6fa")
    if title:
        ax.set_title(title, fontsize=12, weight="bold", pad=8)

    os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
    fig.savefig(out, dpi=200, bbox_inches="tight", pad_inches=0.1)
    plt.close(fig)
    print(f"Saved {out} ({len(df)} rows)")


def main():
    with open("config.yaml") as f:
        cfg = yaml.safe_load(f)
    df = apply_config(load_data(cfg), cfg)
    if df.empty:
        sys.exit("No rows match the filters in config.yaml")
    render(df, cfg.get("output", "output/latest.png"), cfg.get("title"))


if __name__ == "__main__":
    main()
