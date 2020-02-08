# Riddler Classic @ https://fivethirtyeight.com/features/how-many-more-palindrome-dates-will-you-see/

# ambiguous expression
AMB_EXP = "|-1|-2|-3|-4|-5|-6|-7|-8|-9|"


def yield_interpretations(amb_exp, parenthesis_level=0, precedent=""):
    """
    Recursively yield all possible interpretations of an expression that contains ambiguous absolute value symbols "|";
    every interpretation is a non-ambiguous, Python-executable string using function abs() instead of symbol "|".
    :param amb_exp: ambiguous expression
    :param parenthesis_level: nr. of unclosed parentheses before the start of this expression
    :param precedent: part of the expression that has already been interpreted; defaults to "" at the beginning
    :return: yield each possible interpretation
    """
    if amb_exp == "":
        yield precedent
    out_exp = precedent
    abs_symbol_nr = amb_exp.count("|")
    for i, ch in enumerate(amb_exp):
        if ch != "|":
            out_exp += ch
        else:
            if abs_symbol_nr > parenthesis_level:
                new_precedent = out_exp + (" * " if out_exp else "") + "abs("
                for interpr in yield_interpretations(amb_exp[(i + 1):], parenthesis_level + 1, new_precedent):
                    yield interpr
            if parenthesis_level > 0:
                new_precedent = out_exp + ")" + (" " if amb_exp[(i + 1):] else "")
                for interpr in yield_interpretations(amb_exp[(i + 1):], parenthesis_level - 1, new_precedent):
                    yield interpr
            break


# evaluate all interpretations and by results
results = {}
for interpr in yield_interpretations(AMB_EXP):
    try:
        result = eval(interpr)
        if result not in results:
            results[result] = set()
        results[result].add(interpr)
    except:
        print('annot evaluate "%s"' % interpr)

# display all possible results and the interpretations leading to them, in order
print('The expression %s can have %d different values:' % (AMB_EXP, len(results)))
for i, result in enumerate(sorted(results.keys()), 1):
    print("\n#%d:" % i)
    for j, interpr in enumerate(sorted(results[result])):
        if j > 0:
            print("or:")
        print("%d = %s" % (result, interpr))
