
import pydoc


def get_help_str(obj: object) -> str:
    return pydoc.render_doc(obj)
