"""Visualization of election outcomes under different voting schemes."""

from collections import defaultdict
from copy import deepcopy
from glob import glob
from itertools import chain
import random

from matplotlib import pyplot as plt

from pref import VoterPreferences


def make_bar_chart(
    x,
    heights,
    title,
    xlabel,
    ylabel,
    output_file,
):
    """Make a bar chart."""
    color = [random.random(), random.random(), random.random()]
    colors = list(
        map(lambda height: color + [max((height / max(heights))**3, 0.25)],
            heights))

    rects = plt.bar(x, heights, color=colors).patches

    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

    for rect, label in zip(rects, heights):
        plt.text(
            rect.get_x() + rect.get_width() / 2,
            rect.get_height(),
            label,
            ha="center",
            va="bottom",
        )

    plt.savefig(output_file, dpi=400)
    plt.clf()


def plurality(vp, ):
    """Calculate outcome under plurality voting."""
    print("Plurality voting:")

    votes = defaultdict(int)
    print("\tIndividual votes:")
    for voter, preference in vp.preferences.items():
        candidate = max(
            vp.candidates,
            key=lambda candidate: preference[vp.candidates.index(candidate)])

        votes[candidate] += 1
        print(f"\t\t{voter} voted for {candidate}")

    print("\tFinal vote counts:")
    for candidate in vp.candidates:
        print(f"\t\t{candidate} received {votes[candidate]} votes")

    heights = [votes[candidate] for candidate in vp.candidates]
    make_bar_chart(vp.candidates, heights, "Outcome of Plurality Voting",
                   "Candidates", "Votes", "plurality.png")

    elected = max(vp.candidates, key=lambda candidate: votes[candidate])
    print(f"\t{elected} wins under plurality voting")


def runoff(vp, ):
    """Calculate outcome under instant-runoff voting."""
    print("Instant-runoff voting:")

    votes = defaultdict(int)
    round = 1
    candidates_remaining = deepcopy(vp.candidates)
    ended = False
    while not ended:
        print(
            f"\tRound {round} (with candidates {candidates_remaining}) individual votes:"
        )
        for voter, preference in vp.preferences.items():
            candidate = max(
                candidates_remaining,
                key=lambda cand: preference[vp.candidates.index(cand)])

            print(f"\t\t{voter} voted for {candidate}")
            votes[candidate] += 1

        print(f"\tRound {round} vote counts:")
        for candidate in candidates_remaining:
            print(f"\t\t{candidate} received {votes[candidate]} votes")

        if (any(
                map(
                    lambda vote_count: vote_count >= len(vp.preferences.keys())
                    // 2 + 1, votes.values()))):
            print(f"\tOne candidate received majority of votes, ending")
            ended = True
        else:
            heights = [votes[candidate] for candidate in candidates_remaining]
            make_bar_chart(candidates_remaining, heights,
                           f"Outcome of Instant-runoff Voting, Round {round}",
                           "Candidates Remaining", "Votes",
                           f"runoff-round_{round}.png")

            round += 1
            candidate_removed = min(candidates_remaining,
                                    key=lambda candidate: votes[candidate])
            print(f"\tCandidate {candidate_removed} removed")
            candidates_remaining.remove(candidate_removed)
            votes.clear()

    heights = [votes[candidate] for candidate in candidates_remaining]
    make_bar_chart(candidates_remaining, heights,
                   "Outcome of Instant-runoff Voting, Final Round",
                   "Candidates Remaining", "Votes", "runoff-round_final.png")

    elected = max(candidates_remaining, key=lambda candidate: votes[candidate])
    print(f"\t{elected} wins under instant-runoff voting")


def borda(vp, ):
    """Calculate outcome under Borda count voting."""
    print("Borda count voting:")

    points = defaultdict(int)
    print("\tIndividual rankings:")
    for voter, preference in vp.preferences.items():
        ranked_candidates = sorted(
            vp.candidates,
            key=lambda candidate: preference[vp.candidates.index(candidate)],
            reverse=True)

        print(
            f"\t\t{voter} ranked (from most to least preferred) {ranked_candidates}"
        )

        for index, candidate in enumerate(ranked_candidates):
            num_points = len(ranked_candidates) - 1 - index
            points[candidate] += num_points

    print("\tFinal points:")
    for candidate in vp.candidates:
        print(f"\t\t{candidate} received {points[candidate]} points")

    heights = [points[candidate] for candidate in vp.candidates]
    make_bar_chart(vp.candidates, heights, "Outcome of Borda Count Voting",
                   "Candidates", "Points", "borda.png")

    elected = max(vp.candidates, key=lambda candidate: points[candidate])
    print(f"\t{elected} wins under Borda count voting")


def approval(vp, ):
    """Calculate outcome under approval voting."""
    print("Approval voting:")

    agg_pref = list(chain(*list(vp.preferences.values())))
    avg_pref = sum(agg_pref) / len(agg_pref)
    print(
        f"\tAverage preference score of {round(avg_pref, 2)} used as baseline approval"
    )

    points = defaultdict(int)
    print("\tIndividual approvals:")
    for voter, preference in vp.preferences.items():
        approved_candidates = list(
            filter(
                lambda candidate: preference[vp.candidates.index(candidate)] >=
                avg_pref, vp.candidates))

        print(f"\t\t{voter} approved {approved_candidates}")

        for candidate in approved_candidates:
            points[candidate] += 1

    print("\tFinal points:")
    for candidate in vp.candidates:
        print(f"\t\t{candidate} received {points[candidate]} points")

    heights = [points[candidate] for candidate in vp.candidates]
    make_bar_chart(vp.candidates, heights, "Outcome of Approval Voting",
                   "Candidates", "Points", "approval.png")

    elected = max(vp.candidates, key=lambda candidate: points[candidate])
    print(f"\t{elected} wins under approval voting")


def pos_neg(vp, ):
    """Calculate outcome under positive-negative voting."""
    print("Positive-negative voting:")

    votes = defaultdict(int)
    print("\tIndividual votes:")
    for voter, preference in vp.preferences.items():
        pos_candidate = max(
            vp.candidates,
            key=lambda candidate: preference[vp.candidates.index(candidate)])
        neg_candidate = min(
            vp.candidates,
            key=lambda candidate: preference[vp.candidates.index(candidate)])

        votes[pos_candidate] += 1
        votes[neg_candidate] -= 1
        print(
            f"\t\t{voter} voted +1 for {pos_candidate}, -1 for {neg_candidate}"
        )

    print("\tFinal vote counts:")
    for candidate in vp.candidates:
        print(f"\t\t{candidate} received {votes[candidate]} votes")

    heights = [votes[candidate] for candidate in vp.candidates]
    make_bar_chart(vp.candidates, heights,
                   "Outcome of Positive-Negative Voting", "Candidates",
                   "Votes", "pos_neg.png")

    elected = max(vp.candidates, key=lambda candidate: votes[candidate])
    print(f"\t{elected} wins under positive-negative voting")


def main():
    """Visualization of election outcomes under different voting schemes."""
    voter_preferences = VoterPreferences(glob("**/*.csv")[0])
    plurality(voter_preferences)
    runoff(voter_preferences)
    borda(voter_preferences)
    approval(voter_preferences)
    pos_neg(voter_preferences)


if __name__ == "__main__":
    main()
