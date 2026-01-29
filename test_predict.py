"""
Manual test script for the AMR-X model engine.
Runs a few organism/antibiotic pairs through predict_resistance_amrx
and prints the resistance probabilities.
"""

from model_engine import predict_resistance_amrx


def run_tests():
    test_cases = [
        ("ESCHERICHIA COLI", "Ciprofloxacin"),
        ("ACINETOBACTER BAUMANNII", "Amikacin"),
        ("STAPHYLOCOCCUS AUREUS", "Vancomycin"),
        ("PSEUDOMONAS AERUGINOSA", "Cefepime"),
    ]

    print("Manual AMR-X predictions\n")
    for organism, antibiotic in test_cases:
        prob = predict_resistance_amrx(organism, antibiotic)
        print(f"{organism} vs {antibiotic} -> resistance probability: {prob:.3f}")


if __name__ == "__main__":
    run_tests()
