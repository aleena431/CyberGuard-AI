
from pathlib import Path
from collections import Counter
from datetime import datetime

# Project locations
BASE_DIR = Path(__file__).resolve().parent
LOG_FILE = BASE_DIR / "data" / "sample_logs.txt"
REPORT_FILE = BASE_DIR / "reports" / "incident_report.txt"

# Detection threshold
FAILED_LOGIN_THRESHOLD = 5


def analyze_logs():
    if not LOG_FILE.exists():
        print(f"Log file not found: {LOG_FILE}")
        return

    failed_by_ip = Counter()
    total_events = 0

    with LOG_FILE.open("r", encoding="utf-8") as file:
        for line in file:
            total_events += 1

            # Count failed login events
            if "Login failed" in line:
                ip = line.split("ip=")[-1].strip()

                if ip:
                    failed_by_ip[ip] += 1

    findings = []

    for ip, count in failed_by_ip.items():
        if count >= FAILED_LOGIN_THRESHOLD:
            findings.append(
                f"ALERT: {count} failed logins from {ip}"
            )

    # Create the report
    REPORT_FILE.parent.mkdir(parents=True, exist_ok=True)

    with REPORT_FILE.open("w", encoding="utf-8") as report:
        report.write("CyberGuardAI - INCIDENT REPORT\n")
        report.write("=" * 35 + "\n")
        report.write(
            f"Generated: {datetime.now().isoformat(timespec='seconds')}\n"
        )
        report.write(f"Events analyzed: {total_events}\n\n")

        if findings:
            report.write("FINDINGS\n")
            for finding in findings:
                report.write(f"- {finding}\n")
        else:
            report.write("No threshold-based alerts detected.\n")

        report.write(
            "\nNOTE: This is a basic rule-based prototype, "
            "not a complete intrusion detection system.\n"
        )

    print(f"Events analyzed: {total_events}")
    print(f"Alerts detected: {len(findings)}")

    for finding in findings:
        print(finding)

    print(f"\nReport saved to: {REPORT_FILE}")


if __name__ == "__main__":
    analyze_logs()