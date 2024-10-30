# analyze.py
import sys

def analyze(num_opponents, card1, card2):
    all_in_hands = {
        1: {
            "pocket_pairs": ["AA", "KK", "QQ", "JJ", "TT", "99", "88", "77", "66", "55", "44", "33", "22"],
            "suited": [
                "A2s", "A3s", "A4s", "A5s", "A6s", "A7s", "A8s", "A9s", "TAs", "JAs", "QAs", "KAs",
                "K2s", "K3s", "K4s", "K5s", "K6s", "K7s", "K8s", "K9s", "TKs", "JKs", "QKs",
                "Q2s", "Q3s", "Q4s", "Q5s", "Q6s", "Q7s", "Q8s", "Q9s", "TQs", "JQs",
                "J4s", "J5s", "J6s", "J7s", "J8s", "J9s", "TJs",
                "T6s", "T7s", "T8s", "T9s",
                "97s", "98s"
            ],
            "offsuit": [
                "A2o", "A3o", "A4o", "A5o", "A6o", "A7o", "A8o", "A9o", "TAo", "JAo", "QAo", "KAo",
                "K2o", "K3o", "K4o", "K5o", "K6o", "K7o", "K8o", "K9o", "TKo", "JKo", "QKo",
                "Q3o", "Q4o", "Q5o", "Q6o", "Q7o", "Q8o", "Q9o", "TQo", "JQo",
                "J7o", "J8o", "J9o", "TJo",
                "T8o", "T9o",
                "98o"
            ]
        },
        2: {
            "pocket_pairs": ["AA", "KK", "QQ", "JJ", "TT", "99", "88"],
            "suited": ["QAs", "KAs"]
        },
        3: {
            "pocket_pairs": ["AA", "KK", "QQ"],
            "suited": ["KAs"]
        }
    }

    rank_map = {
        '2': '2', '3': '3', '4': '4', '5': '5', '6': '6', '7': '7', '8': '8', '9': '9',
        'T': 'T', 'J': 'J', 'Q': 'Q', 'K': 'K', 'A': 'A'
    }

    # Split the card strings into suit and rank
    card1_suit, card1_rank = card1.split('_')
    card2_suit, card2_rank = card2.split('_')

    # Map the ranks
    card1_rank = rank_map.get(card1_rank, card1_rank)
    card2_rank = rank_map.get(card2_rank, card2_rank)

    # Determine the hand type
    if card1_rank == card2_rank:
        hand = f"{card1_rank}{card2_rank}"  # Pocket pair
        hand_type = "pocket_pairs"
    elif card1_suit == card2_suit:
        hand = f"{max(card1_rank, card2_rank)}{min(card1_rank, card2_rank)}s"  # Suited
        hand_type = "suited"
    else:
        hand = f"{max(card1_rank, card2_rank)}{min(card1_rank, card2_rank)}o"  # Offsuit
        hand_type = "offsuit"

    # Check if the hand qualifies for "All-in"
    if hand in all_in_hands.get(num_opponents, {}).get(hand_type, []):
        return f"{hand} with {num_opponents} Opponent: All-in"
    else:
        return f"{hand} with {num_opponents} Opponent: Fold"


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Error: Expected 3 arguments (opponents, card1, card2)")
        sys.exit(1)

    num_opponents = int(sys.argv[1])
    card1 = sys.argv[2]
    card2 = sys.argv[3]

    result = analyze(num_opponents, card1, card2)
    print(result)
