# Import libraries
from time import perf_counter
from pathlib import Path
import csv
from datetime import datetime, timezone
import tracemalloc
import sys
from pathlib import Path

# Constants
BASE_DIR = Path(__file__).resolve().parent
CHAL_DIR = BASE_DIR / "retos"
FACT_DIR = BASE_DIR / "factorización de enteros"
sys.path.append(str(FACT_DIR))

# Import algorithms
from fermat import fermat
from pollard_rho import pollard_rho
from pollard_p_1 import pollard_p1
from lenstra import lenstra_ecm


# Load challenges
def load_challenges(
    directory: Path = CHAL_DIR,
    filename: str = "retos_factorizacion.txt"):
    challenges = []
    path = directory / filename

    with path.open("r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            t, n = line.split(",")
            challenges.append((int(t), int(n)))

    return challenges


def run_algorithm(name: str, func, n: int, timeout: int) -> dict:
    start_ts = datetime.now(timezone.utc)
    
    # Memory registry
    tracemalloc.start()
    start = perf_counter()
    
    try:
        factors = func(n, timeout)
        elapsed = perf_counter() - start
        
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        
        if factors:
            success = True if factors[0]*factors[1]==n else False
        else:
            success = False
        memory_mb = peak / (1024 * 1024)  # to MB
        
    except Exception as e:
        elapsed = perf_counter() - start
        
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        
        factors = None
        success = False
        memory_mb = peak / (1024 * 1024)

    return {
        "timestamp": start_ts.isoformat(),
        "algorithm": name,
        "n": n,
        "time": elapsed,
        "memory_mb": memory_mb,
        "success": success,
        "factors": factors,
    }


def save_results_csv(results: list, output_file: Path):
    fieldnames = [
        "timestamp",
        "algorithm",
        "bits",
        "n",
        "time",
        "memory_mb",
        "success",
        "factor_1",
        "factor_2",
    ]

    with output_file.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for r in results:
            factors = r.get("factors")
            if isinstance(factors, int):
                f1, f2 = factors, None
            elif isinstance(factors, (list, tuple)) and len(factors) == 2:
                f1, f2 = factors[0], factors[1]
            else:
                f1, f2 = None, None

            writer.writerow({
                "timestamp": r["timestamp"],
                "algorithm": r["algorithm"],
                "bits": r["bits"],
                "n": r["n"],
                "time": r["time"],
                "memory_mb": r["memory_mb"],
                "success": r["success"],
                "factor_1": f1,
                "factor_2": f2,
            })


def main(verbose:bool = False):

    challenges = load_challenges()
    algorithms = {
        "Fermat": fermat,
        "Pollard Rho": pollard_rho,
        "Pollard p-1": pollard_p1,
        "Lenstra": lenstra_ecm,
    }

    results = []
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    output = Path(f"results_factorization_{ts}.csv")

    for bits, n in challenges:
        print(f"\n[+] Processing n = {n} ({bits} bits)")
        for name, func in algorithms.items():
            result = run_algorithm(name, func, n, timeout=60)
            result["bits"] = bits
            results.append(result)
            
            if verbose:
                print(
                    f"{name:18s} | "
                    f"time = {result['time']:.4f}s | "
                    f"memory = {result['memory_mb']:.2f} MB | "
                    f"success = {result['success']}"
                )

        save_results_csv(results, output)


if __name__ == "__main__":
    main(True)