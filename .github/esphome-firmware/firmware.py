#!/usr/bin/env python3
# ==============================================================================
# ESPHome Firmware
# prepare: z verejných YAML (ESPHome Config) vytvorí dočasné kópie pre firmware
#          na stiahnutie — bez hesiel, bez MQTT, bez statickej IP, Wi-Fi sa
#          nastaví po nahratí (Improv cez USB alebo hotspot zariadenia)
# validate: skontroluje kópie cez `esphome config` → report (chyby + varovania)
# site:    vytvorí webovú stránku s tlačidlom Install (ESP Web Tools)
#
# Verejné YAML sa NIKDY nemenia, kópie existujú iba počas buildu.
# Súbor bez esphome: (napr. example.yaml) sa preskočí.
# Doska sa nájde automaticky, názov sa berie z komentára pri board:
#   board: esp32-c3-devkitm-1 #ESP32 C3 Super Mini | https://...
# ==============================================================================
import argparse
import html
import json
import os
import re
import subprocess
import sys
from pathlib import Path

from ruamel.yaml import YAML
from ruamel.yaml.comments import CommentedMap, CommentedSeq

BOARD_NAME_RE = re.compile(r"^[ \t]*board:[ \t]*\S+[ \t]*#[ \t]*([^|\n]+)", re.MULTILINE)
ESP_WEB_TOOLS = "https://unpkg.com/esp-web-tools@10.4.0/dist/web/install-button.js?module"
LOGGER_BAUD_RATE = 115200
LOGO_URL = "https://github.com/DzurisHome.png?size=160"
WARNING_RE = re.compile(r"\bWARNING\b")
ANSI_RE = re.compile(r"\x1b\[[0-9;]*m")


def yaml_rt():
    y = YAML()
    y.preserve_quotes = True
    y.width = 4096
    return y


# ------------------------------------------------------------------------------
# Úprava kópie pre firmware
# ------------------------------------------------------------------------------
def uses_hardware_uart0(cfg):
    """ESP8266 má iba jeden hardvérový UART (GPIO1/GPIO3). Ak ho používa uart:
    (napr. meranie spotreby CSE7766), logger ani Improv cez USB nesmú bežať."""
    if "esp8266" not in cfg:
        return False
    buses = cfg.get("uart")
    buses = buses if isinstance(buses, list) else [buses]
    for bus in buses:
        if not isinstance(bus, dict):
            continue
        for key in ("rx_pin", "tx_pin"):
            pin = bus.get(key)
            if isinstance(pin, dict):
                pin = pin.get("number")
            if str(pin).upper().replace("GPIO0", "GPIO") in ("GPIO1", "GPIO3", "1", "3"):
                return True
    return False


def make_firmware_config(cfg):
    """Vráti zoznam toho, čo bolo z firmware vynechané."""
    missing = []
    improv = not uses_hardware_uart0(cfg)

    #Logger (Improv cez USB potrebuje zapnutý logger)
    if not isinstance(cfg.get("logger"), dict):
        cfg["logger"] = CommentedMap()
    if improv:
        cfg["logger"]["baud_rate"] = LOGGER_BAUD_RATE

    #WiFi: bez siete, bez hesiel, bez statickej IP → nastaví sa po nahratí
    wifi = cfg.get("wifi")
    if not isinstance(wifi, dict):
        wifi = cfg["wifi"] = CommentedMap()
    for key in ("ssid", "password", "networks", "bssid"):
        wifi.pop(key, None)
    if "manual_ip" in wifi:
        wifi.pop("manual_ip")
        missing.append("Static IP")
    ap = wifi.get("ap")
    if not isinstance(ap, dict):
        ap = wifi["ap"] = CommentedMap()
    ap.pop("password", None)

    #WiFi Hotspot + Improv
    if "captive_portal" not in cfg:
        cfg["captive_portal"] = None
    if improv and "improv_serial" not in cfg:
        keys = list(cfg.keys())
        cfg.insert(keys.index("captive_portal") + 1, "improv_serial", None)

    #ESPHome API bez šifrovania
    api = cfg.get("api")
    if isinstance(api, dict):
        if "encryption" in api:
            api.pop("encryption")
            missing.append("API encryption")
        if not api:
            cfg["api"] = None

    #OTA bez hesla
    ota = cfg.get("ota")
    if isinstance(ota, list):
        for item in ota:
            if isinstance(item, dict) and "password" in item:
                item.pop("password")
                if "OTA password" not in missing:
                    missing.append("OTA password")

    #Web Server bez prihlásenia
    web = cfg.get("web_server")
    if isinstance(web, dict) and "auth" in web:
        web.pop("auth")
        missing.append("Web Server login")

    #MQTT preč
    if "mqtt" in cfg:
        cfg.pop("mqtt")
        missing.insert(0, "MQTT")

    #Čas z Home Assistanta (správne časové pásmo pre každého)
    if "time" in cfg:
        seq = CommentedSeq()
        item = CommentedMap()
        item["platform"] = "homeassistant"
        seq.append(item)
        cfg["time"] = seq

    return missing


