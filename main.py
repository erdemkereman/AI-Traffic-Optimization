
from pathlib import Path
import subprocess
import sys
import webbrowser

BASE_DIR = Path(__file__).resolve().parent


def show_results():
    result_file = BASE_DIR / "data/processed/ml_optimization_results.csv"

    if not result_file.exists():
        print("Sonuc dosyasi bulunamadi.")
        return

    import pandas as pd

    df = pd.read_csv(result_file)

    print("\n--- OPTIMIZASYON SONUCLARI ---")
    print(f"Test senaryosu: {len(df)}")

    columns = ["fixed_wait", "adaptive_wait", "ml_wait", "optimal_wait"]

    for column in columns:
        print(f"{column}: {df[column].mean():.3f} saniye")

    improvement = (
        (df["fixed_wait"].mean() - df["ml_wait"].mean())
        / df["fixed_wait"].mean()
        * 100
    )

    print(f"ML iyilesme orani: %{improvement:.2f}")


def show_graphs():
    figures_dir = BASE_DIR / "results/figures"

    files = sorted(figures_dir.glob("*.png"))

    if not files:
        print("Grafik bulunamadi.")
        return

    print("\n--- GRAFIKLER ---")

    for index, file in enumerate(files, start=1):
        print(f"{index} - {file.name}")

    print("0 - Geri don")

    choice = input("Acmak istediginiz grafik: ").strip()

    if choice == "0":
        return

    if not choice.isdigit():
        print("Gecersiz secim.")
        return

    index = int(choice) - 1

    if 0 <= index < len(files):
        webbrowser.open(files[index].resolve().as_uri())
    else:
        print("Gecersiz grafik numarasi.")


def show_report():
    report = BASE_DIR / "docs/ai_traffic_analysis_report.md"

    if report.exists():
        print("\n--- ANALIZ RAPORU ---\n")
        print(report.read_text(encoding="utf-8"))
    else:
        print("Rapor bulunamadi.")


def run_module(module_name):
    print(f"\nCalistiriliyor: {module_name}")

    result = subprocess.run(
        [sys.executable, "-m", module_name],
        cwd=BASE_DIR
    )

    if result.returncode == 0:
        print("\nIslem basariyla tamamlandi.")
    else:
        print(f"\nIslem hata koduyla sonlandi: {result.returncode}")


def main():
    while True:
        print("\n" + "=" * 45)
        print("         AI TRAFFIC OPTIMIZATION")
        print("=" * 45)
        print("1 - ML optimizasyon sonuclarini goster")
        print("2 - Trafik analiz grafiklerini ac")
        print("3 - Analiz raporunu goruntule")
        print("4 - Optimizasyon karsilastirmasini calistir")
        print("5 - Analiz raporunu yeniden olustur")
        print("0 - Cikis")

        choice = input("\nSeciminiz: ").strip()

        if choice == "1":
            show_results()
        elif choice == "2":
            show_graphs()
        elif choice == "3":
            show_report()
        elif choice == "4":
            run_module("src.models.compare_ml_optimization")
        elif choice == "5":
            run_module("src.llm.generate_traffic_report")
        elif choice == "0":
            print("Program kapatiliyor.")
            break
        else:
            print("Gecersiz secim.")


if __name__ == "__main__":
    main()
