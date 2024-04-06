"""Install for development script."""

import subprocess
import sys
from pathlib import Path

import toml

PLATFORM_PATH = Path(__file__).parent.resolve()
LOCK = PLATFORM_PATH / "poetry.lock"
PYPROJECT = PLATFORM_PATH / "pyproject.toml"


LOCAL_DEPS = """
[tool.poetry.dependencies]
python = ">=3.9,<3.12"
datamart-devtools = { path = "./extensions/devtools", develop = true }
datamart-core = { path = "./core", develop = true }

datamart-benzinga = { path = "./providers/benzinga", develop = true }
datamart-federal-reserve = { path = "./providers/federal_reserve", develop = true }
datamart-fmp = { path = "./providers/fmp", develop = true }
datamart-fred = { path = "./providers/fred", develop = true }
datamart-intrinio = { path = "./providers/intrinio", develop = true }
datamart-oecd = { path = "./providers/oecd", develop = true }
datamart-polygon = { path = "./providers/polygon", develop = true }
datamart-sec = { path = "./providers/sec", develop = true }
datamart-tiingo = { path = "./providers/tiingo", develop = true }
datamart-tradingeconomics = { path = "./providers/tradingeconomics", develop = true }
datamart-yfinance = { path = "./providers/yfinance", develop = true }

datamart-commodity = { path = "./extensions/commodity", develop = true }
datamart-crypto = { path = "./extensions/crypto", develop = true }
datamart-currency = { path = "./extensions/currency", develop = true }
datamart-derivatives = { path = "./extensions/derivatives", develop = true }
datamart-economy = { path = "./extensions/economy", develop = true }
datamart-equity = { path = "./extensions/equity", develop = true }
datamart-etf = { path = "./extensions/etf", develop = true }
datamart-fixedincome = { path = "./extensions/fixedincome", develop = true }
datamart-index = { path = "./extensions/index", develop = true }
datamart-news = { path = "./extensions/news", develop = true }
datamart-regulators = { path = "./extensions/regulators", develop = true }
datamart-alpha-vantage = { path = "./providers/alpha_vantage", develop = true }
datamart-biztoc = { path = "./providers/biztoc", develop = true }
datamart-cboe = { path = "./providers/cboe", develop = true }
datamart-ecb = { path = "./providers/ecb", develop = true }
datamart-finra = { path = "./providers/finra", develop = true }
datamart-finviz = { path = "./providers/finviz", develop = true }
datamart-government-us = { path = "./providers/government_us", develop = true }
datamart-nasdaq = { path = "./providers/nasdaq", develop = true }
datamart-seeking-alpha = { path = "./providers/seeking_alpha", develop = true }
datamart-stockgrid = { path = "./providers/stockgrid" ,  develop = true }
datamart_tmx = { path = "./providers/tmx", develop = true }
datamart_tradier = { path = "./providers/tradier", develop = true }
datamart-wsj = { path = "./providers/wsj", develop = true }
datamart-charting = { path = "./obbject_extensions/charting", develop = true }
datamart-econometrics = { path = "./extensions/econometrics", develop = true }
datamart-quantitative = { path = "./extensions/quantitative", develop = true }
datamart-technical = { path = "./extensions/technical", develop = true }
"""


def extract_dev_dependencies(local_dep_path):
    """Extract development dependencies from a given package's pyproject.toml."""
    package_pyproject_path = PLATFORM_PATH / local_dep_path
    if package_pyproject_path.exists():
        package_pyproject_toml = toml.load(package_pyproject_path / "pyproject.toml")
        return (
            package_pyproject_toml.get("tool", {})
            .get("poetry", {})
            .get("group", {})
            .get("dev", {})
            .get("dependencies", {})
        )
    return {}


def get_all_dev_dependencies():
    """Aggregate development dependencies from all local packages."""
    all_dev_dependencies = {}
    local_deps = toml.loads(LOCAL_DEPS)["tool"]["poetry"]["dependencies"]
    for _, package_info in local_deps.items():
        if "path" in package_info:
            dev_deps = extract_dev_dependencies(Path(package_info["path"]))
            all_dev_dependencies.update(dev_deps)
    return all_dev_dependencies


def install_local(_extras: bool = False):
    """Install the Platform locally for development purposes."""
    original_lock = LOCK.read_text()
    original_pyproject = PYPROJECT.read_text()

    pyproject_toml = toml.load(PYPROJECT)
    local_deps = toml.loads(LOCAL_DEPS)["tool"]["poetry"]["dependencies"]
    pyproject_toml["tool"]["poetry"]["dependencies"].update(local_deps)

    if _extras:
        dev_dependencies = get_all_dev_dependencies()
        pyproject_toml["tool"]["poetry"].setdefault("group", {}).setdefault(
            "dev", {}
        ).setdefault("dependencies", {})
        pyproject_toml["tool"]["poetry"]["group"]["dev"]["dependencies"].update(
            dev_dependencies
        )

    TEMP_PYPROJECT = toml.dumps(pyproject_toml)

    try:
        with open(PYPROJECT, "w", encoding="utf-8", newline="\n") as f:
            f.write(TEMP_PYPROJECT)

        CMD = [sys.executable, "-m", "poetry"]
        extras_args = ["-E", "all"] if _extras else []

        subprocess.run(
            CMD + ["lock", "--no-update"], cwd=PLATFORM_PATH, check=True  # noqa: S603
        )
        subprocess.run(
            CMD + ["install"] + extras_args, cwd=PLATFORM_PATH, check=True  # noqa: S603
        )

    except (Exception, KeyboardInterrupt) as e:
        print(e)  # noqa: T201
        print("Restoring pyproject.toml and poetry.lock")  # noqa: T201

    finally:
        # Revert pyproject.toml and poetry.lock to their original state
        with open(PYPROJECT, "w", encoding="utf-8", newline="\n") as f:
            f.write(original_pyproject)

        with open(LOCK, "w", encoding="utf-8", newline="\n") as f:
            f.write(original_lock)


if __name__ == "__main__":
    args = sys.argv[1:]
    extras = any(arg.lower() in ["-e", "--extras"] for arg in args)
    install_local(extras)
