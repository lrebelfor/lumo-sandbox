"""Lumo sandbox data: the fictional lamp webshop used throughout the course."""
import csv, glob, json, os

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(HERE, "data")


def path(*parts):
    return os.path.join(DATA, *parts)


def emails():
    """40 labelled customer emails: dicts with id, text, intent, urgency, order_number."""
    with open(path("emails.jsonl"), encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def handbook():
    """The customer handbook as a list of (file name, Markdown text), one per section."""
    return [(os.path.basename(p), open(p, encoding="utf-8").read()) for p in sorted(glob.glob(path("handbook", "*.md")))]


def handbook_messy():
    return open(path("handbook_export_messy.txt"), encoding="utf-8").read()


def orders():
    return json.load(open(path("orders.json"), encoding="utf-8"))


def products():
    return json.load(open(path("products.json"), encoding="utf-8"))


def eval_rag():
    """20 (question, fact a correct answer must contain) pairs for Gate 1."""
    with open(path("eval_rag.csv"), encoding="utf-8") as f:
        return [(r["question"], r["must_contain"]) for r in csv.DictReader(f)]


def company():
    return open(path("company.md"), encoding="utf-8").read()
