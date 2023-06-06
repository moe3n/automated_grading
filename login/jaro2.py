from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from . import pre


def jaro_winkler(str1: str, str2: str) -> float:

    def get_matched_characters(_str1: str, _str2: str) -> str:
        matched = []
        limit = min(len(_str1), len(_str2)) // 2
        for i, l in enumerate(_str1):
            left = int(max(0, i - limit))
            right = int(min(i + limit + 1, len(_str2)))
            if l in _str2[left:right]:
                matched.append(l)
                _str2 = f"{_str2[0:_str2.index(l)]} {_str2[_str2.index(l) + 1:]}"

        return "".join(matched)

    # matching characters
    matching_1 = get_matched_characters(str1, str2)
    matching_2 = get_matched_characters(str2, str1)
    match_count = len(matching_1)

    # transposition
    transpositions = (
        len([(c1, c2) for c1, c2 in zip(matching_1, matching_2) if c1 != c2]) // 2
    )

    if not match_count:
        jaro = 0.0
    else:
        jaro = (
            1
            / 3
            * (
                match_count / len(str1)
                + match_count / len(str2)
                + (match_count - transpositions) / match_count
            )
        )

    # common prefix up to 4 characters
    prefix_len = 0
    for c1, c2 in zip(str1[:4], str2[:4]):
        if c1 == c2:
            prefix_len += 1
        else:
            break

    return jaro + 0.1 * prefix_len * (1 - jaro)


def combined_similarity(s1, s2, p=0.1):
    # Compute the Jaro-Winkler similarity

    s1, s2 = pre.preprocess(s1, s2)
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([s1])
    feature_names = vectorizer.get_feature_names_out()
    tfidf_matrix = vectorizer.fit_transform([s2])
    feature_names1 = vectorizer.get_feature_names_out()
    # print(feature_names,'\n',feature_names1)
    # s1 = tfidf_matrix[0].toarray().flatten()
    # s2 = tfidf_matrix[1].toarray().flatten()
    s1 = ' '.join(feature_names)
    s2 = ' '.join(feature_names1)
    print("str", s2)

    jaro_winkler_sim = jaro_winkler(s1, s2)

    # Compute the TF-IDF cosine similarity
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([s1, s2])
    cosine_sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
    jaro_winkler_sim_norm = jaro_winkler_sim / 1.0
    cosine_sim_norm = (cosine_sim + 1.0) / 2.0
    print("cosine sim:", cosine_sim)
    print(f"jw:{100*jaro_winkler_sim_norm:.2f}%")

    # Combine the Jaro-Winkler and cosine similarities using a weighted average
    alpha = .5  # Adjust this value to change the weight of the Jaro-Winkler similarity
    combined_sim = alpha * jaro_winkler_sim + (1 - alpha) * cosine_sim

    return combined_sim * 100
