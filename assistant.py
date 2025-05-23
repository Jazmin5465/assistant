from openai import OpenAI
import time

client = OpenAI()

# curriculum_knowledge = client.files.create(
#     file = open("knowledge/OpenAIChatCompletionsAPICheatsheet.pdf", "rb"),
#     purpose = "assistants"
# )

# print(curriculum_knowledge)

def process_run(thread_id, assistant_id):
    new_run = client.beta.threads.runs.create(
    thread_id = thread_id,
    assistant_id = assistant_id
    )

    while True:
        time.sleep(1)
        print("Thinking...")

        run_check = client.beta.threads.runs.retrieve(
        thread_id = thread_id,
        run_id = new_run.id
        )

        if(run_check.status in ["cancelled", "failed", "expired", "completed"]):
            return run_check

assistant = client.beta.assistants.create(
    name = "Study Buddy",
    model = "gpt-3.5-turbo",
    instructions = "You are a helpful study buddy.",
    tools = [{
        "type": "file_search"
    }]
)

thread = client.beta.threads.create()

print("Study buddy: I'm here to assist you! Type 'exit' to exit at any time.")
user_input = ""

while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        print("\nAssistant: Goodbye!\n")
        exit()

    message = client.beta.threads.messages.create(
        thread_id = thread.id,
        role = "user",
        content = user_input
    )

    run = process_run(thread.id, assistant.id)

    if run.status == "completed":
        message_thread = client.beta.threads.messages.list(
            thread_id = thread.id
        )
        print("\nAssistant: " + message_thread.data[0].content[0].text.value + "\n")
    else:
        print("\nAssistant: An error has occured, please try again.\n")