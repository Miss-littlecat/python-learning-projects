from tkinter import *
from quiz_brain import QuizBrain
THEME_COLOR = "#375362"

class QuizInterface:
    def __init__(self,quiz_brain: QuizBrain):
        # quiz_brain: QuizBrain means the type of quiz_brain is QuizBrain
        self.quiz = quiz_brain
        self.window = Tk()
        self.window.title("Quizzler")
        self.window.config(padx=20, pady=20, bg=THEME_COLOR)
        self.score_label = Label(text="Score:0", bg=THEME_COLOR, fg="white",font = ("Arial", 13))
        self.score_label.grid(column=1, row=0)
        self.canvas = Canvas(bg="white", height=300, width=250)
        self.question_text = self.canvas.create_text(
            120,125,
            width=200,
            text=" Some question text.",
            fill=THEME_COLOR,
            font = ("Arial", 18))
        self.canvas.grid(row=1, column=0, columnspan=2,pady=50)
        self.right_logo = PhotoImage(file="images/true.png")
        self.wrong_logo = PhotoImage(file="images/false.png")
        self.right_button = Button(image=self.right_logo,bg=THEME_COLOR,highlightthickness=0,command=self.true_pressed)
        self.right_button.grid(row=2, column=0)
        self.wrong_button = Button(image=self.wrong_logo,bg=THEME_COLOR,highlightthickness=0,command=self.false_pressed)
        self.wrong_button.grid(row=2, column=1)
        self.get_next_question()

        self.window.mainloop()

    def get_next_question(self):
        self.canvas.config(bg="white")
        if self.quiz.still_has_questions():

            self.score_label.config(text=f"Score: {self.quiz.score}")
            q_text = self.quiz.next_question()
            self.canvas.itemconfig(self.question_text, text=q_text)
        else:
            self.canvas.itemconfig(self.question_text, text="you've finished this quiz!"
                                                            f"your final score is: {self.quiz.score}")
            self.right_button.config(state="disabled")
            self.wrong_button.config(state="disabled")

    def true_pressed(self):
        self.give_feedback( self.quiz.check_answer("True"))
        #self.canvas.itemconfig(self.question_text, text="you are right!")
    def false_pressed(self):
        is_right = self.quiz.check_answer("False")
        self.give_feedback(is_right)
        #self.canvas.itemconfig(self.question_text, text="you are wrong!")

    def give_feedback(self,is_right):
#        print(is_right)
        if is_right:
            self.canvas.config(bg="green")
        else:
            self.canvas.config(bg="red")

        self.window.after(1000, self.get_next_question)


    #
    # def check_quiz(self):
    #     user_answer = input(self.question_text)
    #     flag = self.quiz.check_answer(user_answer)
    #     if flag:
    #         print("Correct!")
    #     else:
    #         print("Incorrect!")
# How to display quiz in ui?