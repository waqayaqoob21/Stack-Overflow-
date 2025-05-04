from apps.answers.models.answer import Answer
# Create your Services here.
class AnswerService:
    @staticmethod
    def accept_answer(answer):
        answer.is_accepted = True
        answer.save()
        return answer
