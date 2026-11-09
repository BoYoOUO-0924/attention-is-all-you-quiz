"""出題小工具：輸出題的正解由實際執行程式碼取得，避免答案寫錯。"""
import contextlib, io, os, random, signal, sys, tempfile, textwrap


def _timeout(*_):
    raise TimeoutError("執行超過 3 秒（可能是無窮迴圈）")

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
        signal.signal(signal.SIGALRM, _timeout)
        signal.alarm(3)
        try:
            with contextlib.redirect_stdout(buf):
                exec(compile(code, "<q>", "exec"), {"__name__": "__main__"})
        except BaseException as e:  # noqa
            err = e
        finally:
            signal.alarm(0)
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



def _cases(expect, cases, kw):
    if cases is not None:
        return cases
    return [dict(kw, expect=expect)] if expect is not None else []


def _passes(src, case):
    c = dict(case)
    want = c.pop("expect")
    try:
        _, o, err = _run(src, **c)
    except BaseException:  # noqa
        return False
    return err is None and _fmt(o) == want


def order(unit, qid, tag, q, items, explain, code=None, expect=None, cases=None, **kw):
    """排序題：items 依正確順序排列（保留每行開頭的縮排）。
    有給 expect 或 cases 時，會驗證正確順序執行後的輸出，
    並窮舉其他所有排列，確定只有這一種順序能得到相同結果。"""
    import itertools
    items = [x.strip("\n") for x in items]
    assert len(set(items)) > 1, qid
    cs = _cases(expect, cases, kw)
    if cs:
        assert all(_passes("\n".join(items), c) for c in cs), (qid, "正確順序沒有通過")
        assert len(items) <= 8, (qid, "太多行，無法窮舉驗證")
        for perm in set(itertools.permutations(items)):
            if list(perm) != items:
                assert not all(_passes("\n".join(perm), c) for c in cs), (qid, "另一種順序也正確", perm)
    add(unit, {"id": qid, "type": "order", "q": q,
               "code": textwrap.dedent(code).strip("\n") if code else None,
               "items": items, "explain": explain, "tags": [tag]})


def fill(unit, qid, tag, q, code, blanks, explain, expect=None, cases=None, **kw):
    """填空題：code 用 [[1]]、[[2]]… 標出空格；blanks 是 [(正解, [誘答…]), …]。
    有給 expect 或 cases 時，會驗證正解代入後的輸出，
    並確定每個誘答（其他空格填正解）至少會讓一個案例失敗。"""
    code = textwrap.dedent(code).strip("\n")
    def build(choice):
        src = code
        for n, v in enumerate(choice, 1):
            src = src.replace(f"[[{n}]]", v)
        return src
    correct = [c for c, _ in blanks]
    cs = _cases(expect, cases, kw)
    if cs:
        assert all(_passes(build(correct), c) for c in cs), (qid, "正解沒有通過")
        for b, (_, ds) in enumerate(blanks):
            for d in ds:
                choice = correct[:]; choice[b] = d
                assert not all(_passes(build(choice), c) for c in cs), (qid, f"空格 {b + 1} 的誘答「{d}」也正確")
    out_blanks = []
    for n, (c, ds) in enumerate(blanks, 1):
        assert f"[[{n}]]" in code, (qid, n)
        opts, pos = _place(f"{qid}-{n}", c, ds)
        out_blanks.append({"options": opts, "answer": pos})
    add(unit, {"id": qid, "type": "fill", "q": q, "code": code,
               "blanks": out_blanks, "explain": explain, "tags": [tag]})