# ------------------------------------------------------------------------------
# Čo firmware obsahuje (pre webovú stránku)
# ------------------------------------------------------------------------------
def entries(cfg, component):
    value = cfg.get(component)
    if isinstance(value, list):
        return [v for v in value if isinstance(v, dict)]
    return []


def features_of(cfg):
    names = []

    def has_platform(component, platform, name_part=None):
        for e in entries(cfg, component):
            if e.get("platform") == platform and (
                name_part is None or name_part in str(e.get("name", ""))
            ):
                return True
        return False

    checks = [
        (has_platform("switch", "gpio", "") and any(e.get("id") == "relay" for e in entries(cfg, "switch")), "Relay"),
        (has_platform("sensor", "cse7766") or has_platform("sensor", "hlw8012") or has_platform("sensor", "bl0937"), "Voltage, Current, Power"),
        (has_platform("sensor", "ntc"), "Internal Temperature (NTC)"),
        (any(e.get("id") == "overload_protection" for e in entries(cfg, "select")), "Overload Protection"),
        (any(e.get("id") == "overheat_protection" for e in entries(cfg, "select")), "Overheat Protection"),
        (has_platform("binary_sensor", "gpio", "Button"), "Power Button"),
        (has_platform("light", "status_led"), "Status LED"),
        (has_platform("sensor", "pm1006"), "PM2.5"),
        (has_platform("text_sensor", "template", "Air Quality"), "Air Quality"),
        (has_platform("text_sensor", "template", "Color"), "Color"),
        (has_platform("binary_sensor", "gpio", "Fan"), "Fan"),
        (has_platform("sensor", "internal_temperature"), "Internal Temperature"),
        (has_platform("sensor", "wifi_signal"), "Wi-Fi Signal"),
        (has_platform("sensor", "uptime"), "Uptime"),
        (has_platform("button", "restart"), "Restart Button"),
        ("api" in cfg, "Home Assistant API (auto-discovery)"),
        ("web_server" in cfg, "Web Server"),
        ("ota" in cfg, "OTA Updates"),
        ("safe_mode" in cfg, "Safe Mode"),
        ("time" in cfg, "Time from Home Assistant"),
        ("esp32_ble" in cfg, "Bluetooth"),
        ("bluetooth_proxy" in cfg, "Bluetooth Proxy"),
        ("captive_portal" in cfg, "Wi-Fi Setup Hotspot"),
        ("improv_serial" in cfg, "Wi-Fi Setup over USB (Improv)"),
    ]
    for ok, name in checks:
        if ok:
            names.append(name)
    return names


