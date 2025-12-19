# lvl 1 to lvl 2 already assumed finished
# assume going up to 100/100

success_rates = [0.6, 0.5, 0.4, 0.307, 0.205, 0.153, 0.055]

fail_rates = [0.4, 0.5, 0.6, 0.693, 0.765, 0.817, 0.915]

lost_rates = [0, 0, 0, 0, 0.03, 0.03, 0.03]

trade_type = "frag" # set to energy, frag, or exp. Unrecognized treated as exp.

if trade_type == "energy":
    payout = [4, 12, 24, 40, 60, 100, 600, 2000] # TODO: confirm that 1 sol erda = 100 faint sol erda energy
elif trade_type == "frag":
    payout = [1, 3, 6, 10, 15, 25, 150, 500]
else:
    payout = [20, 60, 120, 200, 300, 500, 3000, 9999]


ev = [] # ev[amt_trades][tier] = expected value of being at amt_trades + 2 and tier + 2.
for amt_trades in range(98):
    ev.append([])
    for tier in range(8):
        ev[-1].append(0)
ev.append(payout)

for amt_trades in range(98):
    ev[amt_trades][7] = payout[7]

for amt_trades in range(97, -1, -1):
    for tier in range(7):
        if tier == 0:
            fail_ev = ev[amt_trades + 1][0]
        else:
            fail_ev = ev[amt_trades + 1][tier - 1]
        roll_ev = success_rates[tier] * ev[amt_trades + 1][tier + 1] + fail_rates[tier] * fail_ev + lost_rates[tier] * ev[amt_trades + 1][0]
        ev[amt_trades][tier] = max(payout[tier], roll_ev)

# at 0 (2) trades, highest posssible is tier 1 (3)
# last impossible case is at 5 (7) trades, with highest possible tier being 6 (8), and tier 7 (9) being impossible 
for amt_trades in range(6):
    for impossible_tier in range(amt_trades + 2, 8):
        ev[amt_trades][impossible_tier] = "Not Poss."

for amt, evs in enumerate(ev):
    print(f"{amt + 2}/100", end=" ")
    print([e if isinstance(e, str) else f"{e:.4f}" for e in evs ])

# since all payouts have the same ratios (except 2000 * 5 =/= 9999), all solutions have the same pattern:
# always settle tier 8
# never settle tier 7
# settle at tier 6 if at 96/100 or later
# settle at tier 5 if at 91/100 or later
# settle at tier 4 if at 99/100
# never settle tier 3 or tier 2
