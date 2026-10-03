"""
Levelized Cost of Hydrogen - discounted cash flow method (IRENA 2020),
as defined in section 3.3 / 5.2 of the thesis:

    LCOH = sum_t (CAPEX_t + OPEX_t + GridCost_t + Repl_t) / (1+r)^t
           -------------------------------------------------------
                       sum_t H_t / (1+r)^t
"""
import numpy as np

from data import parameters as p


def lcoh(capex_eur, h2_kg_per_year, net_grid_cost_eur_per_year,
         opex_eur=p.OPEX_EUR_PER_YEAR, wacc=p.WACC,
         lifetime=p.PROJECT_LIFETIME_YEARS, opex_escalation=p.OPEX_ESCALATION,
         replacements=p.REPLACEMENTS):
    """
    capex_eur                  : total CAPEX in year 0
    h2_kg_per_year             : array (length = lifetime) of H2 output per year
    net_grid_cost_eur_per_year : array, import cost - export revenue (negative = revenue)
    Returns a dict with the LCOH and its decomposition in EUR/kg.
    """
    t = np.arange(1, lifetime + 1)
    df = (1 + wacc) ** -t
    h2 = np.asarray(h2_kg_per_year, dtype=float)
    grid = np.asarray(net_grid_cost_eur_per_year, dtype=float)

    h2_disc = np.sum(h2 * df)
    opex_disc = np.sum(opex_eur * (1 + opex_escalation) ** (t - 1) * df)
    grid_disc = np.sum(grid * df)

    result = {
        "CAPEX": capex_eur / h2_disc,
        "OPEX": opex_disc / h2_disc,
        "Net grid electricity": grid_disc / h2_disc,
    }
    for year, cost, label in replacements:
        result[label] = cost / (1 + wacc) ** year / h2_disc
    result["LCOH"] = sum(result.values())
    return result


def grid_cost_series(import_mwh, export_mwh, lifetime=p.PROJECT_LIFETIME_YEARS,
                     import_price=p.GRID_IMPORT_PRICE_EUR_PER_MWH,
                     export_price=p.GRID_EXPORT_PRICE_EUR_PER_MWH,
                     escalation=p.GRID_PRICE_ESCALATION):
    """Net grid cost per year (EUR). Scalars are repeated for every year."""
    t = np.arange(1, lifetime + 1)
    imp = np.broadcast_to(np.asarray(import_mwh, dtype=float), t.shape)
    exp = np.broadcast_to(np.asarray(export_mwh, dtype=float), t.shape)
    esc = (1 + escalation) ** (t - 1)
    return (imp * import_price - exp * export_price) * esc


def thesis_reproduction():
    """Reproduces Table 13 of the thesis with the inputs of Table 12."""
    t = np.arange(1, p.PROJECT_LIFETIME_YEARS + 1)
    h2 = p.THESIS_H2_T_PER_YEAR * 1_000 * (1 - p.PV_DEGRADATION_PER_YEAR) ** (t - 1)
    grid = grid_cost_series(p.THESIS_IMPORT_GWH * 1_000, p.THESIS_EXPORT_GWH * 1_000)
    return lcoh(sum(p.CAPEX_EUR.values()), h2, grid)


def sensitivity(base_kwargs, parameters, variation=0.2):
    """
    One-at-a-time sensitivity analysis.
    base_kwargs : dict passed to `func` (key 'func' = callable returning LCOH)
    parameters  : list of keyword names to vary by +/- variation
    Returns a list of (parameter, LCOH_low, LCOH_high).
    """
    func = base_kwargs["func"]
    kwargs = {k: v for k, v in base_kwargs.items() if k != "func"}
    out = []
    for name in parameters:
        low = dict(kwargs, **{name: kwargs[name] * (1 - variation)})
        high = dict(kwargs, **{name: kwargs[name] * (1 + variation)})
        out.append((name, func(**low), func(**high)))
    return out
