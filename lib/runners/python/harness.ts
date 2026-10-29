/**
 * Python source that defines `_codedrill_run`. It executes user code in a fresh
 * namespace with guarded builtins (no js/pyodide imports, no file writes),
 * captures stdout/stderr, optionally calls a function once per test case, and
 * returns a JSON string. Shared by the browser worker and the Node validator.
 */
export const HARNESS_PY = String.raw`
import ast, builtins, copy, io, json, linecache, math, sys, traceback

_BLOCKED_MODULES = {"js", "pyodide", "pyodide_js", "micropip", "_pyodide", "pyodide_http"}
_MAX_OUTPUT = 64_000
_FILENAME = "<solution>"


def _guarded_builtins():
    b = dict(vars(builtins))
    real_import = builtins.__import__
    real_open = builtins.open

    def guarded_import(name, globals=None, locals=None, fromlist=(), level=0):
        if level == 0 and name.split(".")[0] in _BLOCKED_MODULES:
            raise ImportError(f"Module '{name}' is not available in CodeDrill")
        return real_import(name, globals, locals, fromlist, level)

    def guarded_open(file, mode="r", *args, **kwargs):
        if any(c in mode for c in "wax+"):
            raise PermissionError("Writing files is disabled in CodeDrill")
        return real_open(file, mode, *args, **kwargs)

    b["__import__"] = guarded_import
    b["open"] = guarded_open
    b["input"] = lambda *a: (_ for _ in ()).throw(RuntimeError("input() is not supported; use function arguments"))
    return b


def _jsonable(v, depth=0):
    if depth > 50:
        return repr(v)
    if v is None or isinstance(v, (bool, int, str)):
        return v
    if isinstance(v, float):
        return v if math.isfinite(v) else repr(v)
    if isinstance(v, (list, tuple)):
        return [_jsonable(x, depth + 1) for x in v]
    if isinstance(v, (set, frozenset)):
        items = [_jsonable(x, depth + 1) for x in v]
        try:
            return sorted(items)
        except TypeError:
            return items
    if isinstance(v, dict):
        return {str(k): _jsonable(x, depth + 1) for k, x in v.items()}
    return repr(v)


def _format_exc(e):
    frames = [f for f in traceback.extract_tb(e.__traceback__) if f.filename == _FILENAME]
    head = ("Traceback (most recent call last):\n" + "".join(traceback.format_list(frames))) if frames else ""
    return head + "".join(traceback.format_exception_only(type(e), e))


def _cap(s):
    return s if len(s) <= _MAX_OUTPUT else s[:_MAX_OUTPUT] + "\n… output truncated"


def _codedrill_run(code, function_name, cases_json, echo_last):
    linecache.cache[_FILENAME] = (len(code), None, code.splitlines(True), _FILENAME)
    ns = {"__name__": "__main__", "__builtins__": _guarded_builtins()}
    out, err = io.StringIO(), io.StringIO()
    result = {"ok": True}
    saved = sys.stdout, sys.stderr
    sys.stdout, sys.stderr = out, err
    try:
        try:
            tree = ast.parse(code, _FILENAME)
            last_expr = None
            if echo_last and tree.body and isinstance(tree.body[-1], ast.Expr):
                last_expr = ast.Expression(tree.body.pop().value)
            exec(compile(tree, _FILENAME, "exec"), ns)
            if last_expr is not None:
                value = eval(compile(last_expr, _FILENAME, "eval"), ns)
                if value is not None:
                    print(repr(value))
        except BaseException as e:
            result["ok"] = False
            result["error"] = _format_exc(e)

        if result["ok"] and function_name:
            fn = ns.get(function_name)
            if not callable(fn):
                result["ok"] = False
                result["error"] = f"Function '{function_name}' is not defined. Keep the function name from the starter code."
            else:
                cases = []
                for case in json.loads(cases_json):
                    case_out = io.StringIO()
                    sys.stdout = case_out
                    try:
                        value = fn(*copy.deepcopy(case["args"]))
                        cases.append({"ok": True, "value": _jsonable(value), "stdout": _cap(case_out.getvalue())})
                    except BaseException as e:
                        cases.append({"ok": False, "error": _format_exc(e), "stdout": _cap(case_out.getvalue())})
                    finally:
                        sys.stdout = out
                result["cases"] = cases
    finally:
        sys.stdout, sys.stderr = saved
    result["stdout"] = _cap(out.getvalue())
    result["stderr"] = _cap(err.getvalue())
    return json.dumps(result)
`;
