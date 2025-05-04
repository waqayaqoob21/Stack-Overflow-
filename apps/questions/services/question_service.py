from apps.questions.models.question import Question

class QuestionService:
    @staticmethod
    def get_all_questions():
        return Question.objects.all().order_by('-created_at')

    @staticmethod
    def filter_by_tag(tag):
        return Question.objects.filter(tags__icontains=tag)

    @staticmethod
    def search_by_title(query):
        return Question.objects.filter(title__icontains=query)

    @staticmethod
    def create_question(user, data):
        return Question.objects.create(author=user, **data)
