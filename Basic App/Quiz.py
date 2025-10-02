from Question import Question

question_prompts = [
    "what color are apples?\n (a)Red\n (b)orange",
    "what color are bananas?\n (a)green\n (b)yellow",
]

questions = [
    Question(question_prompts[0], "a")
    Question(question_prompts[1], "b")

]


def run_test(questions):
    score = 0
    for question in questions:
        answer = input(question.prompt)
        if answer == question.answer:
            score += 1
    print("You got " + str(score)+ "/" + str(len(questions)) + "correct")

run_test(questions)
