import pydoc
import pyg_test

test_classes = [
    pyg_test.TestList,
    pyg_test.TestAny,
    pyg_test.TestTuple,
    pyg_test.TestDict,
    pyg_test.TestUnion,
    pyg_test.TestOptional,
    pyg_test.TestIterString,
    pyg_test.TestIterPair,
]

for cls in test_classes:
    strhelp = pydoc.render_doc(cls)
    print(strhelp)
    print()