# ------------------------------------------------------------------------------
# prepare
# ------------------------------------------------------------------------------
def cmd_prepare(args):
    src_dir = Path(args.config_dir)
    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    y = yaml_rt()

    boards = []
    for f in sorted(src_dir.glob("*.yaml")):
        text = f.read_text(encoding="utf-8")
        cfg = y.load(text)
        if not isinstance(cfg, dict) or "esphome" not in cfg:
            print(f"Skipped (not a device config): {f.name}")
            continue
        m = BOARD_NAME_RE.search(text)
        name = m.group(1).strip() if m else f.stem
        missing = make_firmware_config(cfg)
        board_id = re.sub(r"[^a-z0-9]+", "-", f.stem.lower()).strip("-")
        with open(out_dir / f"{board_id}.yaml", "w", encoding="utf-8") as fh:
            y.dump(cfg, fh)
        boards.append({
            "id": board_id,
            "file": f.name,
            "name": name,
            "improv": "improv_serial" in cfg,
            "ap": str(cfg["wifi"]["ap"].get("ssid") or ""),
            "features": features_of(cfg),
            "missing": missing,
        })
        print(f"Prepared: {f.name} ({name})")

    if not boards:
        print(f"::error::No device configs found in: {src_dir}")
        return 1
    (out_dir / "boards.json").write_text(json.dumps(boards, indent=2), encoding="utf-8")
    if args.matrix:
        Path(args.matrix).write_text(json.dumps([b["id"] for b in boards]), encoding="utf-8")
    return 0


# ------------------------------------------------------------------------------
# validate
# ------------------------------------------------------------------------------
def cmd_validate(args):
    build = Path(args.build)
    boards = json.loads((build / "boards.json").read_text(encoding="utf-8"))
    ignore = []
    if args.ignore and Path(args.ignore).is_file():
        ignore = [
            l.strip() for l in Path(args.ignore).read_text(encoding="utf-8").splitlines()
            if l.strip() and not l.lstrip().startswith("#")
        ]

    results = []
    for b in boards:
        name = f"{b['id']}.yaml"
        proc = subprocess.run(
            ["esphome", "config", name],
            cwd=build, capture_output=True, text=True,
            env={**os.environ, "NO_COLOR": "1"},
        )
        out = ANSI_RE.sub("", proc.stdout + proc.stderr).splitlines()
        warnings = list(dict.fromkeys(
            l.strip() for l in out
            if WARNING_RE.search(l) and not any(i in l for i in ignore)
        ))
        errors = []
        if proc.returncode != 0:
            start = next((i for i, l in enumerate(out) if "Failed config" in l), None)
            if start is not None:
                errors = [l.rstrip() for l in out[start:] if l.strip() and not l.startswith("INFO")][:60]
            else:
                errors = [l.rstrip() for l in out if "ERROR" in l][:30] or out[-20:]
        results.append((b, errors, warnings))
        state = "ERROR" if errors else ("WARNING" if warnings else "OK")
        print(f"{state:8} {name}")

    n_err = sum(1 for _, e, _ in results if e)
    n_warn = sum(1 for _, e, w in results if w and not e)
    status = "errors" if n_err else ("warnings" if n_warn else "ok")

    head = {
        "errors": "### ❌ ESPHome Validate: Failed",
        "warnings": "### ✅ ESPHome Validate: Passed with Warnings",
        "ok": "### ✅ ESPHome Validate: Passed",
    }[status]
    lines = [head, "", f"ESPHome `{args.esphome_version}`", "", "| Board | File | Result |", "|---|---|---|"]
    for b, errors, warnings in results:
        result = "❌ Error" if errors else ("⚠️ Warning" if warnings else "✅ OK")
        lines.append(f"| {b['name']} | `{b['file']}` | {result} |")
    for b, errors, warnings in results:
        if not errors and not warnings:
            continue
        lines += ["", f"#### {b['name']} (`{b['file']}`)", ""]
        if errors:
            lines += ["**Errors**", "", "```"] + errors + ["```", ""]
        if warnings:
            lines += ["**Warnings**", "", "```"] + warnings + ["```", ""]
    Path(args.report).write_text("\n".join(lines) + "\n", encoding="utf-8")
    Path(args.status).write_text(status, encoding="utf-8")
    print(f"Result: {status}")
    return 0


