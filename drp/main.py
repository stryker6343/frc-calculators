# from itertools import accumulate
import json
import scipy.special
# from ba_alliance_selection import get_blue_alliance_data

NUM_TEAMS = 36
# ALLIANCE_SELECTION = get_blue_alliance_data()


def qrp(rank: int, num_teams: int) -> int:
    alpha = 1.07
    x = (num_teams - 2 * rank + 2) / alpha / num_teams
    return round(scipy.special.erfinv(x) * 10 / scipy.special.erfinv(1/alpha) + 12)


def asp(alliance: int, pick: int):
    if pick == 2:
        return alliance
    elif pick >= 0:
        return 17-alliance
    else:
        return 0


# for i in range(1,29):
#     print(i, qrp(i, 28))

# results = {}
# for rank in range(1, NUM_TEAMS+1):
#     a = qrp(rank, NUM_TEAMS)
#     b = 0
#     for selection in ALLIANCE_SELECTION[rank].keys():
#         num_0 = ALLIANCE_SELECTION[rank][selection].count(0)
#         num_1 = ALLIANCE_SELECTION[rank][selection].count(1)
#         num_2 = ALLIANCE_SELECTION[rank][selection].count(2)
#         b += (17 - selection) * (num_0 + num_1) / den
#         b += selection * num_2 / den
#     results[rank] = a + b

# print("Average District Points Earned")
# print("Qualification Matches at Qualification Events")
# print("---------------------------------------------")
# for i in sorted(results.keys()):
#     print(f"Qual Rank: {i}, {results[i]:3.1f} pts")

# print()
print("Qual. Rank,Alliance,Pick,%,Qual. Perf. Pts.,All. Sel. Pts.,Total Pts,Part. Prod.")

with open("alliance_selection_data.json", "r") as f:
    alliance_selection_data = json.load(f, parse_int=int)

minimums = {}
averages = {}
for rank in sorted(alliance_selection_data.keys(), key=int):
    if int(rank) <= NUM_TEAMS:
        totals = []
        partial_products = []
        num_samples = 0
        for selection in sorted(alliance_selection_data[rank].keys(), key=int):
            num_samples += sum([alliance_selection_data[rank][selection].count(i) for i in range(-1, 3)])
        for selection in sorted(alliance_selection_data[rank].keys(), key=int):
            counts = [alliance_selection_data[rank][selection].count(i) for i in range(-1, 3)]
            for i, count in enumerate(counts):
                if count > 0:
                    percentile = count / num_samples
                    qr_pts = qrp(int(rank), NUM_TEAMS+1)
                    as_pts = asp(int(selection), i-1)
                    total_pts = qr_pts + as_pts
                    partial_product = percentile * total_pts
                    totals.append(total_pts)
                    print(f"{rank},{selection},{i},{100*percentile:3.2f}%,{qr_pts},{as_pts},{total_pts},{partial_product}")
                    partial_products.append(partial_product)
        minimums[int(rank)] = min(totals)
        averages[int(rank)] = sum(partial_products)

print()
print("Rank,QRP,Min,Mean")
for rank in sorted(averages.keys()):
    print(f"{rank},{qrp(rank, NUM_TEAMS+1)},{minimums[rank]},{averages[rank]:0.2f}")
