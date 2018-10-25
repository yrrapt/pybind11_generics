import pydoc
import test

test_classes = [
    test.TestList,
    test.TestAny,
    test.TestTuple,
    test.TestDict,
    test.TestUnion,
    test.TestOptional,
]

for cls in test_classes:
    strhelp = pydoc.render_doc(cls)
    print(strhelp)
    print()
