#!/usr/bin/env python3
"""Git connection test project - entry point."""

from __future__ import annotations

import argparse
import dataclasses
import datetime as dt
import json
import os
import platform
import sys
from typing import Any, Dict, List


@dataclasses.dataclass(frozen=True)
class AppConfig:
    project_name: str
    iterations: int
    show_env: bool
    output_json: bool


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="A tiny CLI that prints a diagnostic report for Git testing."
    )
    parser.add_argument(
        "--project-name",
        default="Git Connection Test",
        help="Name used in the generated report.",
    )
    parser.add_argument(
        "--iterations",
        type=int,
        default=3,
        help="Number of simulated steps to include in the report.",
    )
    parser.add_argument(
        "--show-env",
        action="store_true",
        help="Include selected environment variables.",
    )
    parser.add_argument(
        "--json",
        dest="output_json",
        action="store_true",
        help="Print the report as formatted JSON.",
    )
    return parser


def parse_args(argv: List[str]) -> AppConfig:
    args = build_parser().parse_args(argv)
    return AppConfig(
        project_name=args.project_name,
        iterations=max(1, args.iterations),
        show_env=args.show_env,
        output_json=args.output_json,
    )


def collect_environment() -> Dict[str, Any]:
    return {
        "timestamp": dt.datetime.now(tz=dt.timezone.utc).isoformat(),
        "python_version": sys.version.split()[0],
        "executable": sys.executable,
        "platform": platform.platform(),
        "current_directory": os.getcwd(),
    }


def collect_optional_env() -> Dict[str, str]:
    keys = ["USER", "SHELL", "LANG", "TERM"]
    return {key: value for key in keys if (value := os.getenv(key))}


def simulate_steps(iterations: int) -> List[Dict[str, Any]]:
    steps: List[Dict[str, Any]] = []
    for index in range(1, iterations + 1):
        steps.append(
            {
                "step": index,
                "title": f"Task {index}",
                "status": "ok",
                "duration_ms": 120 * index,
            }
        )
    return steps


def build_report(config: AppConfig) -> Dict[str, Any]:
    report: Dict[str, Any] = {
        "project": config.project_name,
        "message": "Hello, Git! Connection test successful.",
        "environment": collect_environment(),
        "steps": simulate_steps(config.iterations),
    }
    if config.show_env:
        report["environment_variables"] = collect_optional_env()
    return report


def render_report_text(report: Dict[str, Any]) -> str:
    lines = [
        f"Project: {report['project']}",
        report["message"],
        "",
        "Environment:",
        f"  Timestamp: {report['environment']['timestamp']}",
        f"  Python: {report['environment']['python_version']}",
        f"  Executable: {report['environment']['executable']}",
        f"  Platform: {report['environment']['platform']}",
        f"  CWD: {report['environment']['current_directory']}",
        "",
        "Steps:",
    ]
    for step in report["steps"]:
        lines.append(
            f"  - {step['title']} | status={step['status']} | "
            f"duration_ms={step['duration_ms']}"
        )
    if "environment_variables" in report:
        lines.append("")
        lines.append("Environment Variables:")
        for key, value in report["environment_variables"].items():
            lines.append(f"  {key}={value}")
    return "\n".join(lines)


def main(argv: List[str]) -> int:
    config = parse_args(argv)
    report = build_report(config)
    if config.output_json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(render_report_text(report))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
