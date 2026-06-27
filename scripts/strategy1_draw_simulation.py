#!/usr/bin/env python3
"""Run Strategy 1: draw-aware Elo simulation for Wimbledon Phase 1."""

from __future__ import annotations

import argparse
import csv
import math
import random
import re
import sys
import unicodedata
import zipfile
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from xml.etree import ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
PROCESSED_DIR = ROOT / "data" / "processed"
REPORTS_DIR = ROOT / "reports"
SUBMISSIONS_DIR = ROOT / "submissions"
DRAW_PATH = PROCESSED_DIR / "wimbledon_2026_draw_sections.csv"
DRAW_TEMPLATE_PATH = PROCESSED_DIR / "wimbledon_2026_draw_sections_template.csv"
FEATURES_PATH = PROCESSED_DIR / "phase1_player_features.csv"
CONSOLIDATED_WORKBOOK_PATH = ROOT / "data" / "tennis_data_consolidated (2).xlsx"
MEN_DRAW_PDF = ROOT / "data" / "2026_MS_draw.pdf"
WOMEN_DRAW_PDF = ROOT / "data" / "2026_LS_draw (1).pdf"
COUNTRY_RE = re.compile(r"\s+[A-Z]{3}$")
DRAW_LINE_RE = re.compile(
    r"^\s*(?:\[(?P<seed>\d+)\]\s*)?(?:\((?P<entry_status>[A-Z])\)\s*)?(?P<position>\d+)\.\s*(?P<body>.+?)\s*$"
)
XLSX_NS = {"main": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
XLSX_REL_NS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"


def ascii_key(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value)
    return re.sub(r"[^a-z]", "", normalized.encode("ascii", "ignore").decode().lower())


def player_keys(value: str) -> set[str]:
    """Build forgiving keys for raw draw names and our existing feature names."""
    cleaned = re.sub(r"\s+\([A-Z]{3}\)(?:\s+SR)?\s*$", "", value.strip())
    cleaned = COUNTRY_RE.sub("", cleaned)
    cleaned = re.sub(r"\s+SR$", "", cleaned)
    keys = {ascii_key(cleaned)}
    if "," in cleaned:
        surname, given = [part.strip() for part in cleaned.split(",", 1)]
        keys.add(ascii_key(f"{given} {surname}"))
        initials = "".join(part[0] for part in re.findall(r"[A-Za-zÀ-ÿ]+", given) if part)
        keys.add(ascii_key(f"{surname} {initials}"))
        if initials:
            keys.add(ascii_key(f"{surname} {initials[0]}"))
    else:
        parts = cleaned.split()
        if len(parts) >= 2:
            given = " ".join(parts[:-1])
            surname = parts[-1]
            first_initial = parts[0][0] if parts[0] else ""
            keys.add(ascii_key(f"{surname}, {given}"))
            keys.add(ascii_key(f"{surname} {''.join(part[0] for part in parts[:-1])}"))
            if first_initial:
                keys.add(ascii_key(f"{surname} {first_initial}"))
    return {key for key in keys if key}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def xlsx_col_to_index(cell_ref: str) -> int:
    letters = "".join(char for char in cell_ref if char.isalpha())
    value = 0
    for char in letters:
        value = value * 26 + ord(char.upper()) - 64
    return value - 1


def normalize_xlsx_target(target: str) -> str:
    target = target.lstrip("/")
    return target if target.startswith("xl/") else f"xl/{target}"


def read_xlsx_sheet(path: Path, sheet_name: str) -> list[dict[str, str]]:
    """Read a simple worksheet into dictionaries without external dependencies."""
    with zipfile.ZipFile(path) as workbook:
        shared_strings: list[str] = []
        if "xl/sharedStrings.xml" in workbook.namelist():
            root = ET.fromstring(workbook.read("xl/sharedStrings.xml"))
            for shared_item in root.findall("main:si", XLSX_NS):
                shared_strings.append("".join(node.text or "" for node in shared_item.findall(".//main:t", XLSX_NS)))

        workbook_root = ET.fromstring(workbook.read("xl/workbook.xml"))
        rels_root = ET.fromstring(workbook.read("xl/_rels/workbook.xml.rels"))
        rel_map = {
            relationship.attrib["Id"]: normalize_xlsx_target(relationship.attrib["Target"])
            for relationship in rels_root
        }
        sheet_path = ""
        sheets_element = workbook_root.find("main:sheets", XLSX_NS)
        for sheet in sheets_element if sheets_element is not None else []:
            if sheet.attrib["name"] == sheet_name:
                rel_id = sheet.attrib[f"{{{XLSX_REL_NS}}}id"]
                sheet_path = rel_map[rel_id]
                break
        if not sheet_path:
            raise ValueError(f"Sheet not found: {sheet_name}")

        sheet_root = ET.fromstring(workbook.read(sheet_path))
        rows: list[list[str]] = []
        for row in sheet_root.findall(".//main:sheetData/main:row", XLSX_NS):
            values: list[str] = []
            for cell in row.findall("main:c", XLSX_NS):
                index = xlsx_col_to_index(cell.attrib["r"])
                while len(values) < index:
                    values.append("")
                cell_type = cell.attrib.get("t")
                value_node = cell.find("main:v", XLSX_NS)
                inline_node = cell.find("main:is/main:t", XLSX_NS)
                if cell_type == "s" and value_node is not None:
                    value = shared_strings[int(value_node.text or 0)]
                elif cell_type == "inlineStr" and inline_node is not None:
                    value = inline_node.text or ""
                elif value_node is not None:
                    value = value_node.text or ""
                else:
                    value = ""
                values.append(value.replace("\xa0", " ").strip())
            rows.append(values)

    if not rows:
        return []
    headers = [header.replace("\xa0", " ").strip() for header in rows[0]]
    dict_rows: list[dict[str, str]] = []
    for row in rows[1:]:
        padded = row + [""] * (len(headers) - len(row))
        dict_rows.append({header: padded[index] for index, header in enumerate(headers) if header})
    return dict_rows


def create_draw_template(path: Path) -> None:
    rows: list[dict[str, object]] = []
    for tour in ("ATP", "WTA"):
        for position in range(1, 129):
            rows.append(
                {
                    "tour": tour,
                    "draw_position": position,
                    "section": math.ceil(position / 16),
                    "seed": "",
                    "player": "",
                    "first_round_opponent": "",
                    "source": "official_draw",
                }
            )
    write_csv(
        path,
        rows,
        ["tour", "draw_position", "section", "seed", "player", "first_round_opponent", "source"],
    )


def build_draw_sections_from_workbook(workbook_path: Path, output_path: Path) -> tuple[list[dict[str, object]], list[str]]:
    issues: list[str] = []
    sheet_specs = [("ATP", "ATP_2026_Draw"), ("WTA", "WTA_2026_Draw")]
    all_rows: list[dict[str, object]] = []
    if not workbook_path.exists():
        return [], [f"Missing consolidated workbook: {workbook_path.relative_to(ROOT)}"]

    for tour, sheet_name in sheet_specs:
        source_rows = read_xlsx_sheet(workbook_path, sheet_name)
        rows_by_position: dict[int, dict[str, object]] = {}
        for source_row in source_rows:
            if not source_row.get("Bracket_Pos") or not source_row.get("Player_Name"):
                continue
            position = int(float(source_row["Bracket_Pos"]))
            rows_by_position[position] = {
                "tour": tour,
                "draw_position": position,
                "section": math.ceil(position / 16),
                "seed": "",
                "entry_status": "",
                "player": source_row["Player_Name"].strip(),
                "country": "",
                "first_round_opponent": "",
                "source": f"{workbook_path.name}:{sheet_name}",
            }
        if len(rows_by_position) != 128:
            issues.append(f"{tour}: expected 128 rows in {sheet_name}, found {len(rows_by_position)}")
        missing_positions = [position for position in range(1, 129) if position not in rows_by_position]
        if missing_positions:
            issues.append(f"{tour}: missing workbook draw positions {missing_positions[:10]}")
        for position, row in rows_by_position.items():
            opponent_position = position + 1 if position % 2 else position - 1
            opponent = rows_by_position.get(opponent_position)
            if opponent:
                row["first_round_opponent"] = opponent["player"]
        all_rows.extend(rows_by_position[position] for position in sorted(rows_by_position))

    if not issues:
        write_csv(
            output_path,
            all_rows,
            [
                "tour",
                "draw_position",
                "section",
                "seed",
                "entry_status",
                "player",
                "country",
                "first_round_opponent",
                "source",
            ],
        )
    return all_rows, issues


def parse_draw_line(line: str, tour: str, source_pdf: Path) -> dict[str, object] | None:
    match = DRAW_LINE_RE.match(line)
    if not match:
        return None
    body = match.group("body").strip()
    country_match = re.search(r"\s+([A-Z]{3})$", body)
    country = country_match.group(1) if country_match else ""
    player = COUNTRY_RE.sub("", body).strip()
    position = int(match.group("position"))
    return {
        "tour": tour,
        "draw_position": position,
        "section": math.ceil(position / 16),
        "seed": match.group("seed") or "",
        "entry_status": match.group("entry_status") or "",
        "player": player,
        "country": country,
        "first_round_opponent": "",
        "source": source_pdf.name,
    }


def extract_draw_rows_from_pdf(path: Path, tour: str) -> list[dict[str, object]]:
    try:
        from pypdf import PdfReader
    except ModuleNotFoundError as exc:
        raise RuntimeError("pypdf is required to parse draw PDFs") from exc

    rows: list[dict[str, object]] = []
    reader = PdfReader(str(path))
    for page in reader.pages:
        text = page.extract_text() or ""
        for line in text.splitlines():
            parsed = parse_draw_line(line, tour, path)
            if parsed:
                rows.append(parsed)

    rows_by_position = {int(row["draw_position"]): row for row in rows}
    for position, row in rows_by_position.items():
        opponent_position = position + 1 if position % 2 else position - 1
        opponent = rows_by_position.get(opponent_position)
        if opponent:
            row["first_round_opponent"] = opponent["player"]
    return [rows_by_position[position] for position in sorted(rows_by_position)]


def build_draw_sections_from_pdfs(output_path: Path) -> tuple[list[dict[str, object]], list[str]]:
    issues: list[str] = []
    pdf_specs = [("ATP", MEN_DRAW_PDF), ("WTA", WOMEN_DRAW_PDF)]
    all_rows: list[dict[str, object]] = []
    for tour, path in pdf_specs:
        if not path.exists():
            issues.append(f"Missing draw PDF: {path.relative_to(ROOT)}")
            continue
        rows = extract_draw_rows_from_pdf(path, tour)
        if len(rows) != 128:
            issues.append(f"{tour}: expected 128 parsed draw rows from {path.name}, found {len(rows)}")
        positions = [int(row["draw_position"]) for row in rows]
        missing_positions = [position for position in range(1, 129) if position not in positions]
        if missing_positions:
            issues.append(f"{tour}: missing draw positions {missing_positions[:10]}")
        all_rows.extend(rows)

    if not issues:
        write_csv(
            output_path,
            all_rows,
            [
                "tour",
                "draw_position",
                "section",
                "seed",
                "entry_status",
                "player",
                "country",
                "first_round_opponent",
                "source",
            ],
        )
    return all_rows, issues


def load_feature_index() -> dict[str, dict[str, dict[str, str]]]:
    rows = read_csv(FEATURES_PATH)
    index: dict[str, dict[str, dict[str, str]]] = {"ATP": {}, "WTA": {}}
    for row in rows:
        tour = row["tour"]
        for value in (row["player"], row["display_name"]):
            for key in player_keys(value):
                index[tour][key] = row
    return index


def load_workbook_elo_index(workbook_path: Path) -> dict[str, dict[str, dict[str, str]]]:
    index: dict[str, dict[str, dict[str, str]]] = {"ATP": {}, "WTA": {}}
    if not workbook_path.exists():
        return index
    for tour, sheet_name, rank_field in (
        ("ATP", "ATP_Elo", "ATP Rank"),
        ("WTA", "WTA_Elo", "WTA Rank"),
    ):
        for row in read_xlsx_sheet(workbook_path, sheet_name):
            player = row.get("Player", "").strip()
            if not player:
                continue
            elo_row = {
                "workbook_player": player,
                "workbook_elo": row.get("Elo", ""),
                "workbook_grass_elo": row.get("gElo", ""),
                "workbook_hard_elo": row.get("hElo", ""),
                "workbook_clay_elo": row.get("cElo", ""),
                "workbook_rank": row.get(rank_field, ""),
                "workbook_elo_rank": row.get("Elo Rank", ""),
                "workbook_grass_elo_rank": row.get("gElo Rank", ""),
            }
            for key in player_keys(player):
                index[tour][key] = elo_row
    return index


def load_historical_feature_index(draw_rows: list[dict[str, str]]) -> dict[str, dict[str, dict[str, object]]]:
    """Build extra features for qualifiers/wildcards that have historical match logs."""
    try:
        from phase1_model import TOURNAMENT_CUTOFF, build_features, build_name_index, load_matches, resolve_entry_name
    except Exception as exc:
        print(f"Warning: could not load historical feature fallback: {exc}")
        return {"ATP": {}, "WTA": {}}

    matches_by_tour = load_matches()
    index: dict[str, dict[str, dict[str, object]]] = {"ATP": {}, "WTA": {}}
    for tour in ("ATP", "WTA"):
        name_index = build_name_index(matches_by_tour[tour])
        entrants: list[dict[str, object]] = []
        seen: set[str] = set()
        for row in draw_rows:
            if row["tour"] != tour:
                continue
            raw_name = row["player"]
            if raw_name in seen:
                continue
            seen.add(raw_name)
            resolved, match_type = resolve_entry_name(raw_name, name_index)
            if match_type in {"ambiguous", "no_history"}:
                continue
            rank = int(row["seed"]) if row.get("seed") else 999
            entrants.append(
                {
                    "tour": tour,
                    "player": resolved,
                    "display_name": raw_name,
                    "rank": rank,
                    "name_match": f"draw_{match_type}",
                }
            )

        for feature in build_features(matches_by_tour[tour], entrants, TOURNAMENT_CUTOFF):
            for value in (str(feature["player"]), str(feature["display_name"])):
                for key in player_keys(value):
                    index[tour][key] = feature
    return index


def load_last_match_index() -> dict[str, dict[str, str]]:
    try:
        from phase1_model import TOURNAMENT_CUTOFF, load_matches
    except Exception as exc:
        print(f"Warning: could not load last-match dates: {exc}")
        return {"ATP": {}, "WTA": {}}

    matches_by_tour = load_matches()
    index: dict[str, dict[str, str]] = {"ATP": {}, "WTA": {}}
    for tour, matches in matches_by_tour.items():
        latest_by_player: dict[str, object] = {}
        for match in matches:
            if match.match_date >= TOURNAMENT_CUTOFF:
                break
            for player in (match.player_1, match.player_2):
                latest_by_player[player] = match.match_date
        for player, match_date in latest_by_player.items():
            for key in player_keys(player):
                index[tour][key] = match_date.isoformat()
    return index


def find_feature(row: dict[str, str], index: dict[str, dict[str, dict[str, str]]]) -> dict[str, str] | None:
    tour = row["tour"]
    for key in player_keys(row["player"]):
        if key in index[tour]:
            return index[tour][key]
    return None


def find_last_match_date(row: dict[str, str], index: dict[str, dict[str, str]]) -> str:
    tour = row["tour"]
    for key in player_keys(row["player"]):
        if key in index[tour]:
            return index[tour][key]
    return ""


def find_workbook_elo(row: dict[str, str], index: dict[str, dict[str, dict[str, str]]]) -> dict[str, str] | None:
    tour = row["tour"]
    for key in player_keys(row["player"]):
        if key in index[tour]:
            return index[tour][key]
    return None


def safe_float(value: object, default: float) -> float:
    try:
        if value == "":
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def blended_rating(feature: dict[str, object], workbook_elo: dict[str, str] | None = None) -> tuple[float, str]:
    """Strategy 1 weighting: workbook grass Elo first, local form second."""
    local_overall = safe_float(feature.get("overall_elo", 1500.0), 1500.0)
    local_grass = safe_float(feature.get("grass_elo", 1500.0), 1500.0)
    if workbook_elo:
        overall = safe_float(workbook_elo.get("workbook_elo"), local_overall)
        grass = safe_float(workbook_elo.get("workbook_grass_elo"), local_grass)
        source = "workbook_elo"
    else:
        overall = local_overall
        grass = local_grass
        source = "local_elo"
    rank_strength = float(feature.get("rank_strength", 0.5) or 0.5)
    recent_form = float(feature.get("recent_form", 0.5) or 0.5)
    wimbledon_form = float(feature.get("wimbledon_form", 0.5) or 0.5)
    rating = (
        0.45 * grass
        + 0.25 * overall
        + 0.12 * (1500.0 + 400.0 * (recent_form - 0.5))
        + 0.10 * (1500.0 + 400.0 * (wimbledon_form - 0.5))
        + 0.08 * (1500.0 + 400.0 * (rank_strength - 0.5))
    )
    return rating, source


def inactivity_penalty(last_match_date: str, feature: dict[str, object]) -> float:
    has_recent_record = float(feature.get("recent_wins", 0) or 0) + float(feature.get("recent_losses", 0) or 0) > 0
    if not last_match_date:
        return 0.0 if has_recent_record else 80.0
    last_date = datetime.strptime(last_match_date, "%Y-%m-%d").date()
    reference_date = datetime(2026, 6, 23).date()
    inactive_days = (reference_date - last_date).days
    if inactive_days > 1095:
        return 80.0 if has_recent_record else 350.0
    if inactive_days > 730:
        return 80.0 if has_recent_record else 260.0
    if inactive_days > 365:
        return 80.0 if has_recent_record else 170.0
    if inactive_days > 180:
        return 80.0
    if inactive_days > 90:
        return 35.0
    return 0.0


def fallback_rating(seed: str) -> float:
    if seed:
        return 1650.0 - min(int(seed), 32) * 3.0
    return 1450.0


def rank_strength(rank: int) -> float:
    return max(0.0, 1.0 - math.log(max(rank, 1)) / math.log(256))


def win_probability(player_a: dict[str, object], player_b: dict[str, object]) -> float:
    rating_a = float(player_a["rating"])
    rating_b = float(player_b["rating"])
    return 1.0 / (1.0 + 10 ** ((rating_b - rating_a) / 400.0))


def simulate_match(player_a: dict[str, object], player_b: dict[str, object], rng: random.Random) -> dict[str, object]:
    return player_a if rng.random() < win_probability(player_a, player_b) else player_b


def prepare_draw_players(
    draw_rows: list[dict[str, str]],
    feature_index: dict[str, dict[str, dict[str, str]]],
    historical_feature_index: dict[str, dict[str, dict[str, object]]],
    last_match_index: dict[str, dict[str, str]],
    workbook_elo_index: dict[str, dict[str, dict[str, str]]],
) -> tuple[dict[str, list[dict[str, object]]], list[str]]:
    players_by_tour: dict[str, list[dict[str, object]]] = {"ATP": [], "WTA": []}
    issues: list[str] = []
    for row in sorted(draw_rows, key=lambda item: (item["tour"], int(item["draw_position"]))):
        player_name = row.get("player", "").strip()
        if not player_name:
            issues.append(f"{row['tour']} position {row['draw_position']}: missing player")
            continue
        workbook_elo = find_workbook_elo(row, workbook_elo_index)
        feature = find_feature(row, feature_index)
        feature_source = "entry_feature"
        if feature is None:
            feature = find_feature(row, historical_feature_index)  # type: ignore[arg-type]
            feature_source = "historical_fallback"
        if feature is None:
            workbook_rank = int(float(workbook_elo.get("workbook_rank") or 999)) if workbook_elo else 999
            workbook_overall = workbook_elo.get("workbook_elo", "") if workbook_elo else ""
            workbook_grass = workbook_elo.get("workbook_grass_elo", "") if workbook_elo else ""
            if workbook_elo:
                feature_source = "workbook_only"
            else:
                issues.append(
                    f"{row['tour']} position {row['draw_position']}: using generic fallback rating for {player_name}"
                )
                feature_source = "generic_fallback"
            feature = {
                "player": player_name,
                "display_name": player_name,
                "rank": str(workbook_rank),
                "overall_elo": workbook_overall or str(fallback_rating(row.get("seed", ""))),
                "grass_elo": workbook_grass or str(fallback_rating(row.get("seed", ""))),
                "rank_strength": f"{rank_strength(workbook_rank):.6f}",
                "recent_form": "0.5",
                "wimbledon_form": "0.5",
            }
        last_match_date = find_last_match_date(row, last_match_index)
        penalty = inactivity_penalty(last_match_date, feature)
        rating, rating_source = blended_rating(feature, workbook_elo)
        rating -= penalty
        if workbook_elo:
            feature_source = f"{feature_source}+workbook_elo"
        players_by_tour[row["tour"]].append(
            {
                "tour": row["tour"],
                "draw_position": int(row["draw_position"]),
                "section": int(row["section"]),
                "seed": row.get("seed", ""),
                "player": feature["player"],
                "display_name": feature["display_name"],
                "entry_rank": int(float(workbook_elo.get("workbook_rank") or feature["rank"])) if workbook_elo else int(float(feature["rank"])),
                "rating": rating,
                "rating_source": rating_source,
                "workbook_elo": workbook_elo.get("workbook_elo", "") if workbook_elo else "",
                "workbook_grass_elo": workbook_elo.get("workbook_grass_elo", "") if workbook_elo else "",
                "workbook_rank": workbook_elo.get("workbook_rank", "") if workbook_elo else "",
                "last_match_date": last_match_date,
                "inactivity_penalty": penalty,
                "feature_source": feature_source,
                "feature": feature,
            }
        )
    return players_by_tour, issues


def validate_draw(players_by_tour: dict[str, list[dict[str, object]]]) -> list[str]:
    issues: list[str] = []
    for tour, players in players_by_tour.items():
        positions = [int(player["draw_position"]) for player in players]
        if len(players) != 128:
            issues.append(f"{tour}: expected 128 draw players, found {len(players)}")
        if len(positions) != len(set(positions)):
            issues.append(f"{tour}: duplicate draw positions found")
        missing_sections = [section for section in range(1, 9) if sum(1 for player in players if player["section"] == section) != 16]
        if missing_sections:
            issues.append(f"{tour}: sections without exactly 16 players: {missing_sections}")
    return issues


def simulate_tour(
    players: list[dict[str, object]],
    simulations: int,
    rng: random.Random,
) -> tuple[Counter[str], Counter[str], Counter[str], Counter[str]]:
    qf_counts: Counter[str] = Counter()
    sf_counts: Counter[str] = Counter()
    final_counts: Counter[str] = Counter()
    title_counts: Counter[str] = Counter()

    ordered = sorted(players, key=lambda player: int(player["draw_position"]))
    for _ in range(simulations):
        round_players = list(ordered)
        while len(round_players) > 8:
            round_players = [
                simulate_match(round_players[index], round_players[index + 1], rng)
                for index in range(0, len(round_players), 2)
            ]
        qf_players = list(round_players)
        qf_counts.update(str(player["display_name"]) for player in qf_players)

        sf_players = [
            simulate_match(qf_players[index], qf_players[index + 1], rng)
            for index in range(0, len(qf_players), 2)
        ]
        sf_counts.update(str(player["display_name"]) for player in sf_players)

        finalists = [
            simulate_match(sf_players[index], sf_players[index + 1], rng)
            for index in range(0, len(sf_players), 2)
        ]
        final_counts.update(str(player["display_name"]) for player in finalists)

        champion = simulate_match(finalists[0], finalists[1], rng)
        title_counts.update([str(champion["display_name"])])

    return qf_counts, sf_counts, final_counts, title_counts


def write_blocker_report(path: Path, issues: list[str]) -> None:
    lines = [
        "# Strategy 1 Draw Simulation Status",
        "",
        f"Generated: {datetime.now().astimezone().isoformat(timespec='seconds')}",
        "",
        "## Status",
        "",
        "Blocked until the official 128-player men's and women's draw is filled in locally.",
        "",
        "## Required File",
        "",
        f"- `{DRAW_PATH.relative_to(ROOT)}`",
        "",
        "## Template Created",
        "",
        f"- `{DRAW_TEMPLATE_PATH.relative_to(ROOT)}`",
        "",
        "## Required Columns",
        "",
        "```text",
        "tour, draw_position, section, seed, player, first_round_opponent, source",
        "```",
        "",
        "## Current Issues",
        "",
    ]
    lines.extend(f"- {issue}" for issue in issues)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_success_report(
    path: Path,
    simulations: int,
    pick_rows: list[dict[str, object]],
    warnings: list[str],
    draw_source: str,
) -> None:
    lines = [
        "# Strategy 1 Draw Simulation Status",
        "",
        f"Generated: {datetime.now().astimezone().isoformat(timespec='seconds')}",
        "",
        "## Status",
        "",
        "Complete. The official singles draw was parsed and the draw-aware Elo simulation ran successfully.",
        "",
        "## Inputs",
        "",
        f"- Draw source: `{draw_source}`",
        f"- `{CONSOLIDATED_WORKBOOK_PATH.relative_to(ROOT)}`",
        f"- `{FEATURES_PATH.relative_to(ROOT)}`",
        "",
        "## Fallback Inputs",
        "",
        f"- `{MEN_DRAW_PDF.relative_to(ROOT)}`",
        f"- `{WOMEN_DRAW_PDF.relative_to(ROOT)}`",
        "",
        "## Outputs",
        "",
        f"- `{DRAW_PATH.relative_to(ROOT)}`",
        "- `reports/strategy_1_draw_simulation_probabilities.csv`",
        "- `reports/strategy_1_draw_simulation_warnings.csv`",
        "- `submissions/strategy_1_phase1_top8.csv`",
        "",
        "## Simulation",
        "",
        f"- Simulations per tour: {simulations}",
        f"- Conservative generic fallback ratings: {len(warnings)} players",
        "",
        "## Section Picks",
        "",
        "| Category | Section | Player | QF probability | Backup |",
        "| --- | ---: | --- | ---: | --- |",
    ]
    for row in pick_rows:
        lines.append(
            f"| {row['category']} | {row['section']} | {row['player']} | "
            f"{row['qf_probability']} | {row['backup_player']} ({row['backup_qf_probability']}) |"
        )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def build_default_draw(draw_path: Path, draw_source: str) -> str | None:
    if draw_source in {"workbook", "auto"} and CONSOLIDATED_WORKBOOK_PATH.exists():
        _, parse_issues = build_draw_sections_from_workbook(CONSOLIDATED_WORKBOOK_PATH, draw_path)
        if parse_issues:
            if draw_source == "workbook":
                create_draw_template(DRAW_TEMPLATE_PATH)
                write_blocker_report(REPORTS_DIR / "strategy_1_draw_simulation_status.md", parse_issues)
                print("Could not build draw sections from consolidated workbook.")
                for issue in parse_issues:
                    print(f"- {issue}")
                return None
            print("Could not build draw sections from workbook; trying PDFs.")
            for issue in parse_issues:
                print(f"- {issue}")
        else:
            print(f"Created draw sections from workbook: {draw_path.relative_to(ROOT)}")
            return "consolidated_workbook"

    if draw_source in {"pdf", "auto"}:
        _, parse_issues = build_draw_sections_from_pdfs(draw_path)
        if not parse_issues:
            print(f"Created draw sections from PDFs: {draw_path.relative_to(ROOT)}")
            return "draw_pdfs"
        create_draw_template(DRAW_TEMPLATE_PATH)
        write_blocker_report(REPORTS_DIR / "strategy_1_draw_simulation_status.md", parse_issues)
        print("Could not build draw sections from PDFs.")
        for issue in parse_issues:
            print(f"- {issue}")
        print(f"Created template: {DRAW_TEMPLATE_PATH.relative_to(ROOT)}")
        return None

    if draw_path.exists():
        return "draw_csv"

    create_draw_template(DRAW_TEMPLATE_PATH)
    write_blocker_report(REPORTS_DIR / "strategy_1_draw_simulation_status.md", [f"Missing {draw_path}"])
    print(f"Missing {draw_path.relative_to(ROOT)}")
    print(f"Created template: {DRAW_TEMPLATE_PATH.relative_to(ROOT)}")
    return None


def run_simulation(draw_path: Path, simulations: int, seed: int, draw_source: str) -> None:
    resolved_draw_source = build_default_draw(draw_path, draw_source)
    if not resolved_draw_source:
        return

    feature_index = load_feature_index()
    workbook_elo_index = load_workbook_elo_index(CONSOLIDATED_WORKBOOK_PATH)
    draw_rows = read_csv(draw_path)
    historical_feature_index = load_historical_feature_index(draw_rows)
    last_match_index = load_last_match_index()
    players_by_tour, match_issues = prepare_draw_players(
        draw_rows,
        feature_index,
        historical_feature_index,
        last_match_index,
        workbook_elo_index,
    )
    validation_issues = validate_draw(players_by_tour)
    if validation_issues:
        create_draw_template(DRAW_TEMPLATE_PATH)
        write_blocker_report(REPORTS_DIR / "strategy_1_draw_simulation_status.md", validation_issues)
        print("Draw simulation blocked by input issues.")
        for issue in validation_issues:
            print(f"- {issue}")
        return

    rng = random.Random(seed)
    probability_rows: list[dict[str, object]] = []
    pick_rows: list[dict[str, object]] = []
    for tour, players in players_by_tour.items():
        qf_counts, sf_counts, final_counts, title_counts = simulate_tour(players, simulations, rng)
        by_display_name = {str(player["display_name"]): player for player in players}
        for display_name, player in by_display_name.items():
            probability_rows.append(
                {
                    "tour": tour,
                    "section": player["section"],
                    "draw_position": player["draw_position"],
                    "player": display_name,
                    "entry_rank": player["entry_rank"],
                    "seed": player["seed"],
                    "qf_probability": qf_counts[display_name] / simulations,
                    "sf_probability": sf_counts[display_name] / simulations,
                    "final_probability": final_counts[display_name] / simulations,
                    "title_probability": title_counts[display_name] / simulations,
                    "rating": f"{float(player['rating']):.2f}",
                    "rating_source": player["rating_source"],
                    "workbook_elo": player["workbook_elo"],
                    "workbook_grass_elo": player["workbook_grass_elo"],
                    "workbook_rank": player["workbook_rank"],
                    "last_match_date": player["last_match_date"],
                    "inactivity_penalty": f"{float(player['inactivity_penalty']):.1f}",
                }
            )

        for section in range(1, 9):
            section_rows = [row for row in probability_rows if row["tour"] == tour and int(row["section"]) == section]
            section_rows.sort(key=lambda row: (-float(row["qf_probability"]), int(row["entry_rank"])))
            winner = section_rows[0]
            backup = section_rows[1] if len(section_rows) > 1 else None
            pick_rows.append(
                {
                    "category": "Men's Singles" if tour == "ATP" else "Women's Singles",
                    "section": section,
                    "player": winner["player"],
                    "entry_rank": winner["entry_rank"],
                    "qf_probability": f"{float(winner['qf_probability']):.4f}",
                    "backup_player": backup["player"] if backup else "",
                    "backup_qf_probability": f"{float(backup['qf_probability']):.4f}" if backup else "",
                    "main_evidence": (
                        f"highest simulated QF probability in section {section}; "
                        f"workbook grass Elo {winner['workbook_grass_elo'] or 'n/a'}; blended rating {winner['rating']}"
                    ),
                }
            )

    probability_rows.sort(key=lambda row: (str(row["tour"]), int(row["section"]), -float(row["qf_probability"])))
    write_csv(
        REPORTS_DIR / "strategy_1_draw_simulation_probabilities.csv",
        probability_rows,
        [
            "tour",
            "section",
            "draw_position",
            "player",
            "entry_rank",
            "seed",
            "qf_probability",
            "sf_probability",
            "final_probability",
            "title_probability",
            "rating",
            "rating_source",
            "workbook_elo",
            "workbook_grass_elo",
            "workbook_rank",
            "last_match_date",
            "inactivity_penalty",
        ],
    )
    write_csv(
        SUBMISSIONS_DIR / "strategy_1_phase1_top8.csv",
        pick_rows,
        [
            "category",
            "section",
            "player",
            "entry_rank",
            "qf_probability",
            "backup_player",
            "backup_qf_probability",
            "main_evidence",
        ],
    )
    if match_issues:
        warning_rows = [{"issue": issue} for issue in match_issues]
        write_csv(REPORTS_DIR / "strategy_1_draw_simulation_warnings.csv", warning_rows, ["issue"])
    else:
        write_csv(REPORTS_DIR / "strategy_1_draw_simulation_warnings.csv", [], ["issue"])
    write_success_report(
        REPORTS_DIR / "strategy_1_draw_simulation_status.md",
        simulations,
        pick_rows,
        match_issues,
        resolved_draw_source,
    )
    print(f"Strategy 1 simulation complete: {simulations} simulations per tour")
    print(f"Wrote {REPORTS_DIR / 'strategy_1_draw_simulation_probabilities.csv'}")
    print(f"Wrote {SUBMISSIONS_DIR / 'strategy_1_phase1_top8.csv'}")
    if match_issues:
        print(f"Wrote fallback warnings for {len(match_issues)} players")


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Strategy 1 draw-aware Elo simulation.")
    parser.add_argument("--draw", type=Path, default=DRAW_PATH, help="Official draw-section CSV path.")
    parser.add_argument(
        "--draw-source",
        choices=["workbook", "pdf", "csv", "auto"],
        default="workbook",
        help="Source used to create the official draw-section CSV.",
    )
    parser.add_argument("--simulations", type=int, default=20000, help="Monte Carlo simulations per tour.")
    parser.add_argument("--seed", type=int, default=20260627, help="Random seed for reproducible simulation.")
    args = parser.parse_args()
    run_simulation(args.draw, args.simulations, args.seed, args.draw_source)


if __name__ == "__main__":
    sys.exit(main())