# ------------------------------------------------------------------------------
# site
# ------------------------------------------------------------------------------
PAGE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<link rel="icon" href="{logo}">
<script type="module" src="{ewt}"></script>
<style>
:root {{ color-scheme: light dark; --bg:#f6f7f9; --card:#fff; --text:#1d2329; --muted:#5b6670; --line:#dde2e7; --ok:#1a7f37; --no:#b42318; --accent:#03a9f4; }}
@media (prefers-color-scheme: dark) {{ :root {{ --bg:#111418; --card:#1a1f25; --text:#e6e9ec; --muted:#9aa5b1; --line:#2b333c; --ok:#3fb950; --no:#f85149; }} }}
* {{ box-sizing: border-box; }}
body {{ margin:0; font:16px/1.5 system-ui,-apple-system,Segoe UI,Roboto,sans-serif; background:var(--bg); color:var(--text); }}
main {{ max-width:760px; margin:0 auto; padding:32px 16px 48px; }}
header {{ display:flex; align-items:center; gap:16px; margin:0 0 24px; }}
header img {{ width:64px; height:64px; border-radius:14px; flex:none; }}
h1 {{ font-size:1.6rem; line-height:1.25; margin:0 0 4px; }}
.sub {{ color:var(--muted); margin:0; }}
.card {{ background:var(--card); border:1px solid var(--line); border-radius:12px; padding:20px; margin-bottom:16px; }}
h2 {{ font-size:1.05rem; margin:0 0 12px; }}
select {{ width:100%; font:inherit; padding:10px; border-radius:8px; border:1px solid var(--line); background:var(--bg); color:var(--text); }}
ol {{ margin:0; padding-left:20px; }}
ul.list {{ list-style:none; margin:0; padding:0; display:grid; grid-template-columns:repeat(auto-fill,minmax(220px,1fr)); gap:4px 16px; }}
.ok::before {{ content:"✓ "; color:var(--ok); font-weight:700; }}
.no::before {{ content:"✕ "; color:var(--no); font-weight:700; }}
.install {{ margin-top:16px; }}
.install button {{ font:inherit; font-weight:600; padding:10px 22px; border:0; border-radius:8px; background:var(--accent); color:#fff; cursor:pointer; }}
.note {{ color:var(--muted); font-size:.9rem; margin:12px 0 0; }}
a {{ color:var(--accent); }}
</style>
</head>
<body>
<main>
  <header>
    <img src="{logo}" alt="Dzuriš Home">
    <div>
      <h1>{title}</h1>
      <p class="sub">Ready-made ESPHome firmware · ESPHome {version}</p>
    </div>
  </header>

  <div class="card">
    <h2>1. Select your board</h2>
    <select id="board">{options}</select>
    <div class="install">
      <esp-web-install-button id="button" manifest="{first_manifest}">
        <button slot="activate">Install</button>
        <span slot="unsupported">Your browser does not support installing firmware. Use Chrome or Edge.</span>
        <span slot="not-allowed">Installing firmware needs a secure (https) connection.</span>
      </esp-web-install-button>
    </div>
    <p class="note">Select your board, connect it with a USB cable and click Install.</p>
    <p class="note" id="download"></p>
  </div>

  <div class="card">
    <h2>2. Set up Wi-Fi</h2>
    <ol id="wifi"></ol>
  </div>

  <div class="card">
    <h2>Included</h2>
    <ul class="list" id="features"></ul>
  </div>

  <div class="card">
    <h2>Not included</h2>
    <ul class="list" id="missing"></ul>
    <p class="note">Need these? Use the <a href="{yaml_url}">YAML files</a> and compile your own firmware in ESPHome.</p>
  </div>
</main>
<script>
const boards = {boards_json};
const select = document.getElementById("board");
function render() {{
  const b = boards.find(x => x.id === select.value);
  document.getElementById("button").setAttribute("manifest", "firmware/" + b.id + "/manifest.json");
  const fill = (id, items, cls) => {{
    const ul = document.getElementById(id);
    ul.replaceChildren(...items.map(t => {{ const li = document.createElement("li"); li.className = cls; li.textContent = t; return li; }}));
  }};
  fill("features", b.features, "ok");
  fill("missing", b.missing.length ? b.missing : ["Nothing"], "no");
  const steps = [];
  if (b.improv) steps.push("Right after the install, this page asks for your Wi-Fi name and password.");
  steps.push((b.improv ? "Skipped it? The" : "After the install, the") + " device starts the Wi-Fi hotspot \u201c" + b.ap + "\u201d. Connect to it with your phone and enter your Wi-Fi there.");
  steps.push("Home Assistant finds the device automatically (ESPHome integration).");
  fill("wifi", steps, "");
  const dl = document.getElementById("download");
  if (b.bin) {{
    dl.innerHTML = "";
    const a = document.createElement("a");
    a.href = "firmware/" + b.id + "/" + b.bin;
    a.textContent = "Download .bin";
    a.setAttribute("download", "");
    dl.append(a, " for OTA update (e.g. from Tasmota or the ESPHome Web Server).");
  }} else {{
    dl.textContent = "";
  }}
}}
select.addEventListener("change", render);
render();
</script>
</body>
</html>
"""


def cmd_site(args):
    site = Path(args.site)
    boards = json.loads(Path(args.boards).read_text(encoding="utf-8"))
    built = [b for b in boards if (site / "firmware" / b["id"] / "manifest.json").is_file()]
    if not built:
        print("::error::No built firmware found")
        return 1
    for b in boards:
        if b not in built:
            print(f"::warning::Firmware missing for: {b['id']}")
    #Súbor na stiahnutie (OTA) z manifestu
    for b in built:
        m = json.loads((site / "firmware" / b["id"] / "manifest.json").read_text(encoding="utf-8"))
        build = (m.get("builds") or [{}])[0]
        b["bin"] = (build.get("ota") or {}).get("path") or ((build.get("parts") or [{}])[0]).get("path") or ""

    options = "".join(
        f'<option value="{html.escape(b["id"])}">{html.escape(b["name"])}</option>' for b in built
    )
    page = PAGE.format(
        title=html.escape(args.title),
        ewt=ESP_WEB_TOOLS,
        logo=LOGO_URL,
        version=html.escape(str(args.esphome_version)),
        options=options,
        first_manifest=f"firmware/{built[0]['id']}/manifest.json",
        yaml_url=html.escape(args.yaml_url),
        boards_json=json.dumps(built).replace("</", "<\\/"),
    )
    (site / "index.html").write_text(page, encoding="utf-8")
    (site / "version.json").write_text(json.dumps({"esphome": args.esphome_version}), encoding="utf-8")
    print(f"Site: {len(built)} board(s)")
    return 0


def main():
    ap = argparse.ArgumentParser(description="Firmware")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("prepare")
    p.add_argument("--config-dir", required=True)
    p.add_argument("--out", required=True)
    p.add_argument("--matrix", help="Write board ids as JSON list")

    s = sub.add_parser("site")
    s.add_argument("--boards", required=True)
    s.add_argument("--site", required=True)
    s.add_argument("--title", required=True)
    s.add_argument("--yaml-url", required=True)
    s.add_argument("--esphome-version", required=True)

    v = sub.add_parser("validate")
    v.add_argument("--build", required=True)
    v.add_argument("--report", required=True)
    v.add_argument("--status", required=True)
    v.add_argument("--esphome-version", required=True)
    v.add_argument("--ignore", help="File with warning substrings to ignore, one per line")

    args = ap.parse_args()
    return {"prepare": cmd_prepare, "validate": cmd_validate, "site": cmd_site}[args.cmd](args)


if __name__ == "__main__":
    sys.exit(main())
