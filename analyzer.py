
from pathlib import Path
from collections import Counter
from datetime import datetime


from backend.db.incidents import create_incident

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

    # Store structured alert details
    alerts = []

    for ip, count in failed_by_ip.items():
        if count >= FAILED_LOGIN_THRESHOLD:
            alerts.append({
                "title": "Multiple failed login attempts",
                "description": (
                    f"{count} failed login attempts detected "
                    f"from IP address {ip}."
                ),
                "severity": "high",
                "source": "sample_log_analyzer",
                "source_ip": ip,
                "count": count,
            })

    findings = [
        f"ALERT: {alert['count']} failed logins from {alert['source_ip']}"
        for alert in alerts
    ]

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
    print(f"Alerts detected: {len(alerts)}")

    for finding in findings:
        print(finding)

    print(f"\nReport saved to: {REPORT_FILE}")

    # Save each detected alert to PostgreSQL
    if alerts:
        print("\nSaving incidents to PostgreSQL...")

        for alert in alerts:
            try:
                incident = create_incident(
                    title=alert["title"],
                    description=alert["description"],
                    severity=alert["severity"],
                    source=alert["source"],
                    source_ip=alert["source_ip"],
                )
                print(
                    f"Incident saved: ID {incident['id']} "
                    f"({alert['source_ip']})"
                )
            except Exception as error:
                print(
                    f"Could not save incident for "
                    f"{alert['source_ip']}: {error}"
                )


if __name__ == "__main__":
    analyze_logs()
