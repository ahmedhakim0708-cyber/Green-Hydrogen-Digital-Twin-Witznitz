import matplotlib.pyplot as plt


def plot_monthly_balance(df, path=None):
    """Monthly PV, grid import/export and hydrogen production."""
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)

    ax1.bar(df["Month"], df["PV_to_electrolyzer_kWh"] / 1e6, label="PV -> electrolyzer")
    ax1.bar(df["Month"], df["Grid_import_kWh"] / 1e6,
            bottom=df["PV_to_electrolyzer_kWh"] / 1e6, label="Grid import")
    ax1.plot(df["Month"], df["Grid_export_kWh"] / 1e6, "k--o", label="Grid export")
    ax1.set_ylabel("Energy (GWh)")
    ax1.set_title("Monthly energy balance")
    ax1.legend()
    ax1.grid(axis="y", linestyle="--", alpha=0.5)

    ax2.bar(df["Month"], df["Hydrogen_kg"] / 1_000, color="tab:green")
    ax2.set_ylabel("Hydrogen (t)")
    ax2.set_title("Monthly hydrogen production")
    ax2.grid(axis="y", linestyle="--", alpha=0.5)

    fig.tight_layout()
    if path:
        fig.savefig(path, dpi=300)
    return fig


def plot_lcoh_breakdown(breakdown, path=None, title="LCOH decomposition"):
    items = {k: v for k, v in breakdown.items() if k != "LCOH"}
    fig, ax = plt.subplots(figsize=(9, 4))
    colors = ["tab:red" if v < 0 else "tab:blue" for v in items.values()]
    ax.barh(list(items.keys()), list(items.values()), color=colors)
    ax.axvline(0, color="black", linewidth=0.8)
    ax.set_xlabel("EUR / kg H2")
    ax.set_title(f"{title} - total {breakdown['LCOH']:.2f} EUR/kg")
    fig.tight_layout()
    if path:
        fig.savefig(path, dpi=300)
    return fig


def plot_tornado(results, base, path=None, target=4.5):
    """results: list of (label, lcoh_low, lcoh_high)."""
    results = sorted(results, key=lambda r: abs(r[2] - r[1]))
    fig, ax = plt.subplots(figsize=(9, 4))
    for i, (label, low, high) in enumerate(results):
        ax.barh(i, low - base, left=base, color="tab:green")
        ax.barh(i, high - base, left=base, color="tab:red")
    ax.set_yticks(range(len(results)))
    ax.set_yticklabels([r[0] for r in results])
    ax.axvline(base, color="black", linewidth=0.8, label=f"Base {base:.2f}")
    ax.axvline(target, color="tab:orange", linestyle="--", label=f"Target {target}")
    ax.set_xlabel("LCOH (EUR/kg)  -  green: -20 %, red: +20 %")
    ax.set_title("Sensitivity analysis")
    ax.legend()
    fig.tight_layout()
    if path:
        fig.savefig(path, dpi=300)
    return fig
