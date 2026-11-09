"""出題小工具：輸出題的正解由實際執行程式碼取得，避免答案寫錯。"""
import contextlib, io, os, random, sys, tempfile, textwrap

ALL = {}  # unit -> list


def _run(code, stdin="", files=None, argv=None):
    code = textwrap.dedent(code).strip("\n")
    old = os.getcwd()
    with tempfile.TemporaryDirectory() as d:
        os.chdir(d)
        for name, content in (files or {}).items():
            with open(name, "w", encoding="utf-8") as f:
                f.write(content)
        buf = io.StringIO()
        old_in, old_argv = sys.stdin, sys.argv
        sys.stdin = io.StringIO(stdin)
        sys.argv = argv or ["main.py"]
        err = None
        try:
            with contextlib.redirect_stdout(buf):
                exec(compile(code, "<q>", "exec"), {"__name__": "__main__"})
        except BaseException as e:  # noqa
            err = e
        finally:
            sys.stdin, sys.argv = old_in, old_argv
            os.chdir(old)
    return code, buf.getvalue(), err


def _fmt(out):
    out = "\n".join(l.rstrip() for l in out.rstrip().split("\n"))
    return out if out != "" else "（沒有輸出）"


def _place(qid, correct, distractors):
    assert correct not in distractors, (qid, correct, distractors)
    assert len(set(distractors)) == len(distractors), (qid, distractors)
    rnd = random.Random(qid)
    opts = distractors[:]
    pos = rnd.randint(0, len(opts))
    opts.insert(pos, correct)
    return opts, pos


def add(unit, q):
    ids = {x["id"] for x in ALL.setdefault(unit, [])}
    assert q["id"] not in ids, q["id"]
    for k in [k for k, v in q.items() if v in (None, "")]:
        del q[k]
    ALL[unit].append(q)


def mc(unit, qid, tag, q, correct, distractors, explain, code=None):
    opts, pos = _place(qid, correct, distractors)
    add(unit, {"id": qid, "q": q, "code": textwrap.dedent(code).strip("\n") if code else None,
               "options": opts, "answer": pos, "explain": explain, "tags": [tag]})


def tf(unit, qid, tag, q, answer, explain, code=None):
    add(unit, {"id": qid, "type": "truefalse", "q": q,
               "code": textwrap.dedent(code).strip("\n") if code else None,
               "answer": answer, "explain": explain, "tags": [tag]})


def out(unit, qid, tag, code, distractors, explain, q="執行下列程式碼後，輸出為何？", **kw):
    code, o, err = _run(code, **kw)
    assert err is None, (qid, err)
    mc(unit, qid, tag, q, _fmt(o), distractors, explain, code)


def raises(unit, qid, tag, code, distractors, explain, q="執行下列程式碼會發生什麼事？", **kw):
    """正解為「拋出 XxxError」或實際輸出。"""
    code, o, err = _run(code, **kw)
    correct = f"拋出 {type(err).__name__}" if err else _fmt(o)
    mc(unit, qid, tag, q, correct, distractors, explain, code)


def check(code, expect, **kw):
    """驗證敘述題裡用到的事實。"""
    code, o, err = _run(code, **kw)
    assert err is None, err
    assert o.rstrip("\n") == expect, (o, expect)
