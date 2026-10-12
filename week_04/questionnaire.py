from collections import Counter

# Counts recursive calls per function (used to measure the cost)
call_counter = Counter()


def build_index(questionnaire):
    return {q["id"]: q for q in questionnaire["questions"]}


# Returns (answer_id, next_question_id) pairs; text/checkbox have answer_id = None
def get_branches(question):
    if question["type"] in ("radio", "select"):
        answers = question.get("answers") or []
        if not answers:
            return [(None, None)]
        return [(a["id"], a.get("next_question_id")) for a in answers]
    return [(None, question.get("next_question_id"))]


# Problems 1 and 2: best(q) = [q] + longest/shortest of best(next)
def _best_path(questionnaire, prefer_longer, use_memo, counter_key):
    index = build_index(questionnaire)
    memo = {}

    def is_better(candidate, current):
        if current is None:
            return True
        if prefer_longer:
            return len(candidate) > len(current)
        return len(candidate) < len(current)

    def best_from(qid, on_path):
        call_counter[counter_key] += 1

        # Base case: end of the questionnaire
        if qid is None or qid not in index:
            return ([], []), False
        # Cycle guard: question is already on the current path
        if qid in on_path:
            return None, True
        if use_memo and qid in memo:
            return memo[qid], False

        on_path.add(qid)
        best_qs, best_as, cut = None, None, False

        for answer_id, next_id in get_branches(index[qid]):
            sub, sub_cut = best_from(next_id, on_path)
            cut = cut or sub_cut
            if sub is None:
                continue
            sub_qs, sub_as = sub
            if is_better(sub_qs, best_qs):
                best_qs = sub_qs
                # Only radio/select questions add an answer id
                best_as = ([answer_id] if answer_id is not None else []) + sub_as

        on_path.remove(qid)  # backtrack

        result = None if best_qs is None else ([qid] + best_qs, best_as)
        # A result cut by the cycle guard depends on the path, so it is not cached
        if use_memo and not cut:
            memo[qid] = result
        return result, cut

    result, _ = best_from(questionnaire.get("start_question_id"), set())
    if result is None:
        return [], []
    return result


def find_longest_question_path(questionnaire, use_memo=True):
    question_ids, answer_path = _best_path(
        questionnaire, prefer_longer=True, use_memo=use_memo, counter_key="longest"
    )
    return {
        "length": len(question_ids),
        "question_ids": question_ids,
        "answer_path": answer_path,
    }


def find_shortest_question_path(questionnaire, use_memo=True):
    question_ids, answer_path = _best_path(
        questionnaire, prefer_longer=False, use_memo=use_memo, counter_key="shortest"
    )
    return {
        "length": len(question_ids),
        "question_ids": question_ids,
        "answer_path": answer_path,
    }


# Problem 3: paths(None) = 1, paths(q) = sum of paths(next); -1 on a cycle
def count_all_possible_paths(questionnaire, use_memo=True):
    index = build_index(questionnaire)
    memo = {}

    def count_from(qid, on_path):
        call_counter["count"] += 1

        if qid is None or qid not in index:
            return 1
        if qid in on_path:
            return -1
        if use_memo and qid in memo:
            return memo[qid]

        on_path.add(qid)
        total = 0
        for _, next_id in get_branches(index[qid]):
            sub = count_from(next_id, on_path)
            if sub == -1:
                return -1
            total += sub
        on_path.remove(qid)

        if use_memo:
            memo[qid] = total
        return total

    return count_from(questionnaire.get("start_question_id"), set())


# Problem 4: recursion with depth tracking
def find_reachable_questions(questionnaire, question_id, answer_id):
    index = build_index(questionnaire)

    question = index.get(question_id)
    if question is None:
        return []
    answer = next(
        (a for a in (question.get("answers") or []) if a["id"] == answer_id), None
    )
    if answer is None:
        return []

    min_depth = {}

    def visit(qid, depth):
        call_counter["reachable"] += 1

        if qid is None or qid not in index:
            return
        # Stop if already reached at an equal or smaller depth (also stops cycles)
        if qid in min_depth and min_depth[qid] <= depth:
            return

        min_depth[qid] = depth
        for _, next_id in get_branches(index[qid]):
            visit(next_id, depth + 1)

    visit(answer.get("next_question_id"), 1)

    result = [
        {
            "question_id": qid,
            "question_text": index[qid]["text"],
            "min_depth": depth,
        }
        for qid, depth in min_depth.items()
    ]
    result.sort(key=lambda r: (r["min_depth"], r["question_id"]))
    return result


# Problem 5: push probability forward; each of k answers gets p / k
def calculate_question_probabilities(questionnaire):
    index = build_index(questionnaire)
    probability = {qid: 0.0 for qid in index}
    weighted_position = {qid: 0.0 for qid in index}

    def propagate(qid, p, position, on_path):
        call_counter["probability"] += 1

        if qid is None or qid not in index:
            return
        if qid in on_path:
            return

        # Accumulate, because several branches can reach the same question
        probability[qid] += p
        weighted_position[qid] += p * position

        branches = get_branches(index[qid])
        share = p / len(branches)

        on_path.add(qid)
        for _, next_id in branches:
            propagate(next_id, share, position + 1, on_path)
        on_path.remove(qid)

    propagate(questionnaire.get("start_question_id"), 1.0, 1, set())

    result = []
    for qid, question in index.items():
        p = probability[qid]
        # Average position given the question is shown; 0 if unreachable
        expected = weighted_position[qid] / p if p > 0 else 0.0
        result.append(
            {
                "question_id": qid,
                "question_text": question["text"],
                "probability": round(p, 4),
                "expected_position": round(expected, 4),
            }
        )
    result.sort(key=lambda r: (-r["probability"], r["question_id"]))
    return result


if __name__ == "__main__":
    import json
    import os
    from pprint import pprint

    here = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(here, "data.json"), encoding="utf-8") as f:
        data = json.load(f)

    print("Problem 1 - longest path:")
    pprint(find_longest_question_path(data))
    print("\nProblem 2 - shortest path:")
    pprint(find_shortest_question_path(data))
    print("\nProblem 3 - number of paths:", count_all_possible_paths(data))
    print("\nProblem 4 - reachable from q2 / a2_truck:")
    pprint(find_reachable_questions(data, "q2", "a2_truck"), sort_dicts=False)
    print("\nProblem 5 - probabilities:")
    for row in calculate_question_probabilities(data):
        print(f"  {row['question_id']:>3}  p={row['probability']:<6}  "
              f"pos={row['expected_position']}")