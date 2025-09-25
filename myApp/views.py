# views.py
from django.shortcuts import render
from django.http import Http404
from django.template.loader import select_template

# ----- Topics (order matters for prev/next) -----
TOPICS = [
    {"slug": "course-introduction",   "title": "Course Introduction",                  "about": "Promise & purpose of the lesson"},
    {"slug": "learning-outcomes",     "title": "Learning Outcomes",                    "about": "What Realtors will be able to do after this course"},
    {"slug": "prior-assumptions",     "title": "Prior Assumptions & Emotions",         "about": "Common misconceptions Realtors and clients have"},
    {"slug": "knowing-the-limits",    "title": "Knowing the Limits of Movers",         "about": "What movers can and cannot do"},
    {"slug": "expensive-freebie",     "title": "The Expensive Freebie Trap",           "about": "Why “while you’re here, could you just…” is dangerous"},
    {"slug": "stories-mistakes",      "title": "Real-World Stories & Costly Mistakes", "about": "Examples of mover requests gone wrong"},
    {"slug": "dos-and-donts",         "title": "The Do’s & Don’ts Guide",              "about": "Key rules Realtors should know and share"},
    {"slug": "client-education",      "title": "Realtor’s Role in Client Education",   "about": "Setting boundaries & preventing liability"},
    {"slug": "practice-scenarios",    "title": "Practice Scenarios & Activities",      "about": "Decision trees, checklists, and role-play"},
    {"slug": "scripts-tools",         "title": "Scripts & Communication Tools",        "about": "How to talk to clients about mover boundaries"},
    {"slug": "job-aids",              "title": "Job Aids & Takeaways",                 "about": "Quick guides, scripts, and red-flag scenarios"},
    {"slug": "wrap-up",               "title": "Wrap-Up & Key Commitments",            "about": "Core message and Realtor responsibilities"},
    {"slug": "transfer-task",         "title": "Transfer Task (24–72 Hours)",          "about": "Reflection, peer sharing, and application"},
    {"slug": "knowledge-check",       "title": "Knowledge Check / Quiz",               "about": "Short self-assessment"},
    {"slug": "closing-motivation",    "title": "Closing Motivation",                   "about": "Why being mover-smart makes you a trusted Realtor"},
]

# Optional: subtitles & meta per lesson (only add what you need)
SUBTITLES = {
    "course-introduction": "The Do’s and Don’ts of Working with Movers",
    "learning-outcomes": "What You’ll Know, Apply, and Communicate",
    "prior-assumptions": "What People Think vs. What’s Actually Safe",
    "knowing-the-limits": "Scope, Safety, and What’s Off-Limits",
    "expensive-freebie": "How ‘While You’re Here…’ Turns Into $50k",
    "stories-mistakes": "Case Studies That Sell Boundaries",
    "dos-and-donts": "The Field Guide to What’s OK—and What Isn’t",
    "client-education": "Be the Boundary-Setter Clients Respect",
    "practice-scenarios": "Live-Fire Drills for Real Conversations",
    "scripts-tools": "Say It Smoothly: Boundary Scripts That Work",
    "job-aids": "Carry, Share, and Use These Tools",
    "wrap-up": "Close Strong: Commitments That Protect Everyone",
    "transfer-task": "Lock It In: Apply Within 72 Hours",
    "knowledge-check": "Quick Confidence Check",
    "closing-motivation": "Finish Strong: Lead with Protection & Trust",
}

META = {
    "course-introduction": {"duration": "10–15 mins", "level": "All Agents"},
    "learning-outcomes":   {"duration": "8–12 mins",  "level": "All Agents"},
    "prior-assumptions": {"duration": "8–12 mins", "level": "All Agents"},
    "knowing-the-limits": {"duration": "10–15 mins", "level": "All Agents"},
    "expensive-freebie": {"duration": "8–12 mins", "level": "All Agents"},
    "stories-mistakes": {"duration": "10–15 mins", "level": "All Agents"},
    "dos-and-donts": {"duration": "10–15 mins", "level": "All Agents"},
    "client-education": {"duration": "10–15 mins", "level": "All Agents"},
    "practice-scenarios": {"duration": "12–18 mins", "level": "All Agents"},
     "scripts-tools": {"duration": "10–15 mins", "level": "All Agents"},
     "job-aids": {"duration": "8–12 mins", "level": "All Agents"},
     "wrap-up": {"duration": "6–10 mins", "level": "All Agents"},
     "transfer-task": {"duration": "6–10 mins", "level": "All Agents"},
    "knowledge-check": {"duration": "6–10 mins", "level": "All Agents"},
    "closing-motivation": {"duration": "4–7 mins", "level": "All Agents"},
    # add more as needed…
}

# ----- Overview -----
def lesson6(request):
    context = {
        "topics": TOPICS,
        "duration": "60–75 mins",
        "level": "All Agents",
    }
    return render(request, "lesson6_overview.html", context)

# ----- Detail -----
def lesson_detail(request, slug):
    # must be a known slug
    try:
        idx = next(i for i, t in enumerate(TOPICS) if t["slug"] == slug)
    except StopIteration:
        raise Http404("Lesson not found")

    topic = TOPICS[idx]
    prev_topic = TOPICS[idx - 1] if idx > 0 else None
    next_topic = TOPICS[idx + 1] if idx < len(TOPICS) - 1 else None

    # Prefer a specific template: lesson_detail_<slug>.html
    # Fall back to a generic template if it doesn't exist yet.
    template = select_template([
        f"lesson_detail_{slug}.html",  # e.g., lesson_detail_learning-outcomes.html
        "lesson_detail_generic.html",
    ])

    # Build lesson context
    lesson_ctx = {
        "title": topic["title"],
        "subtitle": SUBTITLES.get(slug, ""),
        "meta": META.get(slug, {}),
    }

    ctx = {
        "lesson": lesson_ctx,
        "slug": slug,
        "prev_topic": prev_topic,
        "next_topic": next_topic,
        "all_topics": TOPICS,
    }
    return render(request, template.template.name, ctx)


import json, requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

WEBHOOK_URL = "https://katalyst-crm.fly.dev/webhook/1390f5ad-851a-4b6f-ba50-2f084cfc436d"

@csrf_exempt
def chat_proxy(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST only"}, status=405)
    try:
        payload = json.loads(request.body.decode("utf-8"))
    except Exception:
        payload = {"message": request.body.decode("utf-8")}
    try:
        r = requests.post(WEBHOOK_URL, json=payload, timeout=25)
        # Try to pass through JSON if possible; else wrap as text
        try:
            data = r.json()
        except Exception:
            data = {"reply": r.text}
        return JsonResponse(data, status=r.status_code)
    except requests.RequestException as e:
        return JsonResponse({"error": "Upstream error", "detail": str(e)}, status=502)
