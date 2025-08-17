from __future__ import annotations
from flask import Blueprint, render_template, request
from config import TEAM_IDS
from data.football_data import FootballDataClient
from features.stats import extract_team_stats, relevant_matches
from models.poisson import score_matrix, probs_from_matrix, most_likely_score
from pricing.value import expected_value, kelly_fraction

bp = Blueprint("main", __name__)
client = FootballDataClient()


@bp.route("/", methods=["GET", "POST"])
def index():
    teams = sorted(TEAM_IDS.keys())
    ctx = {
        "teams": teams,
        "predictions": None,
        "home_team": None,
        "away_team": None,
        "home_logo": "",
        "away_logo": "",
        "error": None,
        "home_stats": None,
        "away_stats": None,
    }

    if request.method == "POST":
        home_team = request.form.get("home_team")
        away_team = request.form.get("away_team")
        odds_1 = request.form.get("odds_1")
        odds_x = request.form.get("odds_x")
        odds_2 = request.form.get("odds_2")

        ctx.update({"home_team": home_team, "away_team": away_team})

        # validations basiques
        if not home_team or not away_team:
            ctx["error"] = "Veuillez sélectionner deux équipes."
            return render_template("index.html", **ctx)
        if home_team == away_team:
            ctx["error"] = "Veuillez sélectionner deux équipes différentes."
            return render_template("index.html", **ctx)
        if home_team not in TEAM_IDS or away_team not in TEAM_IDS:
            ctx["error"] = "Équipe inconnue."
            return render_template("index.html", **ctx)

        hid, aid = TEAM_IDS[home_team], TEAM_IDS[away_team]

        # logos
        try:
            ctx["home_logo"] = client.team_logo(hid)
        except Exception:
            ctx["home_logo"] = ""
        try:
            ctx["away_logo"] = client.team_logo(aid)
        except Exception:
            ctx["away_logo"] = ""

        # matchs récents
        try:
            home_matches = client.team_matches(hid, days=150, limit=25)
            away_matches = client.team_matches(aid, days=150, limit=25)
        except Exception:
            home_matches, away_matches = [], []

        matches = relevant_matches(home_matches, away_matches, hid, aid)
        if not matches:
            ctx["predictions"] = "no_data"
            return render_template("index.html", **ctx)

        # stats
        h_stats = extract_team_stats(matches, hid)
        a_stats = extract_team_stats(matches, aid)
        ctx["home_stats"], ctx["away_stats"] = h_stats, a_stats

        # lambdas Poisson simples
        home_lambda = max(0.2, (h_stats["gs_avg"] + a_stats["gc_avg"]) / 2)
        away_lambda = max(0.2, (a_stats["gs_avg"] + h_stats["gc_avg"]) / 2)

        # matrices & probas
        M = score_matrix(home_lambda, away_lambda)
        probs = probs_from_matrix(M)  # {'1','X','2','Over2.5','BTTS'}
        most = most_likely_score(M)   # "h-a"

        # normalisations & clés conviviales pour le template
        probs_out = {
            "1": probs.get("1", 0.0),
            "X": probs.get("X", 0.0),
            "2": probs.get("2", 0.0),
            "over25": probs.get("Over2.5", 0.0),
            "under25": 1.0 - probs.get("Over2.5", 0.0),
            "btts_yes": probs.get("BTTS", 0.0),
            "btts_no": 1.0 - probs.get("BTTS", 0.0),
        }

        most_tuple = None
        try:
            h, a = most.split("-")
            most_tuple = (int(h), int(a))
        except Exception:
            most_tuple = None

        # EV & Kelly si cotes fournies
        ev = {"1": None, "X": None, "2": None}
        kelly = {"1": None, "X": None, "2": None}

        def _parse(x: str | None) -> float | None:
            if not x:
                return None
            try:
                v = float(x)
                return v if v >= 1.01 else None
            except Exception:
                return None

        o1, ox, o2 = _parse(odds_1), _parse(odds_x), _parse(odds_2)

        if o1 is not None:
            ev["1"] = probs_out["1"] * max(1.0, o1) - 1.0
            kelly["1"] = kelly_fraction(probs_out["1"], o1, fraction=0.3)
        if ox is not None:
            ev["X"] = probs_out["X"] * max(1.0, ox) - 1.0
            kelly["X"] = kelly_fraction(probs_out["X"], ox, fraction=0.3)
        if o2 is not None:
            ev["2"] = probs_out["2"] * max(1.0, o2) - 1.0
            kelly["2"] = kelly_fraction(probs_out["2"], o2, fraction=0.3)

        preds = {
            "result": max({"1": probs_out["1"], "X": probs_out["X"], "2": probs_out["2"]},
                          key=lambda k: {"1": probs_out["1"], "X": probs_out["X"], "2": probs_out["2"]}[k]),
            "most_likely_score": most_tuple,
            "probs": probs_out,
            "expected_value": ev,
            "kelly": kelly,
        }

        ctx["predictions"] = preds

    return render_template("index.html", **ctx)
