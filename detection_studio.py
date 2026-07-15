from prompt_injection_detector import PromptInjectionDetector


class DetectionStudio:

    def __init__(self):

        self.detector = PromptInjectionDetector()

    def display_menu(self):

        while True:

            print("\n")

            print("=" * 65)

            print("             PROMPT INJECTION DETECTOR")

            print("=" * 65)

            print("1. Analyze Prompt")

            print("2. Explain Detected Threats")

            print("3. Sanitize Prompt")

            print("4. Security Dashboard")

            print("5. Export Security Report")

            print("6. Delete Analysis History")

            print("7. Exit")

            choice = input("\nEnter Choice: ").strip()

            if choice == "1":

                self.detector.analyze_prompt()

            elif choice == "2":

                self.detector.explain_threats()

            elif choice == "3":

                self.detector.sanitize_prompt()

            elif choice == "4":

                self.detector.statistics()

            elif choice == "5":

                self.detector.export_report()

            elif choice == "6":

                self.detector.delete_history()

            elif choice == "7":

                print("\nThank You For Using Prompt Injection Detector!")

                break

            else:

                print("\nInvalid Choice. Please Try Again.")


if __name__ == "__main__":

    studio = DetectionStudio()

    studio.display_menu()