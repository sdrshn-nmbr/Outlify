from difflib import SequenceMatcher

test_cases = [
        (1, "Black crewneck t-shirt", "Top"),
        (2, "White V-neck t-shirt", "Top"),
        (3, "Navy blue polo shirt", "Top"),
        (4, "Red graphic t-shirt", "Top"),
        (5, "Black denim shorts", "Bottom"),
        (6, "White chino shorts", "Bottom"),
        (7, "Royal blue athletic shorts", "Bottom"),
        (8, "Red plaid shorts", "Bottom"),
        (9, "Black slim-fit jeans", "Bottom"),
        (10, "White linen pants", "Bottom"),
        (11, "Indigo blue jogger pants", "Bottom"),
        (12, "Crimson red cargo pants", "Bottom"),
        (13, "Black fedora hat", "Top"),
        (14, "White baseball cap", "Top"),
        (15, "Gray pullover hoodie", "Top"),
        (16, "Yellow zip-up hoodie", "Top"),
        (17, "Olive green button-up shirt", "Top"),
        (18, "Pink oxford shirt", "Top"),
        (19, "Teal half-zip sweatshirt", "Top"),
        (20, "Burgundy sweater vest", "Top"),
        (21, "Charcoal blazer", "Top"),
        (22, "Cream cardigan", "Top"),
        (23, "Denim jacket", "Top"),
        (24, "Tan trench coat", "Top"),
        (25, "Black pinstripe suit jacket", "Top"),
        (26, "White linen blazer", "Top"),
        (27, "Navy blue windbreaker", "Top"),
        (28, "Red bomber jacket", "Top"),
        (29, "Black leather motorcycle jacket", "Top"),
        (30, "White denim jacket", "Top"),
        (31, "Gray tweed vest", "Top"),
        (32, "Mustard yellow raincoat", "Top"),
        (33, "Olive green field jacket", "Top"),
        (34, "Coral blouson jacket", "Top"),
        (35, "Plum corduroy blazer", "Top"),
        (36, "Beige suede jacket", "Top"),
        (37, "Black hoodie vest", "Top"),
        (38, "White sleeveless hoodie", "Top"),
        (39, "Navy blue varsity jacket", "Top"),
        (40, "Red fleece pullover", "Top"),
        (41, "Black down vest", "Top"),
        (42, "White zip-up cardigan", "Top"),
        (43, "Gray knitted poncho", "Top"),
        (44, "Tan safari jacket", "Top"),
        (45, "Black wool pea coat", "Top"),
        (46, "White ski jacket", "Top"),
        (47, "Navy blue puffer jacket", "Top"),
        (48, "Blue striped button-up shirt", "Top"),
        (49, "Green floral print blouse", "Top"),
        (50, "Red plaid flannel shirt", "Top"),
        (51, "Black and white checkered shirt", "Top"),
        (52, "Purple paisley print scarf", "Top"),
        (53, "Orange geometric patterned skirt", "Bottom"),
        (54, "Yellow polka dot sundress", "Bottom"),
        (55, "Blue floral print maxi skirt", "Bottom"),
        (56, "Pink striped leggings", "Bottom"),
        (57, "Green camouflage cargo pants", "Bottom"),
        (58, "Red tartan plaid trousers", "Bottom"),
        (59, "Black and white houndstooth pants", "Bottom"),
        (60, "Gray argyle patterned socks", "Bottom"),
]

def name_similarity(a, b):
  # Returns score for string similarity from 0 to 1
  a = a.lower()
  b = b.lower()
  if a == b:
    return 1
  elif a in b or b in a:
    return (1 + SequenceMatcher(None, a, b).ratio()) / 2
  else:
    return (SequenceMatcher(None, a, b).ratio()) / 2
  
test = """Based on the given weather condition and personal preference, I suggest the following:
[3, "Navy blue polo shirt", "Top"],
[9, "Black slim-fit jeans", "Bottom"]"""

a = "[3, Gray argyle patterned socks"
b = "Gray argyle patterned socks"
max = [0, -100]
for test_case in test_cases:
    sim = name_similarity(test, test_case[1])
    
# print(SequenceMatcher(None, a, b).ratio())
print(max)

def get_two_highest_scores(test_cases):
    highest_scores = [(0, None), (0, None)]  # Initialize with two placeholders for highest scores
    for test_case in test_cases:
        sim = name_similarity(test, test_case[1])  # Assuming 'test' is defined elsewhere
        if sim > highest_scores[0][0]:
            highest_scores[1] = highest_scores[0]  # Shift the second highest score
            highest_scores[0] = (sim, test_case)
        elif sim > highest_scores[1][0]:
            highest_scores[1] = (sim, test_case)
    return highest_scores

# Example usage:
highest_scores = get_two_highest_scores(test_cases)
print("Highest scoring test cases:")
for score, test_case in highest_scores:
    print(f"Test case: {test_case}, Score: {score}")


