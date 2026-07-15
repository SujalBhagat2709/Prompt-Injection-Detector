import json
import os
import re


class PromptInjectionDetector:

    def __init__(self):

        self.file_name = "prompt_analysis.json"

        self.history = []

        self.attack_patterns = {

            "Instruction Override": [

                "ignore previous",

                "ignore all previous",

                "forget previous",

                "disregard instructions",

                "override instructions"

            ],

            "System Prompt Leak": [

                "system prompt",

                "show system prompt",

                "print system prompt",

                "reveal prompt",

                "developer prompt"

            ],

            "Role Manipulation": [

                "you are now",

                "pretend to be",

                "act as",

                "simulate",

                "roleplay"

            ],

            "Data Exfiltration": [

                "reveal secrets",

                "show hidden",

                "display memory",

                "internal instructions",

                "hidden prompt"

            ],

            "Jailbreak Attempt": [

                "do anything now",

                "bypass",

                "ignore safety",

                "disable safety",

                "without restrictions"

            ]

        }

        self.load_history()

    def load_history(self):

        if os.path.exists(self.file_name):

            try:

                with open(

                    self.file_name,

                    "r",

                    encoding="utf-8"

                ) as file:

                    self.history = json.load(file)

            except:

                self.history = []

    def save_history(self):

        with open(

            self.file_name,

            "w",

            encoding="utf-8"

        ) as file:

            json.dump(

                self.history,

                file,

                indent=4

            )

    def normalize(self, text):

        text = text.lower()

        text = re.sub(

            r"\s+",

            " ",

            text

        )

        return text.strip()

    def analyze_prompt(self):

        print("\n========== PROMPT ANALYSIS ==========\n")

        print("Paste Prompt")

        print("Press ENTER twice to finish.\n")

        lines = []

        while True:

            line = input()

            if line == "":

                break

            lines.append(line)

        prompt = "\n".join(lines)

        if prompt == "":

            print("\nPrompt cannot be empty.")

            return

        normalized = self.normalize(

            prompt

        )

        threats = []

        score = 0

        matched = []

        for attack_type in self.attack_patterns:

            keywords = self.attack_patterns[attack_type]

            for keyword in keywords:

                if keyword in normalized:

                    threats.append(

                        attack_type

                    )

                    matched.append(

                        keyword

                    )

                    score += 20

                    break

        if len(prompt) > 4000:

            score += 10

            threats.append(

                "Oversized Prompt"

            )

        repeated = len(

            re.findall(

                r"(.)\1{7,}",

                prompt

            )

        )

        if repeated > 0:

            score += 10

            threats.append(

                "Repeated Character Pattern"

            )

        special = len(

            re.findall(

                r"[<>{}\[\]\\|`]",

                prompt

            )

        )

        if special > 25:

            score += 10

            threats.append(

                "Suspicious Characters"

            )

        score = min(

            score,

            100

        )

        if score < 25:

            risk = "Low"

        elif score < 50:

            risk = "Medium"

        elif score < 75:

            risk = "High"

        else:

            risk = "Critical"

        report = {

            "score": score,

            "risk": risk,

            "threats": threats,

            "matched": matched,

            "length": len(prompt)

        }

        self.history.append(

            report

        )

        self.save_history()

        print("\n========== RESULT ==========\n")

        print(

            "Threat Score :",

            score,

            "%"

        )

        print(

            "Risk Level :",

            risk

        )

        print(

            "Prompt Length :",

            len(prompt),

            "Characters"

        )

        print()

        if threats:

            print("Detected Threats")

            print()

            for threat in threats:

                print("-", threat)

        else:

            print("No Threats Detected.")

        print()

        if matched:

            print("Matched Patterns")

            print()

            for pattern in matched:

                print("-", pattern)

    def explain_threats(self):

        if not self.history:

            print("\nNo Analysis History Available.")

            return

        latest = self.history[-1]

        print("\n========== THREAT EXPLANATION ==========\n")

        if not latest["threats"]:

            print("No Threats Detected.")

            return

        explanations = {

            "Instruction Override":
                "Attempts to ignore or replace previous instructions.",

            "System Prompt Leak":
                "Attempts to reveal hidden system or developer prompts.",

            "Role Manipulation":
                "Attempts to change the AI's intended role or behavior.",

            "Data Exfiltration":
                "Attempts to access hidden memories, secrets, or internal data.",

            "Jailbreak Attempt":
                "Attempts to bypass safety restrictions or policies.",

            "Oversized Prompt":
                "Very large prompts may hide malicious instructions.",

            "Repeated Character Pattern":
                "Repeated characters may be used to confuse prompt filters.",

            "Suspicious Characters":
                "Unusual symbols may indicate encoded or obfuscated attacks."

        }

        for threat in latest["threats"]:

            print(f"{threat}")

            print(f"Reason : {explanations.get(threat, 'Unknown')}")

            print()

    def sanitize_prompt(self):

        if not self.history:

            print("\nNo Prompt Analysis Available.")

            return

        print("\nPaste Prompt To Sanitize")

        print("Press ENTER twice to finish.\n")

        lines = []

        while True:

            line = input()

            if line == "":

                break

            lines.append(line)

        prompt = "\n".join(lines)

        cleaned = prompt

        for attack in self.attack_patterns.values():

            for keyword in attack:

                cleaned = re.sub(

                    keyword,

                    "[REMOVED]",

                    cleaned,

                    flags=re.IGNORECASE

                )

        print("\n========== SANITIZED PROMPT ==========\n")

        print(cleaned)

    def statistics(self):

        if not self.history:

            print("\nNo Statistics Available.")

            return

        total = len(self.history)

        average = sum(

            item["score"]

            for item in self.history

        ) / total

        low = 0

        medium = 0

        high = 0

        critical = 0

        for item in self.history:

            if item["risk"] == "Low":

                low += 1

            elif item["risk"] == "Medium":

                medium += 1

            elif item["risk"] == "High":

                high += 1

            else:

                critical += 1

        print("\n========== SECURITY DASHBOARD ==========\n")

        print("Analyses :", total)

        print("Average Threat Score :", round(average, 2), "%")

        print("Low Risk :", low)

        print("Medium Risk :", medium)

        print("High Risk :", high)

        print("Critical Risk :", critical)

    def export_report(self):

        if not self.history:

            print("\nNo Report Available.")

            return

        file_name = "security_report.txt"

        with open(

            file_name,

            "w",

            encoding="utf-8"

        ) as file:

            file.write(

                "========== PROMPT SECURITY REPORT ==========\n\n"

            )

            for number, report in enumerate(

                self.history,

                start=1

            ):

                file.write(

                    f"Analysis : {number}\n"

                )

                file.write(

                    f"Threat Score : {report['score']}%\n"

                )

                file.write(

                    f"Risk : {report['risk']}\n"

                )

                file.write(

                    f"Prompt Length : {report['length']}\n"

                )

                file.write(

                    "Threats:\n"

                )

                for threat in report["threats"]:

                    file.write(

                        f"- {threat}\n"

                    )

                file.write(

                    "Matched Patterns:\n"

                )

                for pattern in report["matched"]:

                    file.write(

                        f"- {pattern}\n"

                    )

                file.write(

                    "-" * 60 + "\n"

                )

        print("\nSecurity Report Exported.")

        print("File :", file_name)

    def delete_history(self):

        if not self.history:

            print("\nHistory Empty.")

            return

        choice = input(

            "\nDelete Entire History? (yes/no): "

        ).lower()

        if choice == "yes":

            self.history.clear()

            self.save_history()

            print("\nHistory Deleted Successfully.")

        else:

            print("\nCancelled.")