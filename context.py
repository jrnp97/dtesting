import sys
import contextlib

@contextlib.contextmanager
def mi_context_manager(expected_exception):
    print("Contexto Inicio")
    try:
        yield
        # Codigo del contexto esta aqui
    except Exception as error:
        if isinstance(error, expected_exception):
            print("TEST PASSES")
            return 
        raise error
    finally:
        etype, exc, _ = sys.exc_info()
        if not etype:
            print("TEST NO PASSED")
        print("Context Termino")

with mi_context_manager(expected_exception=ValueError) as value:
    print("CONTEXT OBJECT", value)
    raise ValueError("TESTING_MYCONTEXT")

