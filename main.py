from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route("/schedule", methods=["POST"])
def schedule_interviews():
  """
  Schedules interviews and returns the maximum number that can be attended.

  Returns:
      JSON response with the maximum number of interviews.
  """
  try:
    data = request.get_json()
    start_times = data["start_times"]
    end_times = data["end_times"]

    # Validate input
    if not start_times or not end_times or len(start_times) != len(end_times):
      return jsonify({"error": "Invalid input"}), 400

    # Sort schedules by end time
    interviews = list(zip(start_times, end_times, strict=False))
    interviews.sort(key=lambda x: x[1])

    # Track active interviews and count max concurrent
    active_interviews, max_concurrent = 0, 0
    for _, end_time in interviews:

      active_interviews -= 1  # Interview ends
      max_concurrent = max(max_concurrent, active_interviews)
      active_interviews += 1  # New interview starts

    return jsonify({"max_interviews": max_concurrent}), 200

  except Exception as e:
    return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
  app.run(debug=True)
