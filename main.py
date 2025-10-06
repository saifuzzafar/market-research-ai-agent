from market_research_agent.agent import run_agent_stream
from market_research_agent.report import generate_report

if __name__ == "__main__":
    print("🤖 Enhanced Stock Analyzer AI Agent")
    print("=" * 50)
    print("Features:")
    print("• Real-time stock/crypto analysis")
    print("• Market sentiment analysis")
    print("• Investment recommendations")
    print("• Automated report generation")
    print("• Streamed execution with detailed steps")
    print("=" * 50)
    print("Type 'exit' to quit. Type 'report' to save last analysis.\n")
    last_response = None
    while True:
        query = input("Ask a question: ")
        if query.lower() in ["exit", "quit"]:
            break
        if query.lower() == "report" and last_response:
            response = generate_report(stock="", filename="report.pdf", price=last_response,sentiment="", recommendation="",)
            print(response)
            continue
        elif query.lower() == "report":
            print("No previous analysis to save as report.")
            continue
        try:
             response = run_agent_stream(query)
             last_response  = response

        except Exception as e:
            print(f"Error {e}")

